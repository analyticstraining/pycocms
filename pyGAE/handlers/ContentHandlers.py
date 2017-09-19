from BaseHandler import BaseHandler, user_required, roles_required
from models import MyContent
import logging
from google.appengine.ext import ndb

class CreateContentHandler(BaseHandler):
    @roles_required('editor', 'admin')
    def get(self):
        # retrieve all posts
        self.render_template('createcontent.html')

    @roles_required('editor', 'admin')
    def post(self):
        title = self.request.get('title')
        description = self.request.get('description')
        content = self.request.get('content')
        visibility = int(self.request.get('visibility'))
        subscriptions = self.request.get('subscriptions', allow_multiple=True)
        user = self.user
        logging.info('creating content for user %s' % (user.email_address))
        myContent = MyContent(title=title,
                              description=description,
                              content_type='page',
                              content=content,
                              visibility=visibility,
                              subscriptions=subscriptions,
                              created_by_user_id=user.get_id(),
                              modified_by_user_id=user.get_id())
        key = myContent.put()
        self.display_message('Content created <a href="/content/%s">%s</a>' % (key.urlsafe(),key.urlsafe()))

class DeleteContentHandler(BaseHandler):
    @roles_required('editor', 'admin')
    def get(self, *args, **kwargs):
        logging.info('DeleteContentHandler')
        page_id = kwargs['page']
        key = ndb.Key(urlsafe=page_id)
        content = key.get()
        content.key.delete()
        self.redirect("/content")

class EditContentHandler(BaseHandler):
    @roles_required('editor', 'admin')
    def get(self, *args, **kwargs):
        logging.info('EditContentHandler')
        page_id = kwargs['page']
        key = ndb.Key(urlsafe=page_id)
        content = key.get()
        self.render_template('editcontent.html',
                             {'id': page_id,
                              'title': content.title,
                              'content': content,
                             })

    @roles_required('editor', 'admin')
    def post(self, *args, **kwargs):
        content_id = kwargs['page']
        key = ndb.Key(urlsafe=content_id)
        content = key.get()
        logging.info(str(content))
        content.title = self.request.get('title')
        content.description = self.request.get('description')
        logging.info('description: ' + content.description)
        content.content = self.request.get('content')
        content.visibility = int(self.request.get('visibility'))
        content.subscriptions = self.request.get('subscriptions', allow_multiple=True)
        content.put()
        self.display_message('Content updated <a href="/content/%s">%s</a>' % (key.urlsafe(),key.urlsafe()))

class ViewContentHandler(BaseHandler):

    def get(self, *args, **kwargs):
        logging.info('ViewContentHandler (user: %s)' %( str(self.user) ))
        #id = kwargs['id']
        #id = self.request.get('id')
        #id = None
        if kwargs.has_key('page'):
            page_id = kwargs['page']
            #retrieve specific content
            key = ndb.Key(urlsafe=page_id)
            content = key.get()
            if not content.can_user_view(self.user):
                #self.response.set_status(403)
                self.abort(403, 'You are not authorized to access this resource')
            else:
                self.render_template('content.html',
                                 {'id': page_id, 
                                  'title': content.title,
                                  'content': content.content,
                                  'canEdit': content.can_user_edit(self.user)})
        else:
            # retrieve all content
            content = MyContent.get_by_user(self.user).fetch()
            htmlContent = []
            for element in content:
                created_by_key = ndb.Key(self.user_model, element.created_by_user_id)
                created_by_user = created_by_key.get() 
                newElement = {
                    'id': element.key.urlsafe(),
                    'title': element.title,
                    'content': element.content,
                    'created_by': created_by_user.email_address
                }
                htmlContent.append(newElement)
            self.render_template('contentlist.html',
                                 params={'contents': htmlContent, 'rawcontent': content})
