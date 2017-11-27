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

""" Settings including hostnames, ports, APP_ID, logging level, etc Settings
is used for most of the modules, servers, and clients
"""

from enum import Enum
import logging

class Settings(Enum):
    """ Governs settings for most modules, servers, and clients """

    HOST = "0.0.0.0"                            #local host used to bind locally
    HOST_REMOTE = "192.168.1.143"               #DEV remote host used to bind remotely 
    PORT = 8000                                 #TCP port for the first server
    APP_ID = "123adalsdjfhaldfjkahl234234234"   #app id for security
    LOGGING_LEVEL = logging.DEBUG               #logging level
    ADMIN_USER = "admin"                        #controller admin username
    ADMIN_PASS = "autobotfun"                   #controller admin password

    

    

