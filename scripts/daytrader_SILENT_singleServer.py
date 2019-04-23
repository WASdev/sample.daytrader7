import sys
import os

#-----------------------------------------------------------------
# WARNING: Jython/Python is extremely sensitive to indentation
# errors. Please ensure that tabs are configured appropriately
# for your editor of choice.
#-----------------------------------------------------------------

#-----------------------------------------------------------------
# daytrader_singleServer.py - DayTrader Single Server Install Script
#-----------------------------------------------------------------
#
# This script is designed to configure the JDBC and JMS resource required by
# the DayTrader application. Both single server and clustered environments are
# supported. A "silent install" option is also supported after manually setting
# the default config options in this file.
#  
# To invoke the script type:
#   wsadmin -f daytrader_singleServer.py [all|configure|cleanup|install|uninstall]
#      where:   all        -  configures JDBC and JMS resources and installs the app
#               configure  -  only configures the JDBC and JMS resource
#               cleanup    -  removes the JDBC and JMS resources
#               install    -  installs the DayTrader ear
#               uninstall  -  uninstalls the DayTrader ear
#
# If no parameters are specified, "all" is assumed!
#

print "daytrader_singleServer.py"

# Process the resource file containing all of the admin task definitions 
dir = os.getcwd()
resources = dir+os.sep+"resource_scripts.py"
execfile(resources)

# Edit this parameter to switch between Interactive and Silent installs
SilentInstall = "true"


#---------------------------------------------------------------------
# Default Properties for Silent Install
#
# Edit the variables in this section to perform a silent install. 
#---------------------------------------------------------------------

# Silent install properties for Managed Node
# - Modify these properties to specify the target node and server
#TargetNodeName =   "AppSrv01"
#TargetServerName = "server1"
# - Or uncomment the following lines to detect the server and node names
TargetNodeName =   getName(getNodeId(""))
TargetServerName = getName(getServerId(""))


# Security options
# Note: If global security is enabled or will be enabled at some point and
#   time, the AdminAuthAlias should be updated with a valid administrative
#   userid and password. In single-server configurations, this can be provided
#   by role-based auth (default), local OS auth, LDAP, etc. For cluster 
#   configurations, LDAP, Windows Active Directory or some other form of 
#   centralized authentication mechanism must be used to validate the userid.
SecurityEnabled = "false"
DefaultAdminUser =   "AdminUserID"
DefaultAdminPasswd = "password"

# JDBC provider options
# JDBC provider types include:
#   "DB2 Universal","DB2 iSeries (Toolbox)","DB2 iSeries (Native)","Derby","Oracle","Embedded MS SQL Server","Informix"
DefaultProviderType =   "DB2 Universal"
DefaultPathName =       "/opt/db2jars/db2jcc.jar;/opt/db2jars/db2jcc_license_cu.jar"
DefaultNativePathName = ""

# Datasource options
# Note: For Oracle, default port is 1521. For DB2, 50000.
DefaultDatabaseName = "tradedb"
DefaultHostname =     ""
DefaultPort =         "50000"
DefaultUser =         "db2inst1"
DefaultPasswd =       "passw0rd"

# Additional defaults for vendor specific Datasources
DefaultIfxLockMode =   "60"
DefaultIfxServerName = "ifxServerName"
DefaultOraclePort =    "1521"
DefaultDB2DriverType = "4"

# Deploy options
# Deploy types include:
#   "DB2UDB_V82","DB2UDBOS390_V8","DB2UDBISERIES_V54","DERBY_V10","MSSQLSERVER_2005","ORACLE_V10G","INFORMIX_V100"
DefaultEJBDeployType = "DB2UDB_V82"

# JMS Messaging Engine Datastore options
# Note: true - file store will be used
#       false - database data store will be used
DefaultMEFileStore = "true"
DefaultMEFileStoreLocation = "default" 


#---------------------------------------------------------------------
#  Misc options
#---------------------------------------------------------------------

