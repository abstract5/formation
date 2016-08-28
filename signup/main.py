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
import cgi
import re

USER_RE = re.compile("^[a-zA-Z0-9_-]{3,20}$")
def valid_username(usename):
    return USER_RE.match(usename)

PASS_RE = re.compile("^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")
def valid_email(mail):
    return EMAIL_RE.match(mail)


sign_form = """
<h1>Signup</h1>
<form method="post">
    <table>
        <tr>
            <td>Username: </td>
            <td><input name="username" value="%(username)s" required/>
            <span style="color: red">%(use_error)s</span>
            </td>
        </tr>
        <tr>
            <td>Password: </td>
            <td><input type="password" name="passw" required/>
            <span style="color: red">%(pass_error)s</span>
            </td>
        </tr>
        <tr>
            <td>Verify Password: </td>
            <td><input type="password" name="pass_c" required/>
            </td>
        </tr>
        <tr>
            <td>Email (Optional): </td>
            <td><input name="email" value="%(email)s"/>
            <span style="color: red">%(email_error)s</span>
            </td>
        </tr>
    </table>
    <input type="submit"/>
</form>
"""

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username="", use_error="", pass_error="", email="", email_error=""):
         self.response.write(sign_form % {"username": username,
                                        "use_error": use_error,
                                        "pass_error": pass_error,
                                        "email": email,
                                        "email_error": email_error})

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get("username")
        passw = self.request.get("passw")
        pass_c = self.request.get("pass_c")
        email = self.request.get("email")

        if not valid_username(username):
            use_error = "Please enter a valid username."
            self.write_form()
        if not valid_password(passw):
            pass_error = "Please enter a valid Password."
            self.write_form()
        if not passw == pass_c:
            pass_error = "Your passwords do not match."
            self.write_form()
        if email:
            if not valid_email(email):
                email_error = "That is not a valid email."
                self.write_form()
        else:
            self.redirect("/welcome")

class WelcomeHandler(webapp2.RequestHandler):
    def post(self):
        username = self.request.get("username")
        self.response.write("<h1><b>Welcome, " + username + "!</b></h1>")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
