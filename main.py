#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
from google.appengine.api import mail
import os
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
class MainHandler(webapp2.RequestHandler):    
    def get (self):
        template_values = {} 
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
class ApplyHandler(webapp2.RequestHandler):    
    def get (self):
        template_values = {} 
        template = JINJA_ENVIRONMENT.get_template('apply.html')
        self.response.write(template.render(template_values))

class SubmitHandler(webapp2.RequestHandler):
    def post(self):
        filename = self.request.POST["myfile"].filename
        name = self.request.get("name")
        message = mail.EmailMessage(sender= name+" <vy@fju.us>",
                                subject=name+" Application")

        message.to = "<careers@taramt.com>"
        message.body = """ 
First Name:  """+self.request.get("name")+ """
Email:  """ +self.request.get("email")+ """
Mobile No:  """ +self.request.get("phone")

        message.attachments = [(filename, self.request.POST.get('myfile').file.read())]
        message.send()
        self.response.write('Successfully submitted ')


class ContactHandler(webapp2.RequestHandler):
    def post(self):
        msg = "Message:  " + self.request.get("message")

        name = self.request.get("name")
        message = mail.EmailMessage(sender= name+" <vy@fju.us>",
                                subject=" Query " + msg)

        message.to = "<careers@taramt.com>"
        message.body = """ 
First Name:  """+self.request.get("name")+ """
Email:  """ +self.request.get("email")+ """
Mobile No:  """ +self.request.get("phone") + """
""" + msg
        
        message.send()
        self.response.write('Successfully submitted ')

app = webapp2.WSGIApplication([
    ('/apply',ApplyHandler),
    ('/', MainHandler),
    ('/submit', SubmitHandler),
    ('/contact', ContactHandler)
    
], debug=True)
