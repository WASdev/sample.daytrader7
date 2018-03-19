 # (C) Copyright IBM Corporation 2015.
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 # http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.
 

daytrader7.jmx is an Apache JMeter script that may be used for running the DayTrader7 benchmark.
daytrader7_mojarra.jmx is the same as daytrader7.jmx, but for use with Mojarra JSF implementations.

Jmeter version 3.3 or later is highly recommended.
To use the script, you will need to put the the WebSocket Sampler (and dependencies) from WebSocket Samplers by Peter Doornbosch into lib/ext. 
Use the Jmeter plugin manager or download via https://bitbucket.org/pjtr/jmeter-websocket-samplers.


The script has the following options:
	-JHOST	    The name of the machine running the DayTrader Application. The default is localhost.
	-JPORT	    The HTTP port of the server running the DayTrader Application. The default is 9082.
	-JPROTOCOL  The transport either http or https
				NOTE: The websocket plugin does not offer a variable substitution. See the WS note below.
	-JTHREADS   The number of jmeter threads to start. The default is 50.
	-JRAMP		The ramp up time for starting the threads. Set this to the same value as -JTHREADS for a smoother startup. The default is 0.
	-JDURATION  The time (in seconds) to run jmeter.
	-JMAXTHINKTIME The time in milliseconds to wait between each call. The default is 0 ms
	-JSTOCKS    The total amount of stocks/quotes in the database, minus one. The default is 9999, which assumes there are 10,000 stocks in the database.
	-JBOTUID    The lowest user id. The default is 0.
	-JTOPUID    The highest user id. The default is 14999, which assumes there are 15,000 users in the database.
	
WS NOTE: To enable encrypted WebSocket, either open daytrader7.jmx using the GUI and enable WSS on the WS2 and WS1 calls, or edit the daytrader.jmx file and change the TLS prop to true.

Example: ./jmeter -n -t daytrader7.jmx -JHOST=myserver -JPORT=9082 -JPROTOCOL=http -JMAXTHINKTIME=100 -JDURATION=300

To see output every five seconds from JMeter, edit the following section in <JMETER_HOME>/bin/jmeter.properties

#---------------------------------------------------------------------------
# Summariser - Generate Summary Results - configuration (mainly applies to non-GUI mode)
#---------------------------------------------------------------------------
#
# Define the following property to automatically start a summariser with that name
# (applies to non-GUI mode only)
summariser.name=summary
#
# interval between summaries (in seconds) default 30 seconds
summariser.interval=5
#
# Write messages to log file
summariser.log=true
#
# Write messages to System.out
summariser.out=true
