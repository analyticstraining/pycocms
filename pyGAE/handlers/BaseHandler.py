from google.appengine.ext.webapp import template
from google.appengine.ext import ndb

import logging
import os.path
import webapp2

from webapp2_extras import auth
from webapp2_extras import sessions

def roles_required(*roles):
    def required_decorator(handler):
        logging.info('role_required %s ' % (str(roles)))
        def check(self, *args, **kwargs):
            auth = self.auth
            user_info = auth.get_user_by_session()
            if not user_info:
                self.redirect(self.uri_for('login'), abort=True)
            else:
                user = self.user_model.get_by_id(user_info['user_id'])
                if user.role in roles:
                    return handler(self, *args, **kwargs)
                else:
                    self.redirect(self.uri_for('login'), abort=True)
        return check
    return required_decorator

def user_required(handler):
    """
        Decorator that checks if there's a user associated with the current session.
        Will also fail if there's no session present.
    """
    def check_login(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
            self.redirect(self.uri_for('login'), abort=True)
        else:
            return handler(self, *args, **kwargs)

    return check_login

def admin_required(handler):
    def check_login(self, *args, **kwargs):
        auth = self.auth
        user_info = auth.get_user_by_session()
        if not user_info:
            self.redirect(self.uri_for('login'), abort=True)
        else:
            user = self.user_model.get_by_id(user_info['user_id'])
            if not user.is_cms_admin:
                self.redirect(self.uri_for('unauthorized'), abort=True)
            else:
                return handler(self, *args, **kwargs)
    return check_login

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def auth(self):
        """Shortcut to access the auth instance as a property."""
        return auth.get_auth()

    @webapp2.cached_property
    def user_info(self):
        """Shortcut to access a subset of the user attributes that are stored
        in the session.

        The list of attributes to store in the session is specified in
        config['webapp2_extras.auth']['user_attributes'].
        :returns
        A dictionary with most user information
        """
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user(self):
        """Shortcut to access the current logged in user.

        Unlike user_info, it fetches information from the persistence layer and
        returns an instance of the underlying model.

        :returns
        The instance of the user model associated to the logged in user.
        """
        u = self.user_info
        return self.user_model.get_by_id(u['user_id']) if u else None

    @webapp2.cached_property
    def user_model(self):
        """Returns the implementation of the user model.

        It is consistent with config['webapp2_extras.auth']['user_model'], if set.
        """    
        return self.auth.store.user_model

    @webapp2.cached_property
    def session(self):
        """Shortcut to access the current session."""
        return self.session_store.get_session(backend="datastore")

    def render_template(self, view_filename, params=None, scripts=[]):
        '''
        render_template('view file name', {params})
        Renders a view template. Implicit parameters:
        - user_info: (self.user_info)
        - user: (self.user)
        - host_url: URL of the host
        - scripts: URL for the scripts directory
        - styles: URL for the css directory
        '''
        if not params:
            params = {}
        base_scripts = ['jquery.min.js', 'bootstrap.min.js']
        base_scripts_path = self.request.host_url + '/js'
        page_scripts = []
        for script in base_scripts:
            page_scripts.append(base_scripts_path + '/' + script)
        
        for script in scripts:
            page_scripts.append(base_scripts_path + '/' + script)
        params['user_info'] = self.user_info
        params['user'] = self.user
        params['host_url'] = self.request.host_url
        params['page_scripts'] = page_scripts
        params['styles'] = self.request.host_url + '/css'
        # shameless hack, remove that '..'
        path = os.path.join(os.path.dirname(__file__), '../views', view_filename)
        self.response.out.write(template.render(path, params))

    def display_message(self, message):
        """Utility function to display a template with a simple message."""
        params = {
            'message': message
        }
        self.render_template('message.html', params)

    # this is needed for webapp2 sessions to work
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)
