from google.appengine.api import mail
from BaseHandler import BaseHandler, user_required, admin_required
from utils import render_text_template
import logging
import datetime

class UserCreateHandler(BaseHandler):
    @admin_required
    def get(self):
        self.render_template('user_create.html')

    @admin_required
    def post(self):
        logging.info('Signup handler')
        user_name = self.request.get('username').strip()
        
        email = self.request.get('email').strip()
        
        name = self.request.get('name').strip()
        last_name = self.request.get('lastname').strip()
        password = self.request.get('password').strip()
        password2 = self.request.get('password2').strip()

        if password != password2:
            self.render_template('user_create.html', {'error': 'The passwords provided do not match'})
            return
        logging.info('here we go ?')

        subscription = self.request.get('subscription').strip()
        role = self.request.get('role').strip()

        expiration_day = self.request.get('expiration_day').strip()
        expiration_month = self.request.get('expiration_month').strip()
        expiration_year = self.request.get('expiration_year').strip()
        subscription_expiration_date = None
        if expiration_day != '' and expiration_month != '' and expiration_year != '':
            try:
                expiration_date = datetime.date(int(expiration_year), int(expiration_month), int(expiration_day))
                
            except (TypeError, ValueError) as e:
                logging.info('User create failed because of %s', type(e))
                self.render_template('user_create.html', {'error': 'Expiration date parsing error: ' + e.message })
                return

        unique_properties = ['email_address']
        user_data = self.user_model.create_user(user_name,
                                                unique_properties,
                                                email_address=email, 
                                                role=role,
                                                subscription=subscription,
                                                subscription_expiration_date=subscription_expiration_date,
                                                name=name,
                                                last_name=last_name,
                                                password_raw=password,
                                                verified=False)
        if not user_data[0]: #user_data is a tuple
            self.render_template('user_create.html',{ 'error':'Unable to create user for email %s because of \
                duplicate keys %s' % (user_name, user_data[1])})
            return
        logging.info('user created')
        user = user_data[1]
        user_id = user.get_id()

        token = self.user_model.create_signup_token(user_id)

        verification_url = self.uri_for('verification', type='v', user_id=user_id,
        signup_token=token, _full=True)
        logging.info(verification_url)
        msg = render_text_template('user_added_email.html', {'name': name, 'site': self.request.host_url, 'user_name': user_name, 'url': verification_url, 'password': password})
       
        self.display_message(msg)
        logging.info('Try to send email')
        
        try:
            message = mail.EmailMessage()
            message.sender = "info@analyticstraining.it"
            message.to = email
            message.subject = "Registration to AT Tools"
            message.html = msg
            message.send()
        except Exception as e:
            logging.info("Some error occurred %s", str(e))