'''
Configuration script in Python.
Add a secret_key
'''

APP_CONFIG = {
    'webapp2_extras.auth': {
        'user_model': 'models.User',
        'user_attributes': ['name', "email_address"]
    },
    'webapp2_extras.sessions': {
        'secret_key': 'YOUR_SECRET_KEY'
    }
}