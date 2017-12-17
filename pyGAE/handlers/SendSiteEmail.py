from google.appengine.api import mail
from BaseHandler import BaseHandler, user_required, admin_required, app_name
from google.appengine.ext.webapp import template
import os.path
import logging
import app_config

def send_signup_email(user_data, home_url, verification_url):
    path = os.path.join(os.path.dirname(__file__), '../email_templates', 'welcome_signup.html')
    logging.info('template path: %s' %( path))
    
    params = {}
    params['app_name'] = app_config.APP_NAME
    params['home_url'] = home_url
    params['verification_url'] = verification_url
    params['user'] = user_data
    msg = template.render(path, params)

    logging.info(msg)
    logging.info('Trying to send email')
    
    try:
        message = mail.EmailMessage()
        message.sender = app_config.MAIL_SENDER
        message.to = user_data['email']
        message.subject = "Registration to " + app_config.APP_NAME
        message.html = msg
        message.send()
    except Exception as e:
        logging.info("Some error occurred %s", str(e))