CmdOptions =      ["all", "configure", "cleanup", "install", "uninstall"]
DefaultOptions =  ["yes", "no"]
BooleanOptions =  ["true", "false"]
ProviderOptions = ["DB2 Universal","DB2 iSeries (Toolbox)","DB2 iSeries (Native)","Derby","Oracle","Embedded MS SQL Server","Informix"]
DeployOptions =   ["DB2UDB_V82","DB2UDBOS390_V8","DB2UDBISERIES_V54","DERBY_V10","MSSQLSERVER_2005","ORACLE_V10G","INFORMIX_V100"]


#---------------------------------------------------------------------
# Application specific config information
#
# NOTE: This should NOT be modified!!!
#---------------------------------------------------------------------

DefaultTradeAppName = "DayTrader3"
DefaultEarFile =      "daytrader3.0.5-ee6-src.ear"

# Deployment options
DefaultRunEJBDeploy = "false"
DefaultRunWSDeploy =  "false"
DefaultBindings =     "true"
DefaultUseMetadata =  "true"

# JDBC Driver and DataSource Config Parameters
# Datasource properties
DefaultDatasourceName = "TradeDataSource"
DefaultDatasourceAuthAliasName =  "TradeDataSourceAuthData"
DefaultNoTxDatasourceName = "NoTxTradeDataSource"

DefaultStmtCacheSize =  60
DefaultXA = "false"

# JMS (Messaging) Config Parameters
# Global Security properties for JMS
DefaultAdminAuthAliasName = "TradeAdminAuthData"

#reliability = "ASSURED_PERSISTENT"
reliability = "EXPRESS_NONPERSISTENT"

#deliveryMode = "Persistent"
deliveryMode = "NonPersistent"

#durability = "Durable"
durability = "NonDurable"

# Queue/Topic Names
brokerSIBDest =  "TradeBrokerJSD"
topicSpace =     "Trade.Topic.Space"
brokerJMSQCF =   "TradeBrokerQCF"
streamerJMSTCF = "TradeStreamerTCF"
brokerQueue =    "TradeBrokerQueue"
streamerTopic =  "TradeStreamerTopic"
brokerMDB =      "TradeBrokerMDB"
streamerMDB =    "TradeStreamerMDB"


#---------------------------------------------------------------------
# Common JDBC Driver Paths 
#---------------------------------------------------------------------
# Note: wsadmin parses the command line based on ";" regardless of platform type
DB2WinJccPath =         "c:/sqllib/java/db2jcc.jar;c:/sqllib/java/db2jcc_license_cu.jar;"
DB2zSeriesNativePath =  "/usr/lpp/db2/db2810/jcc/lib"
DB2CliPath =            "c:/sqllib/java/db2java.zip"
OraclePath =            "c:/oracle/product/10.1.0/db_1/jdbc/lib/ojdbc14.jar"
DerbyPath =             "$\{WAS_INSTALL_ROOT\}/derby/lib/derby.jar"
DB2iSeriesNativePath =  "/QIBM/ProdData/Java400/ext/db2_classes.jar"
DB2iSeriesToolboxPath = "/QIBM/ProdData/HTTP/Public/jt400/lib/jt400.jar"




#---------------------------------------------------------------------
#  Basic App Administration Procedures
#---------------------------------------------------------------------


def printUsageAndExit ():
	print ""
	print "Usage: wsadmin -f daytrader_singleServer.py [all|configure|cleanup|install|uninstall]"
	print ""
	print "   where:  all        -  configures JDBC and JMS resources and installs the app"
	print "           configure  -  only configures the JDBC and JMS resource"
	print "           cleanup    -  removes the JDBC and JMS resources"
	print "           install    -  installs the DayTrader ear"
	print "           uninstall  -  uninstalls the DayTrader ear"
	print ""
	print "   If no parameters are specified, \"all\" is assumed!"
	print ""
	sys.exit()
#endDef 


#---------------------------------------------------------------------
#  Parse Command Line
#---------------------------------------------------------------------

if (len(sys.argv) == 0):
	operation = "all"
elif (sys.argv[0] in CmdOptions):
	operation = sys.argv[0]
else:
	printUsageAndExit( )
#endElse 

print ""
print "------------------------------------------------"
print " Daytrader Install/Configuration Script"
print ""
print " Operation:  " + operation
print " Silent:     " + SilentInstall
print "------------------------------------------------"

