from google.appengine.ext import ndb

class MyContent(ndb.Model):
    """Class to model the CMS content"""
    title = ndb.StringProperty(required=True)
    slug = ndb.TextProperty(required=False) #User can provide a "friendly name" for the content in order to have a human readable URL
    description = ndb.TextProperty(required=False)
    content_type = ndb.TextProperty(required=True) # page | app |something else
    content = ndb.TextProperty(required=True)
    visibility = ndb.IntegerProperty(required=True) #public | private
    subscriptions = ndb.StringProperty(required=False, repeated=True) # needed only when an item has public visibility
    created_by_user_id = ndb.IntegerProperty(required=True)
    modified_by_user_id = ndb.IntegerProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def get_by_user(cls, user):
        """Retrieve all items that a user can see or that somebody not logged in can see (user = None)"""
        if user == None:
            return cls.query(cls.visibility == 2)
        if user.is_cms_admin:
            return cls.query() # admin has full visibility of everything
        user_subscription = user.subscription
        user_id = user.get_id()
        return cls.query(
            ndb.OR(cls.created_by_user_id == user_id,
                ndb.AND(cls.subscriptions == user_subscription,
                    ndb.OR(cls.visibility == 1, cls.visibility == 2)
                )
            )
        )

    def can_user_view(self, user):
        if user == None:
            return self.visibility == 2
        if user.is_cms_admin:
            return True
        user_id = user.get_id()
        if self.created_by_user_id == user_id:
            return True
        if (self.visibility == 1 or self.visibility == 2) and user.subscription in self.subscriptions:
            return True
        return False

    def can_user_edit(self, user):
        user_id = user.get_id()

        return self.created_by_user_id == user_id or user.is_cms_admin or user.is_cms_editor
