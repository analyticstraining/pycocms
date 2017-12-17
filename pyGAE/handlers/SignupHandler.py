from google.appengine.api import mail
from BaseHandler import BaseHandler, user_required, admin_required, app_name
from google.appengine.ext.webapp import template
from SendSiteEmail import send_signup_email
import os.path
import logging
import app_config

class SignupHandler(BaseHandler):
    def get(self):
        self.render_template('signup.html')

    def post(self):
        logging.info('Signup handler')
        user_name = self.request.get('username')
        email = self.request.get('email')
        name = self.request.get('name')
        password = self.request.get('password')
        last_name = self.request.get('lastname')

        unique_properties = ['email_address']
        user_data = self.user_model.create_user(user_name,
                                                unique_properties,
                                                email_address=email, 
                                                role='user',
                                                subscription='basic',
                                                name=name,
                                                last_name=last_name,
                                                password_raw=password,
                                                verified=False)
        if not user_data[0]: #user_data is a tuple
            self.display_message('Unable to create user for email %s because of \
                duplicate keys %s' % (user_name, user_data[1]))
            return
        logging.info('user created')
        user = user_data[1]
        user_id = user.get_id()

        token = self.user_model.create_signup_token(user_id)

        verification_url = self.uri_for('verification', type='v', user_id=user_id, signup_token=token, _full=True)
        home_url = self.uri_for('home')
        logging.info(verification_url)

        send_signup_email( {'user_name': user_name, 'name': name, 'last_name': last_name, 'email': email}, home_url, verification_url)
        
        self.redirect(self.uri_for('signedup', user_id=user_id), abort=True)

class SignedUpHandler(BaseHandler): 
    def get(self, *args, **kwargs):
        
        user_id = kwargs['user_id']
        logging.info('SignedUp Handler %s', user_id)
        target_user = self.user_model.get_by_user_id(int(user_id))
        if not target_user:
            self.abort(404)
        self.render_template('signedup.html', {
            'mail_sender': app_config.MAIL_SENDER,
            'target_user': target_user
        })