#---------------------------------------------------------------------
# Daytrader configuration procedures
#---------------------------------------------------------------------

scope = ""

if (SilentInstall == "false" and ( operation == "configure" or operation == "all") ):
	SecurityEnabled = getValidInput("Global security is (or will be) enabled (true|false) ["+SecurityEnabled+"]:", SecurityEnabled, BooleanOptions )

	# Obtain node name and id for scope
	print "------------------------------------------------"
	print " Collecting Single Server or Managed Server Info"
	print "" 
        
	node = getNodeId("")
	TargetNodeName = getName(node )
	scope = node

	server = getServerId("")
	TargetServerName = getName(server )

	print " Node:   " + TargetNodeName
	print " Server: " + TargetServerName
	print "------------------------------------------------"

	print ""
	print "------------------------------------------------"
	print " Collecting Database/Datasource Information"
	print "------------------------------------------------"

	print "JDBC provider options include the following:"
	for provider in ProviderOptions:
		print " " + provider
	#endFor
	DefaultProviderType = getValidInput("Select the JDBC provider type ["+DefaultProviderType+"]:", DefaultProviderType, ProviderOptions )

	print "Deploy options include the following:"
	for deploy in DeployOptions:
		print " " + deploy
	#endFor
	DefaultEJBDeployType = getValidInput("Select the EJB deployment target ["+DefaultEJBDeployType+"]:", DefaultEJBDeployType, DeployOptions)
       
	print "The JDBC driver class path provides the full path to all required jar files."
	print "Note: Use \";\" and \"/\" as path separators and delimiters."
	print ""
	print "DB2 Examples:"
	print "Windows:    C:/sqllib/java/db2jcc.jar;C:/sqllib/java/db2jcc_license_cu.jar"
	print "Unix/Linux: /home/db2inst1/sqllib/java/db2jcc.jar;/home/db2inst1/sqllib/java/db2jcc_license_cu.jar"
	
	DefaultPathName = getInput("Please enter the location of JDBC driver (jar) files:",DefaultPathName )

	if (DefaultEJBDeployType.find("OS390") > 0):
		DefaultNativePathName = getInput("Please enter the driver native library path:", DefaultNativePathName )
		DefaultXA = "false"
		DefaultDB2DriverType = "2"
	#endIf

	DefaultDatabaseName = getInput("Please enter the database name (location) ["+DefaultDatabaseName+"]:", DefaultDatabaseName )

	if (DefaultProviderType == "Oracle"):
		DefaultPort = DefaultOraclePort
	#endIf

	if (DefaultProviderType != "Derby" or DefaultProviderType != "DB2 iSeries (Native)"):
		DefaultHostname = getInput("Please enter the database hostname ["+DefaultHostname+"]:", DefaultHostname )
		DefaultPort = getInput("Please enter the database port number ["+DefaultPort+"]:", DefaultPort )
	#endIf

	if (DefaultProviderType == "Informix"):
		DefaultIfxServerName = getInput("Please enter the Informix server name ["+DefaultIfxServerName+"]:", DefaultIfxServerName)
		DefaultIfxLockMode = getInput("Please enter the Informix lock mode wait value ["+DefaultIfxLockMode+"]:", DefaultIfxLockMode)
	#endIf

	if (DefaultProviderType != "Derby"):
		DefaultUser = getInput("Please enter the database username ["+DefaultUser+"]:", DefaultUser )
		DefaultPasswd = getInput("Please enter the database password ["+DefaultPasswd+"]:", DefaultPasswd )
	#endIf 

	print ""
	print "------------------------------------------------"
	print " Collecting JMS Provider Information"
	print "------------------------------------------------"

	DefaultMEFileStore = getValidInput("Use file store for JMS Provder ["+DefaultMEFileStore+"]:", DefaultMEFileStore, BooleanOptions )
	
	if (DefaultMEFileStore == "true"):
		DefaultMEFileStoreLocation = getInput("ME file store location ["+DefaultMEFileStoreLocation+"]:", DefaultMEFileStoreLocation)
	#endIf

	if (SecurityEnabled == "true"):
		print "-------------------------------------------------"
		print " Collecting Security Information for JMS"
		print " "
		print " Note: The supplied authentication data must"
		print "  correspond to a valid administrative username"
		print "  and password."
		print "-------------------------------------------------"

		DefaultAdminUser = getInput("Please enter a valid administrative username ["+DefaultAdminUser+"]:", DefaultAdminUser )
		DefaultAdminPasswd = getInput("Please enter a valid administrative password ["+DefaultAdminPasswd+"]:", DefaultAdminPasswd )
	#endIf
