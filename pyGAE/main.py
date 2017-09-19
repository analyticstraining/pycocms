#!/usr/bin/env python

import logging
import webapp2

from handlers import *
from app_config import APP_CONFIG

app = webapp2.WSGIApplication([
    webapp2.Route('/', HomeHandler, name='home'),
    webapp2.Route('/signup', SignupHandler),
    webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',
      handler=VerificationHandler, name='verification'),
    webapp2.Route('/password', SetPasswordHandler),
    webapp2.Route('/unauthorized', UnauthorizedHandler, name='unauthorized'),
    webapp2.Route('/login', LoginHandler, name='login'),
    webapp2.Route('/logout', LogoutHandler, name='logout'),
    webapp2.Route('/forgot', ForgotPasswordHandler, name='forgot'),
    webapp2.Route('/manage/users', UserManagerHandler, name='usermanager'),
    webapp2.Route('/user/create', UserCreateHandler, name='usercreate'),
    webapp2.Route('/user/edit/<user_id:.+>', UserEditorHandler, name='useredit'),
    webapp2.Route('/user/profile', UserProfileHandler, name='userprofile'),
    webapp2.Route('/user/subscription', ManageSubscriptionHandler, name='managesubscription'),
    webapp2.Route('/authenticated', AuthenticatedHandler, name='authenticated'),
    webapp2.Route('/content/create', CreateContentHandler, name='createContent'),
    webapp2.Route('/content/delete/<page:.+>', DeleteContentHandler, name='deleteContent'),
    webapp2.Route('/content/edit/<page:.+>', EditContentHandler, name='createContent'),
    webapp2.Route('/content/<page:.+>', ViewContentHandler, name="viewContent"),
    webapp2.Route('/content', ViewContentHandler, name="viewContent"),
    webapp2.Route('/<page>', ViewContentHandler, name="viewContentRoot")
    
], debug=True, config=APP_CONFIG)

logging.getLogger().setLevel(logging.DEBUG)
