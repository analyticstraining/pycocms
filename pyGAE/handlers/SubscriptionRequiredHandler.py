from BaseHandler import BaseHandler
class SubscriptionRequiredHandler(BaseHandler):
    def get(self, *args, **kwargs):
        subscription_level= kwargs['subscription']
        is_expired = kwargs['expired']
        self.render_template('subscription_required.html', {'subscription_level': subscription_level, 'is_expired': is_expired})