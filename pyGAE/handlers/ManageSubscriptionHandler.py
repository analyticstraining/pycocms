from BaseHandler import BaseHandler, user_required

class ManageSubscriptionHandler(BaseHandler):
    @user_required
    def get(self):
        self.render_template('manage_subscription.html')