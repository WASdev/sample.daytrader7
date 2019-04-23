#--------------------------------------------------------------------
# WebSphere Tuning Script for DayTrader
#--------------------------------------------------------------------
#
# This script is designed to modify some of the most common
# WebSphere configuration parameters and tuning knobs.
# In order to tune the config parameters, simply change the values
# provided below. This script assumes that all server names in a
# cluster configuration are unique.
#
# To invoke the script, type:
#   wsadmin -f tuneDayTrader.py <scope> <id>
#      scope      - 'cluster' or 'server'
#      id         - name of target object within scope (ie. servername)
#
# Examples:
#   wsadmin -f tuneDayTrader.py server server1
#
#   wsadmin -f tuneDayTrader.py cluster TradeCluster
#
#
#--------------------------------------------------------------------

AdminConfig.setValidationLevel("NONE" )
from sys import registry

print "Starting script..."
print "Reading config parameters..."

#--------------------------------------------------------------------
# COMMON CONFIG PARAMETERS
# - Adjust these parameters based on the intended target system
#--------------------------------------------------------------------

# ORB properties (false)
noLocalCopies = "true"

# ORB Thread Pool (10,50) - For split-tier configurations
minOrbPool = 10
maxOrbPool = 50

# WebContainer Thread Pool (false, 10,50)
enableServletCache = "false"
minWebPool = 100
maxWebPool = 100

# Default Thread Pool (5,20)
minDefaultPool = 5
maxDefaultPool = 20

# HTTP KeepAlive settings (true, 100)
keepAliveEnabled = "true"
maxPersistentRequests = -1

# JVM properties
# Note: OS specific changes to the heap size settings are located
#  in the next section -> "Base OS Specific JVM settings". Changes
#  to the generic JVM arguments are handled below.
minHeap = 2560
maxHeap = 2560
verboseGC = "false"
genericArgs = "-Xss128k -Xmso128K -Xnoloa -Xmn1280m -Xgcthreads6 -Xdisableexplicitgc -Xtrace:none -Xlp -Xaggressive -XtlhPrefetch -Xcodecache14m -Xshareclasses:none -Xnodfpbd -Xnocompactgc -Xgc:noconcurrentmark -Xnoclassgc"

# OS Specific JVM options
IBMJDKoptions = ""
SUNJDKoptions = "-XX:+UseTLAB -Xnoclassgc -XX:MaxPermSize=64m -Xmn256m -XX:SurvivorRatio=16"
HPJDKoptions = "-Xmn512m -XX:PermSize=80m -XX:+ForceMmapReserved -XX:SurvivorRatio=16 -Xoptgc -XX:+UseParallelGC -Djava.nio.channels.spi.SelectorProvider=sun.nio.ch.DevPollSelectorProvider -XX:-ExtraPollBeforeRead -XX:+UseSpinning"
ISeriesJDKoptions = "-Djava.compiler=jitc"

# SystemOut and SystemErr log rollover type (SIZE)
rollover = "NONE"

# TraceService settings {"*=all=disabled",20,1}
#traceSpec = "*=all=disabled"
traceSpec = "*=info"
traceRolloverSize = 100
maxFiles = 10

# Java2 Security (false for 5.1 and true for 6.0)
j2Security = "false"

# PMI service
PMIstatus = "false"

# TradeDataSource config properies (10, 1,10)
statementCache = 60
minTradeDSPool = maxWebPool + maxDefaultPool
maxTradeDSPool = maxWebPool + maxDefaultPool

# TradeBrokerQCF config properties (1,10)
minBrokerPool = 1
maxBrokerPool = maxDefaultPool

# TradeStreamerTCF config properties (1,10)
minStreamerPool = 1
maxStreamerPool = maxDefaultPool

# Uninstall default applications
# Possibly uninstall applications - DefaultApplication, ivtApp
uninstallApps = "true"
uninstallList = ["ivtApp", "DefaultApplication", "query"]

