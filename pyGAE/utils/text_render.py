from google.appengine.ext.webapp import template
import os.path

def render_text_template(text_filename, params=None):
    path = os.path.join(os.path.dirname(__file__), '../texts', text_filename)
    return template.render(path, params)