#endIf 

if (operation == "all" or operation == "configure"):
	# Create the JDBC/Datasource config objects
	
	if (scope == ""):
		#scope = AdminConfig.getid("/Node:"+TargetNodeName+"/Server:"+TargetServerName+"/")
		# By default, we normally use Node scope
		scope = AdminConfig.getid("/Node:"+TargetNodeName+"/")
	#endIf

	print ""
	print "------------------------------------------------"
	print " Configuring JDBC/Datasource Resources"
	print " Scope: "+scope
	print "------------------------------------------------"

	createJAASAuthData(DefaultDatasourceAuthAliasName, DefaultUser, DefaultPasswd )

	provider = createJDBCProvider(DefaultProviderType, DefaultXA, scope, DefaultPathName, DefaultNativePathName )

	datasource = createDatasource(DefaultDatasourceName, "jdbc/"+DefaultDatasourceName, DefaultStmtCacheSize, DefaultDatasourceAuthAliasName, provider)
	noTxDatasource = createDatasource(DefaultNoTxDatasourceName, "jdbc/"+DefaultNoTxDatasourceName, 10, DefaultDatasourceAuthAliasName, provider)
	addDatasourceProperty(noTxDatasource, "nonTransactionalDataSource", "true")

	if (DefaultProviderType.find("DB2") >= 0 or DefaultProviderType == "Derby"):
		updateDB2orDerbyDatasource(datasource, DefaultDatabaseName, DefaultHostname, DefaultPort, DefaultDB2DriverType)
		updateDB2orDerbyDatasource(noTxDatasource, DefaultDatabaseName, DefaultHostname, DefaultPort, DefaultDB2DriverType)
	elif (DefaultProviderType == "Oracle"):
		updateOracleDatasource(datasource, DefaultDatabaseName, DefaultHostname, DefaultPort)
		updateOracleDatasource(noTxDatasource, DefaultDatabaseName, DefaultHostname, DefaultPort)		
	elif (DefaultProviderType == "Informix"):
		updateInformixDatasource(datasource, DefaultDatabaseName, DefaultIfxServerName, DefaultPort, DefaultHostname, DefaultIfxLockMode)
		updateInformixDatasource(noTxDatasource, DefaultDatabaseName, DefaultIfxServerName, DefaultPort, DefaultHostname, DefaultIfxLockMode)
	elif (DefaultProviderType == "Embedded MS SQL Server"):
		print "Not yet supported"
		sys.exit()
	#endIf

	print ""
	print "------------------------------------------------"
	print " JDBC Resource Configuration Completed!!!"
	print "------------------------------------------------"

	# Create the JMS config objects

	print ""
	print "------------------------------------------------"
	print " Configuring JMS Resources"
	print " Scope: "+scope
	print "------------------------------------------------"

	createJAASAuthData(DefaultAdminAuthAliasName, DefaultAdminUser, DefaultAdminPasswd )

	sibus = createSIBus(getName(scope ), DefaultAdminAuthAliasName )
	fileStore = [DefaultMEFileStore, DefaultMEFileStoreLocation]
	target = [TargetNodeName, TargetServerName]
	dsParms = ["true", "dummy"]
	addSIBusMember(sibus, fileStore, target, dsParms)

	if (SecurityEnabled == "true"):
		createSIBusSecurityRole(sibus, DefaultAdminUser )
	#endIf 

	# Create the Trade Broker Queue and Trade TopicSpace Destinations

	createSIBDestination(sibus, brokerSIBDest, "Queue", reliability, target )
	createSIBDestination(sibus, topicSpace, "TopicSpace", reliability, [] )

	createJMSConnectionFactory(sibus, brokerJMSQCF, "Queue", "jms/"+brokerJMSQCF, DefaultAdminAuthAliasName, scope )
	createJMSConnectionFactory(sibus, streamerJMSTCF, "Topic", "jms/"+streamerJMSTCF, DefaultAdminAuthAliasName, scope )

	createJMSQueue(brokerQueue, "jms/"+brokerQueue, brokerSIBDest, deliveryMode, scope )
	createJMSTopic(streamerTopic, "jms/"+streamerTopic, topicSpace, deliveryMode, scope )

	createMDBActivationSpec(brokerMDB, "eis/"+brokerMDB, sibus, "jms/"+brokerQueue, "javax.jms.Queue", DefaultAdminAuthAliasName, scope, durability )
	createMDBActivationSpec(streamerMDB, "eis/"+streamerMDB, sibus, "jms/"+streamerTopic, "javax.jms.Topic", DefaultAdminAuthAliasName, scope, durability )

	print ""
	print "------------------------------------------------"
	print " JMS Resource Configuration Completed!!!"
	print "------------------------------------------------"

	print ""
	print "Saving..."
	AdminConfig.save( )
