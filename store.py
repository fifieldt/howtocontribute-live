#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Form storage

Captures the form data and saves it to a database
"""

import web

app = web.application(('/', 'Index'), globals())
responses = open('responses.txt', 'a')

class Index(object):
    def POST(self):
        #strip <Storage ... > and add new line
        response = str(web.input())[9:-1] + "\n"
        responses.write(response)
        return "Thank you"

    def GET(self):
        return "no GET."

if __name__ == "__main__":
    app.run()
