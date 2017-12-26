from BaseHandler import BaseHandler, user_required, admin_required
import logging
import datetime
from google.appengine.ext import ndb

class UserEditorHandler(BaseHandler):
    @admin_required
    def get(self, *args, **kwargs):
        user_id = kwargs['user_id']
        edit_user = self.user_model.get_by_id(int(user_id))
        params = {'edit_user': edit_user}
       
        self.render_template('user_editor.html',params)

    @admin_required
    def post(self, *args, **kwargs):
        logging.info('User Editor handler POST')
        user_id = kwargs['user_id']
        edit_user = self.user_model.get_by_id(int(user_id))
        name = self.request.get('name')
        last_name = self.request.get('last_name')
        role = self.request.get('role')
        subscription = self.request.get('subscription')

        expiration_day = self.request.get('expiration_day').strip()
        expiration_month = self.request.get('expiration_month').strip()
        expiration_year = self.request.get('expiration_year').strip()

        if expiration_day != '' and expiration_month != '' and expiration_year != '':
            try:
                expiration_date = datetime.date(int(expiration_year), int(expiration_month), int(expiration_day))
                edit_user.subscription_expiration_date = expiration_date
            except (TypeError, ValueError) as e:
                logging.info('User edit for user  %s  failed because of %s', edit_user.name, type(e))
                self.render_template('user_editor.html', {'edit_user': edit_user, 'error': 'Expiration date parsing error: ' + e.message })
                return
        edit_user.name = name
        edit_user.last_name = last_name
        edit_user.role = role
        edit_user.subscription = subscription
        edit_user.put()
        self.render_template('user_editor.html', {'edit_user': edit_user, 'user_updated': True})
