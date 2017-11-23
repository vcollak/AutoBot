#! /bin/bash

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

### BEGIN INIT INFO
# Provides:          autoBot
# Required-Start:    $local_fs $remote_fs
# Required-Stop:
# X-Start-Before:    rmnologin
# Default-Start:     2 3 4 5
# Default-Stop:
# Short-Description: Start the autoBot script
# Description: Start the autoBot script on PI. autoBot controlls the robot
### END INIT INFO

robotPath="/home/pi/robot/clientRobot.py"

case "$1" in
  start)
        # start the script
        if [ -f $robotPath  ]
        then
                sudo python3 $robotPath & >&1
        fi
        ;;
  stop)
        #stop the robot
        sudo kill `ps -ef | grep "python3 $robotPath" | grep -v "sudo" | grep -v "grep" | awk '{ print $2 }'`
	;;
  status)
	#status to see if robot is running or not
	pid=`ps -ef | grep "python3 $robotPath" | grep -v "sudo" | grep -v "grep" | awk '{ print $2 }'`
 	if [ $pid ]
	then
		echo "Robot is running with PID $pid"
	else
		echo "Robot is not running"
	fi
	;;
  reload|restart|force-reload)
        ;;
  *)
        echo "Usage: $N {start|stop|status}" >&2
        exit 1
        ;;
esac

exit 0