from BaseHandler import BaseHandler,  admin_required

class UserManagerHandler(BaseHandler):
    @admin_required
    def get(self):
        allUsers = self.user_model.query().fetch()
       
        self.render_template('user_manager.html',{'users': allUsers})