#---------------------------------------------------------------------
# Base OS Specific JVM settings
#---------------------------------------------------------------------

os = registry.getProperty("os.name")

if (os.find("Windows") > -1):
        genericArgs = genericArgs + IBMJDKoptions
elif (os.find("AIX") > -1):
        genericArgs = genericArgs + IBMJDKoptions
elif (os.find("Linux") > -1):
        genericArgs = genericArgs + IBMJDKoptions
elif (os.find("SunOS") > -1):
        genericArgs = genericArgs + SUNJDKoptions
elif (os.find("HP-UX") > -1):
        genericArgs = genericArgs + HPJDKoptions
elif (os.find("z/OS") > -1):
        genericArgs = genericArgs + IBMJDKoptions
        minHeap = 768
        maxHeap = 768
elif (os.find("OS/400") > -1):
        genericArgs = genericArgs + ISerisJDKoptions
        maxHeap = 0
#endIf


#---------------------------------------------
# Check/Print Usage
#---------------------------------------------

def printUsageAndExit (  ):
        print " "
        print "Usage: wsadmin -f tuneTrade.jacl <cluster | server> <name>"
        sys.exit()
#endDef 

#---------------------------------------------
# Misc Procedures
#---------------------------------------------

def getName (objectId):
        endIndex = (objectId.find("(c") - 1)
        stIndex = 0
        if (objectId.find("\"") == 0):
                stIndex = 1
        #endIf
        return objectId[stIndex:endIndex+1]
#endDef

#---------------------------------------------
# Parse command line arguments
#---------------------------------------------

print "Parsing command line arguments..."

if (len(sys.argv) < 2):
        printUsageAndExit( )
else:
        scope = sys.argv[0]
        print "Scope:   "+`scope`

        if (scope == "cluster"):
                clustername = sys.argv[1]
                print "Cluster: "+clustername
        elif (scope == "server"):
                servername = sys.argv[1]
                print "Server:  "+servername
        else:
                print "Error: Invalid Argument ("+scope+")"
                printUsageAndExit( )
        #endElse 
#endElse 

#---------------------------------------------
# Obtain server list
#---------------------------------------------

print ""
print "Obtaining server list..."

serverList = []
if (scope == "cluster"):
        cluster = AdminConfig.getid("/ServerCluster:"+clustername+"/" )
        memberList = AdminConfig.showAttribute(cluster, "members" )
        for member in memberList[1:-1].split(" "):
                member = member.rstrip()
                memberName = getName(member )
                serverList.append(AdminConfig.getid("/Server:"+memberName+"/" ))
        #endFor 
else:
        server = AdminConfig.getid("/Server:"+servername+"/" )
        serverList.append(server)
#endElse 

#---------------------------------------------
# Print config properties
#---------------------------------------------

print ""
print "WebSphere configuration"
print "-----------------------"
print ""
print "   Enforce Java2 Security:      "+j2Security+" "
print ""

print "Servers:"
for server in serverList:
        print "   " + getName(server)
