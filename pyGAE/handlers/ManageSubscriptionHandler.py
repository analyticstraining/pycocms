from BaseHandler import BaseHandler, user_required
from models import MyContent
import logging
from google.appengine.ext import ndb

class ManageSubscriptionHandler(BaseHandler):
    @user_required
    def get(self):
        self.render_template('manage_subscription.html')