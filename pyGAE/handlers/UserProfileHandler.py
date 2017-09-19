from BaseHandler import BaseHandler, user_required
from models import MyContent
import logging
from google.appengine.ext import ndb

class UserProfileHandler(BaseHandler):
    @user_required
    def get(self):
        self.render_template('user_profile.html')

    @user_required
    def post(self):
        logging.info('User Profile handler POST')
        user = self.user
        #user_name = self.request.get('username')
        #email = self.request.get('email')
        name = self.request.get('name')
        user.name = name
        logging.info('User name %s (%s)' %(name, user.name))
        password = self.request.get('password')
        password2 = self.request.get('password2')
        
        if password != None and password != '':
            if password != password2:
                self.render_template('user_profile.html', {'error': 'Password Mismatch'})
                return
            else:
                logging.info('changing password %s' % (password))
                user.set_password(password)
        else:
            logging.info('No password provided')
        last_name = self.request.get('last_name')
        user.last_name = last_name
        user.put()

        self.render_template('user_profile.html', {'user_updated': True})

