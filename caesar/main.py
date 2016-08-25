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
from caesar import encrypt
import cgi

en_form="""
<form method="post">
    <label>Enter rotation amount:
        <input name="rot" value="%(rot)s"/>
    </label>
    <br>
    <textarea rows="6" cols="50" name="en">%(en)s</textarea>
    <br>
    <input type="submit"/>
</form>
"""

class MainHandler(webapp2.RequestHandler):
    def write_form(self, rot="", en=""):
        self.response.write(en_form % {"rot": cgi.escape(rot, quote=True),
                                        "en": cgi.escape(en, quote=True)})

    def get(self):
        self.write_form()

    def post(self):
        user_rot = self.request.get("rot")
        user_en = self.request.get("en")

        if user_rot.isdigit():
            rot_amount = int(user_rot)
            user_en = encrypt(user_en, rot_amount)

        self.write_form(user_rot, user_en)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