#endFor 
print ""
print " EJB/ORB ----------------------------------------"
print "   NoLocalCopies:               "+noLocalCopies
print "   Min ORB Pool Size:           "+str(minOrbPool)
print "   Max ORB Pool Size:           "+str(maxOrbPool)
print " Web --------------------------------------------"
print "   Enable Servlet Cache:        "+enableServletCache
print "   Min WebContainer Pool Size:  "+str(minWebPool)
print "   Max WebContainer Pool Size:  "+str(maxWebPool)
print " Default (JMS) Thread Pool ----------------------"
print "   Min Default Pool Size:       "+str(minDefaultPool)
print "   Max Default Pool Size:       "+str(maxDefaultPool)
print " HTTP Inbound Channel ---------------------------"
print "   Keepalives Enabled:          "+keepAliveEnabled
print "   Maximum Persistent Requests: "+str(maxPersistentRequests)
print " JVM --------------------------------------------"
print "   Min JVM Heap Size:           "+str(minHeap)
print "   Max JVM Heap Size:           "+str(maxHeap)
print "   Verbose GC:                  "+verboseGC
print "   Generic JVM Arguments:  "
print "      "+genericArgs
print " Logging ----------------------------------------"
print "   System Log Rollover Type:    "+rollover
print "   Trace Specification:         "+traceSpec
print "   Rollover Size:               "+str(traceRolloverSize)
print "   Max Backup Files:            "+str(maxFiles)
print " Misc -------------------------------------------"
print "   Enable PMI Service:          "+PMIstatus
print ""
print "   Uninstall default apps:      "+uninstallApps
print ""
print " TradeDataSource Config -------------------------"
print "   Statement Cache Size:        "+str(statementCache)
print "   Min Connection Pool Size:    "+str(minTradeDSPool)
print "   Max Connection Pool Size:    "+str(maxTradeDSPool)
print " TradeBrokerQCF Config --------------------------"
print "   Min Connection Pool Size:    "+str(minBrokerPool)
print "   Max Connection Pool Size:    "+str(maxBrokerPool)
print " TradeStreamerTCF Config --------------------------"
print "   Min Connection Pool Size:    "+str(minStreamerPool)
print "   Max Connection Pool Size:    "+str(maxStreamerPool)
print ""

#---------------------------------------------
# Modify cell parameters
#---------------------------------------------

# Accessing cell based security config
print "Accessing security configuration..."
sec = AdminConfig.list("Security" )
attrs = [["enforceJava2Security", j2Security]]
print "Updating security..."
AdminConfig.modify(sec, attrs )


#---------------------------------------------
# Modify server parameters
#---------------------------------------------

