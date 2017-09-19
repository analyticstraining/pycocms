from google.appengine.api import mail
from BaseHandler import BaseHandler, user_required, admin_required
import logging

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

        verification_url = self.uri_for('verification', type='v', user_id=user_id,
        signup_token=token, _full=True)
        logging.info(verification_url)
        msg = 'Send an email to user in order to verify their address. \
            They will be able to do so by visiting <a href="{url}">{url}</a>'
        self.display_message(msg.format(url=verification_url))
        logging.info('Try to send email')
        
        try:
            message = mail.EmailMessage()
            message.sender = "info@analyticstraining.it"
            message.to = email
            message.subject = "Registration to AT Tools"
            message.html = msg.format(url=verification_url)
            message.send()
        except Exception as e:
            logging.info("Some error occurred %s", str(e))