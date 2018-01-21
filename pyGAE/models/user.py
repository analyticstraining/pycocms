import time
import datetime as dt
import webapp2_extras.appengine.auth.models
from google.appengine.ext import ndb
from webapp2_extras import security
import logging

SUBSCRIPTION_LEVELS = [
    'basic',
    'silver',
    'gold'
]

SUBSCRIPTION_DAYS_DEFAULT = 31

class SubscriptionException(Exception):
    """Simple Exception class to handle Subscription related errors"""
    def __init__(self, message):
        super(SubscriptionException, self).__init__(message)
        self.message = message
    def __str__(self):
        return self.message

class User(webapp2_extras.appengine.auth.models.User):
    """class modeling the User. It extends the basic User class with some utility functions"""
    # role can be 'user', 'editor' or 'admin'
    role = ndb.StringProperty(required=True)
    subscription = ndb.StringProperty()
    subscription_expiration_date = ndb.DateTimeProperty(required=False)
    subscription_canceled = ndb.BooleanProperty(required=False)
    subscription_cancel_date = ndb.DateTimeProperty(required=False)
    subscription_change_date = ndb.DateTimeProperty(required=False)
    subscription_change_reason = ndb.StringProperty(required=False)
    def set_password(self, raw_password):
        """Sets the password for the current user

        :param raw_password:
            The raw password which will be hashed and stored
        """
        self.password = security.generate_password_hash(raw_password, length=12)

    #To retrieve a user you can do:
    #    user = self.user_model.get_by_id(int(user_id))
    #@classmethod
    #def get_by_user_id(cls, user_id):
    #    user_key = ndb.Key(cls, user_id)
    #    user = user_key.get()
    #    return user
    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        """Returns a user object based on a user ID and token.

        :param user_id:
            The user_id of the requesting user.
        :param token:
            The token string to be verified.
        :returns:
            A tuple ``(User, timestamp)``, with a user object and
            the token timestamp, or ``(None, None)`` if both were not found.
        """
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        # Use get_multi() to save a RPC call.
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp

        return None, None

    @property
    def is_cms_admin(self):
        '''Checks the role to see if the user is a CMS admin'''
        return self.role == 'admin'

    @property
    def is_cms_editor(self):
        '''Checks the role to see if the user is a CMS editor'''
        return self.role == 'editor'

    @property
    def can_add_cms_pages(self):
        '''Checks the role to see if the user is enabled to add a page to the CMS.
           Only editors and admin can do that'''
        return self.is_cms_admin or self.is_cms_editor

    @property
    def user_id(self):
        '''Returns the ID of the user'''
        return self.get_id()

    def start_subscription(self, subscription_level, expiration_date=None, change_reason='start'):
        if not subscription_level in SUBSCRIPTION_LEVELS:
            raise SubscriptionException("Unknown subscription level %s" % str(subscription_level))
        if subscription_level == 'basic' and  not expiration_date is None:
            raise SubscriptionException('basic subscription needs no expiration date')
        self.subscription = subscription_level
        if subscription_level != 'basic' and expiration_date is None:
            expiration_date = dt.datetime.utcnow() + dt.timedelta(days=SUBSCRIPTION_DAYS_DEFAULT)
        self.subscription_expiration_date = expiration_date
        self.subscription_change_date = dt.datetime.utcnow()
        self.subscription_change_reason = change_reason
        self.subscription_canceled = False
        self.put()

    def cancel_subscription(self, reason):
        self.subscription_canceled = True
        self.subscription_cancel_date = dt.datetime.utcnow()
        self.put()
        #self.start_subscription('basic', change_reason="cancel_" + reason)

    def set_subscription_expiration_date(self, expiration_date):
        self.subscription_change_date = dt.datetime.utcnow()
        self.subscription_change_reason = 'set_expiration_date'
        self.subscription_expiration_date = expiration_date
        self.put()

    def renew_subscription(self, days=SUBSCRIPTION_DAYS_DEFAULT):
        if isinstance(self.subscription_expiration_date, dt.datetime):
            self.subscription_expiration_date += dt.timedelta(days)
            self.subscription_change_date = dt.datetime.utcnow()
            self.subscription_change_reason = 'renew'
            self.subscription_canceled = False
            self.put()
        else:
            raise SubscriptionException("subscription expiration date not a datetime")

    def check_subscription(self):
        '''
        Retrieves the type of subscription and a flag saying if it is expired or not.
        It returns a dict {"subscription": String, "is_expired": Boolean}
        If the subscription is expired then it downgrades it to 'basic'
        '''
        is_expired = False
        if self.subscription_expiration_date != None:
            is_expired = self.subscription_expiration_date < dt.datetime.utcnow()
            logging.info('is_expired %s' %(is_expired))
            if is_expired:
                self.start_subscription('basic', change_reason="expired")
        logging.info('check_subscription %s %s' %(self.subscription, str(is_expired)))
        return (self.subscription, is_expired)