for server in serverList:
        servername = getName(server )
        print ""
        print "Server: "+servername
        print ""

        # Accessing orb config
        print "Accessing ORB configuration..."
        orb = AdminConfig.list("ObjectRequestBroker", server )
        print "ORB noLocalCopies (old/new):              "+AdminConfig.showAttribute(orb,"noLocalCopies")+"/"+noLocalCopies
        attrs = [["noLocalCopies", noLocalCopies]]
        orbPool = AdminConfig.showAttribute(orb, "threadPool" )
        print "ThreadPool MaxSize (old/new):             "+AdminConfig.showAttribute(orbPool, "maximumSize")+"/"+str(maxOrbPool)
        print "ThreadPool MinSize (old/new):             "+AdminConfig.showAttribute(orbPool, "minimumSize")+"/"+str(minOrbPool)
        attrs2 = [["maximumSize", maxOrbPool], ["minimumSize", minOrbPool]]
        print "Updating ORB..."
        print " "
        AdminConfig.modify(orb, attrs )
        AdminConfig.modify(orbPool, attrs2 )

        # Accessing web container thread pool config
        print "Accessing web container configuration..."
        webCont = AdminConfig.list("WebContainer", server )
        print "Enable Servlet Caching (old/new):         "+AdminConfig.showAttribute(webCont, "enableServletCaching")+"/"+enableServletCache
        attrs = [["enableServletCaching", enableServletCache]]

        tpList = AdminConfig.list("ThreadPool", server )
        webPool = ""
        for pool in tpList.split("\n"):
            pool = pool.rstrip()
            if (getName(pool) == "WebContainer"):
                webPool = pool
                break
                #endIf
        #endFor
        print "ThreadPool MaxSize (old/new):             "+AdminConfig.showAttribute(webPool, "maximumSize")+"/"+str(maxWebPool)
        print "ThreadPool MinSize (old/new):             "+AdminConfig.showAttribute(webPool, "minimumSize")+"/"+str(minWebPool)
        attrs2 = [["maximumSize", maxWebPool], ["minimumSize", minWebPool]]
        print "Updating web container..."
        print " "
        AdminConfig.modify(webCont, attrs)
        AdminConfig.modify(webPool, attrs2 )

        # Accessing web container thread pool config
        print "Accessing default thread pool configuration..."
        tpList = AdminConfig.list("ThreadPool", server )
        defaultPool = ""
        for pool in tpList.split("\n"):
            pool = pool.rstrip()
            if (getName(pool) == "Default"):
                defaultPool = pool
                break
                #endIf
        #endFor
        print "ThreadPool MaxSize (old/new):             "+AdminConfig.showAttribute(defaultPool, "maximumSize")+"/"+str(maxDefaultPool)
        print "ThreadPool MinSize (old/new):             "+AdminConfig.showAttribute(defaultPool, "minimumSize")+"/"+str(minDefaultPool)
        attrs = [["maximumSize", maxDefaultPool], ["minimumSize", minDefaultPool]]
        print "Updating web container thread pool..."
        print " "
        AdminConfig.modify(defaultPool, attrs )

        # Accessing HTTP keepalive config
        print "Accessing HTTP KeepAlive configuration..."
        HTTPInbound = AdminConfig.list("HTTPInboundChannel", server )
        http2 = ""

        for inbound in HTTPInbound.split("\n"):
            inbound = inbound.rstrip()
            if (getName(inbound) == "HTTP_2"):
                http2 = inbound
                break
            #endIf
        #endFor
        print "KeepAlive Enabled (old/new):        "+AdminConfig.showAttribute(http2,"keepAlive")+"/"+keepAliveEnabled
        print "Max Persistent Requests (old/new):  "+AdminConfig.showAttribute(http2,"maximumPersistentRequests")+"/"+str(maxPersistentRequests)
        attrs = [["keepAlive", keepAliveEnabled], ["maximumPersistentRequests", maxPersistentRequests]]
        print "Updating HTTP KeepAlives..."
        print " "
        AdminConfig.modify(http2, attrs )

        # Accessing JVM config
        print "Accessing JVM configuration..."
        jvm = AdminConfig.list("JavaVirtualMachine", server )
        print "Initial Heap Size (old/new):  "+AdminConfig.showAttribute(jvm, "initialHeapSize")+"/"+str(minHeap)
        print "Maximum Heap Size (old/new):  "+AdminConfig.showAttribute(jvm, "maximumHeapSize")+"/"+str(maxHeap)
        print "VerboseGC Enabled (old/new):  "+AdminConfig.showAttribute(jvm, "verboseModeGarbageCollection")+"/"+verboseGC
        print "Generic Arguments (old/new):  "+AdminConfig.showAttribute(jvm, "genericJvmArguments")+"/"+genericArgs
        attrs = [["initialHeapSize", minHeap], ["maximumHeapSize", maxHeap], ["verboseModeGarbageCollection", verboseGC], ["genericJvmArguments", genericArgs]]
        print "Updating JVM..."
        print " "
        AdminConfig.modify(jvm, attrs )

        # Accessing System log file config
        print "Accessing System log file configuration..."
        logList = AdminConfig.list("StreamRedirect", server )

        for log in logList.split("\n"):
            log = log.rstrip()
            print AdminConfig.showAttribute(log,"fileName")+" Rollover Type (old/new):  "+AdminConfig.showAttribute(log,"rolloverType")+"/"+rollover
            attrs = [["rolloverType", rollover]]
            print "Updating logs..."
            print " "
            AdminConfig.modify(log, attrs )
        #endFor 

        # Accessing Trace Service config
        print "Accessing Trace Service configuration..."
        traceService = AdminConfig.list("TraceService", server )
        traceLog = AdminConfig.showAttribute(traceService, "traceLog" )
        print "Trace Spec (old/new):          "+AdminConfig.showAttribute(traceService, "startupTraceSpecification")+"/"+traceSpec
        print "Rollover File Size (old/new):  "+AdminConfig.showAttribute(traceLog, "rolloverSize")+"/"+str(traceRolloverSize)
        print "Max Backup Files (old/new):    "+AdminConfig.showAttribute(traceLog, "maxNumberOfBackupFiles")+"/"+str(maxFiles)
        attrs = [["startupTraceSpecification", traceSpec]]
        attrs2 = [["rolloverSize", traceRolloverSize], ["maxNumberOfBackupFiles", maxFiles]]
        print "Updating Trace Service..."
        print " "
        AdminConfig.modify(traceService, attrs )
        AdminConfig.modify(traceLog, attrs2 )

        # Accessing PMI service config
        print "Accessing PMI service configuration..."
        pmi = AdminConfig.list("PMIService", server )
        print "Enable (old/new):  "+AdminConfig.showAttribute(pmi, "enable")+"/"+PMIstatus
        attrs = [["enable", PMIstatus]]
        print "Updating PMI..."
        print " "
        AdminConfig.modify(pmi, attrs )

        # Accessing TradeDataSource config
        print "Accessing TradeDataSource configuration..."
        tradeDS = AdminConfig.getid("/DataSource:TradeDataSource/")
        print "Statement Cache Size (old/new):  "+AdminConfig.showAttribute(tradeDS, "statementCacheSize")+"/"+str(statementCache)
        attrs = [["statementCacheSize", statementCache]]
        connPool = AdminConfig.showAttribute(tradeDS, "connectionPool")
        print "Connection Pool MaxSize (old/new):             "+AdminConfig.showAttribute(connPool, "maxConnections")+"/"+str(maxTradeDSPool)
        print "Connection Pool MinSize (old/new):             "+AdminConfig.showAttribute(connPool, "minConnections")+"/"+str(minTradeDSPool)
        attrs2 = [["maxConnections", maxTradeDSPool], ["minConnections", minTradeDSPool]]
        print "Updateing TradeDataSource..."
        print " "
        AdminConfig.modify(tradeDS, attrs)
        AdminConfig.modify(connPool, attrs2)

        # Accessing TradeBrokerQCF config
        print "Accessing TradeBrokerQCF configuration..."
        brokerQCF = AdminConfig.getid("/ConnectionFactory:TradeBrokerQCF/")
        connPool = AdminConfig.showAttribute(brokerQCF, "connectionPool")
        print "Connection Pool MaxSize (old/new):             "+AdminConfig.showAttribute(connPool, "maxConnections")+"/"+str(maxBrokerPool)
        print "Connection Pool MinSize (old/new):             "+AdminConfig.showAttribute(connPool, "minConnections")+"/"+str(minBrokerPool)
        attrs = [["maxConnections", maxBrokerPool], ["minConnections", minBrokerPool]]
        print "Updateing TradeBrokerQCF..."
        print " "
        AdminConfig.modify(connPool, attrs)

        # Accessing TradeStreamerTCF config
        print "Accessing TradeStreamerTCF configuration..."
        streamerTCF = AdminConfig.getid("/ConnectionFactory:TradeStreamerTCF/")
        connPool = AdminConfig.showAttribute(streamerTCF, "connectionPool")
        print "Connection Pool MaxSize (old/new):             "+AdminConfig.showAttribute(connPool, "maxConnections")+"/"+str(maxStreamerPool)
        print "Connection Pool MinSize (old/new):             "+AdminConfig.showAttribute(connPool, "minConnections")+"/"+str(minStreamerPool)
        attrs = [["maxConnections", maxStreamerPool], ["minConnections", minStreamerPool]]
        print "Updateing TradeStreamerTCF..."
        print " "
        AdminConfig.modify(connPool, attrs)

        # Uninstalling default applications
        # Possibly uninstall applications - DefaultApplication, ivtApp, UDDIRegistry, ManagementEJB
        if (uninstallApps):
                print "Uninstalling default applications..."
                appList = AdminApp.list( )
                for app in appList:
                        if (app in uninstallList):
                                print "Removing application "+app+"..."
                                AdminApp.uninstall(app )
                        #endIf 
                #endFor 
        #endIf 
#endFor 

print ""
print "Script completed..."
print "Saving config..."

AdminConfig.save( )
