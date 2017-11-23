###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Vladimir Collak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

"""
Used to serve static content and log the controller client in. The controller
client is a page that includes controls (forward, backward, left, right, stop). 
When user presses the appropriate button we'll use javascript to send the command 
to a websocket server. 
"""

from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from settings import settings
 
app = Flask(__name__)


@app.route('/')
def home():
    """
    Root site. Show the controller UI if logged in or login 
    """
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('controller.html')
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    """
    User needs to log in
    """

    admin_user = settings.Settings.ADMIN_USER.value
    admin_pass = settings.Settings.ADMIN_PASS.value

    if request.form['password'] == admin_pass and request.form['username'] == admin_user:
        session['logged_in'] = True
    else:
        flash('Wrong password!')
    return home()

@app.route("/logout")
def logout():
    """ 
    User needs to log out 
    """

    session['logged_in'] = False
    return home()

 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=80)

    
    