#endIf 


#---------------------------------------------------------------------
# Daytrader install procedures
#---------------------------------------------------------------------

if (operation == "all" or operation == "install"):
	print " "
	print "------------------------------------------------"
	print " Installing DayTrader"
	print "------------------------------------------------"

	if (SilentInstall == "false" and operation == "install"):
		TargetNodeName = getName(getNodeId(""))
		TargetServerName = getName(getServerId(""))
        
		#print "Deploy options include the following:"
		#for deploy in DeployOptions:
		#	print " " + deploy
		##endFor
		#DefaultEJBDeployType = getValidInput("Select the EJB deployment target ["+DefaultEJBDeployType+"]:", DefaultEJBDeployType, DeployOptions)
	#endIf 

	target = [TargetNodeName, TargetServerName]

	installApp(DefaultTradeAppName, DefaultEarFile, DefaultRunEJBDeploy, DefaultRunWSDeploy, DefaultBindings, DefaultUseMetadata, DefaultEJBDeployType, target )

	print ""
	print "------------------------------------------------"
	print " DayTrader Installation Completed!!!"
	print "------------------------------------------------"

	print ""
	print "Saving..."
	AdminConfig.save( )
#endIf

if (operation == "uninstall"):
	print " "
	print "------------------------------------------------"
	print " Uninstalling DayTrader"
	print "------------------------------------------------"

	uninstallApp(DefaultTradeAppName)

	print ""
	print "------------------------------------------------"
	print " DayTrader Uninstall Completed!!!"
	print "------------------------------------------------"

	print ""
	print "Saving..."
	AdminConfig.save( )
#endIf

if (operation == "cleanup"):
	print " "
	print "------------------------------------------------"
	print " Uninstalling JMS Resources"
	print "------------------------------------------------"

	deleteMDBActicationSpec(brokerMDB)
	deleteMDBActicationSpec(streamerMDB)

	deleteJMSQueue(brokerQueue)
	deleteJMSTopic(streamerTopic)

	deleteJMSConnectionFactory(brokerJMSQCF)
	deleteJMSConnectionFactory(streamerJMSTCF)

	deleteSIBDestination(brokerSIBDest)
	deleteSIBDestination(topicSpace)

	deleteSIBus(getName(getNodeId("")))

	removeJAASAuthData(DefaultAdminAuthAliasName)

	print " "
	print "------------------------------------------------"
	print " Uninstalling JDBC Resources"
	print "------------------------------------------------"

	removeDatasource(DefaultDatasourceName)
	removeDatasource(DefaultNoTxDatasourceName)
	removeJAASAuthData(DefaultDatasourceAuthAliasName)

	print ""
	print "------------------------------------------------"
	print " DayTrader Resource Cleanup Completed!!!"
	print "------------------------------------------------"

	print ""
	print "Saving..."
	AdminConfig.save( )
#endIf

print ""
print "Saving config..."
AdminConfig.save( )


