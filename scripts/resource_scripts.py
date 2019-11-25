import sys
import re
import sre
global AdminConfig

#-----------------------------------------------------------------
# WARNING: Jython/Python is extremly sensitive to indentation
# errors. Please ensure that tabs are configured appropriately
# for your editor of choice.
#-----------------------------------------------------------------

#-----------------------------------------------------------------
# getInput - Obtain generic input from the user. If default value
#            provided, return default value if nothing is entered.
#-----------------------------------------------------------------
def getInput (prompt, defaultValue):
	print ""
	print prompt
	retValue = sys.stdin.readline().strip() 
	if (retValue == ""):
		retValue = defaultValue
	#endIf

	return retValue
#endDef

#-----------------------------------------------------------------
# getValidInput - Obtain valid input from the user based on list of
#            valid options. Continue to query user if the invalid
#            options are entered. Return default value if nothing
#            is entered.
#-----------------------------------------------------------------
def getValidInput (prompt, defaultValue, validOptions):
	validate = 1     

	while (validate):
		print ""
		print prompt
		retValue = sys.stdin.readline().strip()

		if (retValue == ""):
			retValue = defaultValue
			validate = 0
		#endIf
                
		if (validate and validOptions.count(retValue) > 0):
			# Is retValue one of the valid options
			validate = 0
		#endIf
	#endWhile

	return retValue
#endDef

#-----------------------------------------------------------------
# getName - Return the base name of the config object.
#-----------------------------------------------------------------
def getName (objectId):
	endIndex = (objectId.find("(c") - 1)
	stIndex = 0
	if (objectId.find("\"") == 0):
		stIndex = 1
	#endIf
	return objectId[stIndex:endIndex+1]
#endDef


#-----------------------------------------------------------------
# getCellId - Return the cell id. It is assumed that only one cell
#            exists.
#-----------------------------------------------------------------
def getCellId ():
	cell = AdminConfig.list("Cell").split("\n")
	if (len(cell) != 1):
		print "Cell is not available.  This script assumes that there is one and only one cell available."
		print "Exiting..."
		sys.exit()
	#endIf

	return cell[0]
#endDef

#-----------------------------------------------------------------
# getNodeId - Return the node id of the existing node if in a single
#           server environment. If in an ND environment query the
#           user to determine desired node.
#-----------------------------------------------------------------
def getNodeId (prompt):
	nodeList = AdminConfig.list("Node").split("\n")

	if (len(nodeList) == 1):
		node = nodeList[0]
	else:
		print ""
		print "Available Nodes:"
                
		nodeNameList = []

		for item in nodeList:
			item = item.rstrip()
			name = getName(item) 

			nodeNameList.append(name)
			print "   " + name
		#endFor

		DefaultNode = nodeNameList[0]
		if (prompt == ""):
			prompt = "Select the desired node"
		#endIf

		nodeName = getValidInput(prompt+" ["+DefaultNode+"]:", DefaultNode, nodeNameList )

		index = nodeNameList.index(nodeName)
		node = nodeList[index]
	#endElse

	return node
#endDef

#-----------------------------------------------------------------
# getServerId - Return the server id of the existing server if
#           in a single server environment. If in an ND environment
#           query the user to determine desired server.
#-----------------------------------------------------------------
def getServerId (prompt):
	serverList = AdminConfig.list("Server").split("\n")

	if (len(serverList) == 1):
		server = serverList[0]
	else:
		print ""
		print "Available Servers:"
		
		serverNameList = []                

		for item in serverList:
			item = item.rstrip()
			name = getName(item)

			serverNameList.append(name)
			print "   " + name
		#endFor

		DefaultServer = serverNameList[0]
		if (prompt == ""):
			prompt = "Select the desired server"
		#endIf                
		serverName = getValidInput(prompt+" ["+DefaultServer+"]:", DefaultServer, serverNameList )

		index = serverNameList.index(serverName)
		server = serverList[index]
	#endElse

	return server
#endDef

#-----------------------------------------------------------------
# getServer1Id - Return the id for server1 if it exists
#-----------------------------------------------------------------
def getServer1Id ():
	serverList = AdminConfig.getid("/Server:server1/").split("\n")

	if (len(serverList) != 1):
		print "More than one default server (server1) available."
		print "Exiting..."
		sys.exit()
	#endIf

	return serverList[0]
#endDef

#-----------------------------------------------------------------
# getNodeIdFromServerId - Return the node id based on the node
#            name found within the server id
#-----------------------------------------------------------------
def getNodeIdFromServerId (serverId):
	nodeName = serverId.split("/")[3]

	return AdminConfig.getid("/Node:" + nodeName + "/")
#endDef

#-----------------------------------------------------------------
# createJAASAuthData - Create a new JAAS Authentication Alias if
#            one with the same name does not exist. Otherwise,
#            return the existing Authentication Alias.
#-----------------------------------------------------------------
def createJAASAuthData ( aliasName, user, passwd ):
	print " "
	print "Creating JAAS AuthData " + aliasName + "..."

	# Check if aliasName already exists
	authDataAlias = ""
	authList = AdminConfig.list("JAASAuthData" )
	if (len(authList) > 0):
		for item in authList.split("\n"):
			item = item.rstrip()
			alias = AdminConfig.showAttribute(item, "alias" )
			if (alias == aliasName):
				authDataAlias = item
				break
			#endIf
		#endFor
	#endIf

	# If authAlias does not exist, create a new one

	if (authDataAlias == ""):
		print "  Alias Name: " + aliasName
		print "  User:       " + user
		print "  Password:   " + passwd

		attrs = AdminConfig.list("Security")
		attrs0 = [["alias", aliasName], ["userId", user], ["password", passwd]]
                
		authDataAlias = AdminConfig.create("JAASAuthData", attrs, attrs0)
                
		print aliasName + " created successfully!"
	else:
		print aliasName + " already exists!"
	#endElse

	return authDataAlias
#endDef

def removeJAASAuthData (name):
	print " "
	print "Removing JAAS AuthData " + name + "..."

	authList = AdminConfig.list("JAASAuthData")
	auth = ""
	if (len(authList) > 0):
		for item in authList.split("\n"):
			item = item.rstrip()
			ident = AdminConfig.showAttribute(item.rstrip(), "alias" )
			if (ident == name):
				auth = item
				break
			#endIf
		#endFor
	#endIf

	if (auth != ""):
		AdminConfig.remove(auth)
		print name + " removed successfully!"
	else:
		print name + " not found!"
	#endElse
#endDef


#-----------------------------------------------------------------
# createJDBCProvider - Create a new JDBC Provider if one with the
#            same name does not exist in the specified scope. Otherwise,
#            return the existing JDBCProvider. The 3 types or providers
#            currently supported include DB2 JCC, DB2 CLI, and Oracle.
#-----------------------------------------------------------------
def createJDBCProvider (provider, XA, scopeId, path, nativePath):
	
	XA = XA.lower()

	if (provider == "DB2 Universal"):
		name = "DB2 Universal JDBC Driver Provider Only"
		if (XA == "true"):
			name = "DB2 Universal JDBC Driver Provider Only (XA)"
		#endIf
	elif (provider == "DB2 iSeries (Toolbox)"):
		name = "DB2 UDB for iSeries Provider Only (Toolbox)"
		if (XA == "true"):
			name = "DB2 UDB for iSeries Provider Only (Toolbox XA)"
		#endIf
	elif (provider == "DB2 iSeries (Native)"):
		name = "DB2 UDB for iSeries Provider Only (Native)"
		if (XA == "true"):
			name = "DB2 UDB for iSeries Provider Only (Native XA)"
		#endIf
	elif (provider == "DB2 for zOS Local"):
		name = "DB2 for zOS Local JDBC Provider Only (RRS)"
	elif (provider == "Derby"):
		name = "Derby JDBC Provider Only"
		if (XA == "true"):
			name = "Derby JDBC Provider Only (XA)"
		#endIf
	elif (provider == "Oracle"):
		name = "Oracle JDBC Driver Provider Only "
		if (XA == "true"):
			name = "Oracle JDBC Driver Provider Only (XA)"
		#endIf
	elif (provider == "Embedded MS SQL Server"):
		name = "WebSphere embedded ConnectJDBC driver for MS SQL Server Provider Only"
		if (XA == "true"):
			name = "WebSphere embedded ConnectJDBC driver for MS SQL Server Provider Only (XA)"
		#endIf
	elif (provider == "Informix"):
		name = "Informix JDBC Driver Provider Only"
		if (XA == "true"):
			name = "Informix JDBC Driver Provider Only (XA)"
		#endIf
	#endIf

	print " "
	print "Creating JDBC Provider " + name + "..."

	# Check if the JDBC provider already exists	

	scopeName = getName(scopeId)
	stIndex = (scopeId.find("|") + 1)
	endIndex = (scopeId.find(".") - 1)
	scope = scopeId[stIndex:endIndex+1]

	providerId = ""
	if (scope == "cell"):
		providerId = AdminConfig.getid("/Cell:"+scopeName+"/JDBCProvider:\""+name+"\"/" )
	elif (scope == "node"):
		providerId = AdminConfig.getid("/Node:"+scopeName+"/JDBCProvider:\""+name+"\"/" )
	elif (scope == "server"):
		providerId = AdminConfig.getid("/Server:"+scopeName+"/JDBCProvider:\""+name+"\"/" )
	#endIf

	if (providerId == ""):
		print "  Provider Name:        " + name
		print "  Classpath:            " + path
		print "  Native path:          " + nativePath
		print "  XA enabled:           " + XA

		template = AdminConfig.listTemplates("JDBCProvider", name+"(")
		providerId = AdminConfig.createUsingTemplate("JDBCProvider", scopeId, [["name", name], ["classpath", path], ["nativepath", nativePath]], template)

		# Template creates a datasource with the same name as the provider
		# Delete this datasource
		dsId = ""
		dsList = AdminConfig.list("DataSource")
		if (len(dsList) > 0):
			for item in dsList.split("\n"):
				item = item.rstrip()
				provider = AdminConfig.showAttribute(item, "provider" )
				if (providerId == provider):
					dsId = item
					print "Found DS"
				#endIf
			#endFor
		#endIf
		if (dsId != ""):
			AdminConfig.remove(dsId)
		#endIf

		print name + " provider created successfully!"
	else:
		print name + " provider already exists!"
	#endElse

	return providerId
#endDef

def removeJDBCProvider(name):
	print " "
	print "Removing JDBCProvider " + name + "..."

	temp = AdminConfig.getid("/JDBCProvider:" + name + "/")
	if (temp):
		AdminConfig.remove(temp)
		print name + " removed successfully!"
	else:
		print name + " not found!"
	#endElse
#endDef

def createDatasource (datasourceName, jndiName, stmtCacheSz, authAliasName, providerId):
	# Connection pool properties
	maxConnections =    50
	minConnections =    10

	print " "
	print "Creating DataSource " + datasourceName + "..."
	
	# Check if the DataSource already exists
	dsId = ""
	dsList = AdminConfig.getid("/DataSource:" + datasourceName + "/")
	if (len(dsList) > 0):
		for item in dsList.split("\n"):
			item = item.rstrip()
			provider = AdminConfig.showAttribute(item, "provider" )
			if (providerId == provider):
				dsId = item
			#endIf
		#endFor
	#endIf

	if (dsId == ""):
		print "  Datasource Name:       " + datasourceName
		print "  JNDI Name:             " + jndiName
		print "  Statement Cache Size:  " + str(stmtCacheSz)	
		print "  AuthAliasName:         " + authAliasName
		
		# Map provider to datasource template
		providerName = getName(providerId)
		
		providerToDsDict = {"DB2 UDB for iSeries Provider Only (Native XA)":"DB2 UDB for iSeries (Native XA) DataSource",
					"DB2 UDB for iSeries Provider Only (Native)":"DB2 UDB for iSeries (Native) DataSource",
					"DB2 UDB for iSeries Provider Only (Toolbox XA)":"DB2 UDB for iSeries (Toolbox XA) DataSource",
					"DB2 UDB for iSeries Provider Only (Toolbox)":"DB2 UDB for iSeries (Toolbox) DataSource",
					"DB2 Universal JDBC Driver Provider Only (XA)":"DB2 Universal JDBC Driver XA DataSource",
					"DB2 Universal JDBC Driver Provider Only":"DB2 Universal JDBC Driver DataSource",
					"DB2 for zOS Local JDBC Provider Only (RRS)":"DB2 for zOS Local JDBC Driver DataSource (RRS)",
					"Derby JDBC Provider Only":"Derby JDBC Driver DataSource 40",
					"Derby JDBC Provider Only (XA)":"Derby JDBC Driver XA DataSource",
					"Oracle JDBC Driver Provider Only (XA)":"Oracle JDBC Driver XA DataSource",
					"Oracle JDBC Driver Provider Only":"Oracle JDBC Driver DataSource",
					"WebSphere embedded ConnectJDBC driver for MS SQL Server Provider Only (XA)":"WebSphere embedded ConnectJDBC for SQL Server XA DataSource",
					"WebSphere embedded ConnectJDBC driver for MS SQL Server Provider Only":"WebSphere embedded ConnectJDBC for SQL Server DataSource",
					"Informix JDBC Driver Provider Only (XA)":"Informix JDBC Driver XA DataSource",
					"Informix JDBC Driver Provider Only":"Informix JDBC Driver DataSource"}

		dsName = providerToDsDict[providerName]
		
		# If using Derby Database, check the WAS Version and use the new Derby 40 provider for WAS Version >= 7.0
		if (dsName == "Derby JDBC Driver XA DataSource"):
			server = AdminControl.queryNames('WebSphere:type=Server,*')
			WASversion = AdminControl.getAttribute(server,'platformVersion')
			if (WASversion.startswith('7.')):
				dsName = "Derby JDBC Driver XA DataSource 40"		
				
		template =  AdminConfig.listTemplates("DataSource", dsName)
		attr = [["name", datasourceName], ["jndiName", jndiName], ["statementCacheSize", stmtCacheSz]]
		if (authAliasName != ""):
			attr.append(["authDataAlias", authAliasName])
			attr.append(["xaRecoveryAuthAlias", authAliasName])
		#endIf
		dsId = AdminConfig.createUsingTemplate("DataSource", providerId, attr, template)

		#Update connection pool sizings
		pool = AdminConfig.showAttribute(dsId, "connectionPool")
		AdminConfig.modify(pool, [["maxConnections", maxConnections], ["minConnections", minConnections]])

		#Determine RRA
		tempName = providerId[providerId.rfind("/")+1 : providerId.rfind("|")]
		if (providerId.find("/servers/") > 0):
			radapter = AdminConfig.getid("/Server:" + tempName + "/J2CResourceAdapter:WebSphere Relational Resource Adapter/")
		elif (providerId.find("/nodes/") > 0):
			radapter = AdminConfig.getid("/Node:" + tempName + "/J2CResourceAdapter:WebSphere Relational Resource Adapter/")
		elif (providerId.find("(cells/") > 0):
			radapter = AdminConfig.getid("/Cell:" + tempName + "/J2CResourceAdapter:WebSphere Relational Resource Adapter/")
		#endIf
		
		#Create CMPConnectionFactory
		tempList = AdminConfig.listTemplates('CMPConnectorFactory','default')
		template = ""
		if (len(tempList) > 0):
			for item in tempList.split("\n"):
				item = item.rstrip()
				if (item[0:20] == "CMPConnectorFactory("):
					template = item
					break
				#endIf
			#endFor
		#endIf
		
		attr = [["name", datasourceName + "_CF"], ["cmpDatasource", dsId]]
		cmpFact_id = AdminConfig.createUsingTemplate("CMPConnectorFactory", radapter, attr, template)

		print datasourceName + " created successfully!"
	else:
		print datasourceName + " already exists in this JDBC Provider!"
	#endIf

	return dsId
#endDef

def addDatasourceProperty (datasourceId, name, value):
    parms = ["-propertyName", name, "-propertyValue", value]
    AdminTask.setResourceProperty(datasourceId, parms)
#endDef 

def updateDB2orDerbyDatasource (datasourceId, dbname, hostname, port, driverType):
	resourceProps = AdminConfig.list("J2EEResourceProperty", datasourceId).split("\n")
	for item in resourceProps:
		item = item.rstrip()
		propName = getName(item)
		if (propName == "serverName"):
			AdminConfig.modify(item, [["value", hostname]])
		#endIf
		if (propName == "portNumber"):
			AdminConfig.modify(item, [["value", port]])
		#endIf
		if (propName == "databaseName"):
			AdminConfig.modify(item, [["value", dbname]])
		#endIf
		if (propName == "driverType"):
			AdminConfig.modify(item, [["value", driverType]])
		#endIf
	#endFor
#endDef

def updateInformixDatasource (datasourceId, dbname, serverName, port, ifxHost, lockMode):
	resourceProps = AdminConfig.list("J2EEResourceProperty", datasourceId).split("\n")
	for item in resourceProps:
		item = item.rstrip()
		propName = getName(item)
		if (propName == "serverName"):
			AdminConfig.modify(item.rstrip(), [["value", serverName]])
		#endIf
		if (propName == "portNumber"):
			AdminConfig.modify(item, [["value", port]])
		#endIf
		if (propName == "databaseName"):
			AdminConfig.modify(item, [["value", dbname]])
		#endIf
		if (propName == "informixLockModeWait"):
			AdminConfig.modify(item, [["value", lockMode]])
		#endIf
		if (propName == "ifxIFXHOST"):
			AdminConfig.modify(item, [["value", ifxHost]])
		#endIf
	#endFor
#endDef

def updateOracleDatasource (datasourceId, sid, hostname, port):
	resourceProps = AdminConfig.list("J2EEResourceProperty", datasourceId).split("\n")
	url = "jdbc:oracle:thin:@" + hostname + ":" + port + ":" + sid        
	for item in resourceProps:
		item = item.rstrip()
		propName = getName(item)
		if (propName == "URL"):
			AdminConfig.modify(item, [["value", url]])
		#endIf
	#endFor
#endDef

def removeDatasource(name):
	print " "
	print "Removing DataSource " + name + "..."

	temp = AdminConfig.getid("/DataSource:" + name + "/")
	if (temp):
		AdminConfig.remove(temp)
		print name + " removed successfully!"
	else:
		print name + " not found!"
	#endElse
#endDef

#-----------------------------------------------------------------
# enableSIBService - Enable the SIB Service on the specified
#            server.
#-----------------------------------------------------------------
def enableSIBService (serverId):
	serverName = getName(serverId)

	service = ""
	serviceList = AdminConfig.list("SIBService")
	for item in serviceList.split("\n"):
		item = item.rstrip()
		if (item.find("servers/" + serverName + "|") >= 0):
			service = item
		#endIf
	#endFor

	print " "
	print "Enabling SIB Service on " + serverName + "..."

	if (service == ""):                 
		print "Unable to find SIB Service!"
	else:
		parms = [["enable", "true"]]
		AdminConfig.modify(service, parms )
		print "SIB Service enabled successfully!"
	#endElse
#endDef

#-----------------------------------------------------------------
# createSIBus - Create a new SIBus if one does not exist. Otherwise,
#            return the existing SIBus.
#-----------------------------------------------------------------
def createSIBus ( busName, authAlias ):
	print " "
	print "Creating SIBus " + busName + "..."

	# Check if the SIBus already exists

	SIBus = AdminConfig.getid("/SIBus:"+busName+"/" )
	if (SIBus == ""):
		parms = ["-bus", busName, "-interEngineAuthAlias", authAlias]
		SIBus = AdminTask.createSIBus(parms )
                
		print busName + " created successfully!"
	else:
		print busName + " already exists!"
	#endElse

	return SIBus
#endDef

def deleteSIBus(name):
	print " "
	print "Deleting SIBus " + name + "..."

	temp = AdminConfig.getid("/SIBus:" + name + "/")
	if (temp):
		parms = ["-bus", name]
		AdminTask.deleteSIBus(parms)
		print name + " removed successfully!"
	else:
		print name + " not found!"
	#endElse
#endDef

#-----------------------------------------------------------------
# createSIBusRole - Add user role
#-----------------------------------------------------------------
def createSIBusSecurityRole ( busId, userName ):
	print " "
	busName = getName(busId)

	# Check if the SIBAuthUser already exists
	SIBAuthUser = ""
	tmpSIBAuthUserList = AdminConfig.list("SIBAuthUser", busId)
	if (len(tmpSIBAuthUserList) > 0):
		for item in tmpSIBAuthUserList.split("\n"):
			item = item.rstrip()
			tmp = AdminConfig.showAttribute(item, "identifier" )
			if (tmp == userName):
				SIBAuthUser = item
			#endIf
		#endFor
	#endIf

	if (SIBAuthUser == ""):
		print "Creating SIBus security role for " + userName + "..."
                
		parms = ["-bus", busName, "-user", userName]
		SIBAuthUser = AdminTask.addUserToBusConnectorRole(parms )
               
		print userName + " security role created successfully!"
	else:
		print "Role " + userName + " already exists for " + busName + "!"
	#endElse

	return SIBAuthUser
#endDef

#-----------------------------------------------------------------
# addSIBusMember - Add the specified server or cluster to the
#            SIBus if it does not already exist. Assumes that the
#            specified SIBus already exists.
#-----------------------------------------------------------------
def addSIBusMember ( busId, fileStore, targetArgs, dataStoreArgs ):
	#    busName          - SIBus name
	#    fileStore [0]    - create file store, otherwise create data store
 	#    fileStore [1]    - logDirectory - directory where fileStore is located (only used if fileStore[0] = true)
	#    targetArgs[0]    - cluster name or node name
	#    targetArgs[1]    - server name
	#    dataStoreArgs[0] - defaultDS - create default DS (true|false)
	#    dataStoreArgs[1] - dsJndi - jndi name of the datastore (only used if defaultDS = false)

	busName = getName(busId)
	if (len(targetArgs) == 1):
		clusterName = targetArgs[0]
		nodeName = "dummy"
		serverName = "dummy"
	else:
		nodeName = targetArgs[0]
		serverName = targetArgs[1]
		clusterName = "dummy"
	#endElse

	if (len(dataStoreArgs) == 2):
		defaultDS = dataStoreArgs[0]
		dsJndi = dataStoreArgs[1]
		defaultDS = defaultDS.lower()
	#endIf

	# Check if the bus member already exists
	parms = ["-bus", busName]
	busMembers = AdminTask.listSIBusMembers(parms).split("\n")
	member = ""
	if (busMembers[0] != ""):
		for item in busMembers:
			item = item.rstrip()
			cluster = AdminConfig.showAttribute(item, "cluster" )
			node = AdminConfig.showAttribute(item, "node" )
			server = AdminConfig.showAttribute(item, "server" )

			if (cluster == clusterName  or ( server == serverName  and node == nodeName ) ):
				member = item
				break
			#endIf
		#endFor
	#endIf
	
	if (member == ""):
		print ""
		if (len(targetArgs) == 1):
			print "Adding SIBus member " + clusterName + "..."
			parms = ["-bus", busName, "-cluster", clusterName]
		else:
			print "Adding SIBus member " + nodeName + " - " + serverName + "..."
			parms = ["-bus", busName, "-node", nodeName, "-server", serverName]
		#endElse

		print "  File Store:            " + fileStore[0]
		if (fileStore[0] == "true"):
			parms.append("-fileStore")
			if (fileStore[1] != "default" and fileStore[1] != ""):
				print "  File Store Location:   " + fileStore[1]
				parms.append("-logDirectory")
                        	parms.append(fileStore[1])
			#endIf
		else:
			parms.append("-dataStore")
			print "  Default DataSource:    " + defaultDS
			parms.append("-createDefaultDatasource")
			parms.append(defaultDS)
			if (defaultDS == "false"):
				print "  Datasource JNDI Name:  " + dsJndi
				parms.append("-datasourceJndiName")
				parms.append(dsJndi)
			#endIf
		#endElse

		member = AdminTask.addSIBusMember(parms )
		print "SIBus member added successfully!"
	else:
		print "SIBus member already exists!"
	#endElse

	return member
#endDef

#-----------------------------------------------------------------
# createMessageEngine - Create a new message engine on the specified
#            target.
#-----------------------------------------------------------------
def createMessageEngine ( busId, defaultDS, dsJndi, optArgs ):
	#    busName     - SIBus name
	#    defaultDS   - create default DS (true|false)
	#    dsJndi      - jndi name of the datasource (only used if defaultDS = false)
	#    optArgs[0]  - node name or cluster name
	#    optArgs[1]  - server name

	defaultDS = defaultDS.lower()
	if (len(optArgs) == 1):
		clusterName = optArgs[0]
	else:
		nodeName = optArgs[0]
		serverName = optArgs[1]
	#endElse

	busName = getName(busId)

	print " "
	print "Creating SIB Messaging Engine..."
	print "  Bus Name:            " + busName
	print "  Default DataSource:  " + defaultDS
	if (defaultDS == "False"):
		print "  Datasource JNDI Name:  " + dsJndi
	#endIf
	if (len(optArgs) == 1):
		print "  Cluster Name:        " + clusterName
	else:
		print "  Node Name:           " + nodeName
		print "  Server Name:         " + serverName
	#endElse

	if (len(optArgs) == 1):
		parms = ["-bus", busName, "-cluster", clusterName, "-createDefaultDatasource", defaultDS]
	else:
		parms = ["-bus", busName, "-node", nodeName, "-server", serverName, "-createDefaultDatasource", defaultDS]
	#endElse

	if (defaultDS == "false"):
		parms.append("-datasourceJndiName")
		parms.append(dsJndi)
	#endIf

	me = AdminTask.createSIBEngine(parms )
	print getName(me) + "Message Engine created successfully!"
	
	return me
#endDef

#-----------------------------------------------------------------
# modifyMEDataStore - Modify the data store attributes for the
#            target messageing engine.
#-----------------------------------------------------------------
def modifyMEDataStore ( meId, authAlias, schema ):
	#    meId        - id of the target message engine
	#    authAlias   - authentication alias name
	#    datasource  - datasource JNDI name
	#    schema      - schema name

	print " "
	print "Modifying ME DataStore parameters..."

	dataStore = AdminConfig.showAttribute(meId, "dataStore" )

	if (dataStore != ""):
		print "  ME Name:          " + getName(meId)
		print "  AuthAlias:        " + authAlias
		print "  Schema Name:      " + schema

		attrs = [["authAlias", authAlias], ["schemaName", schema]]
		AdminConfig.modify(dataStore, attrs )

		print getName(meId) + " data store modified successfully!"
	else:
		print "Data store could not be located for " + getName(meId) + "!"
	#endElse
#endDef

#-----------------------------------------------------------------
# createSIBDestination - Create a new SIB Destination if one with the same
#            name does not exist on the specified SIBus. Otherwise,
#            return the existing Destination.
#-----------------------------------------------------------------
def createSIBDestination ( busId, destName, destType, reliability, optArgs ):
	#    SIBus       - SIBus name
	#    destName    - destination name
	#    destType    - destination type
	#    reliability - reliability
	#    optArgs[0]  - cluster name or node name
	#    optArgs[1]  - server name

	if (len(optArgs) == 1):
		clusterName = optArgs[0]
	elif (len(optArgs) == 2) :
		nodeName = optArgs[0]
		serverName = optArgs[1]
	#endElse

	print " "
	print "Creating SIB Destination " + destName + "..."

	# Check if the SIB Destination already exists
	SIBus = getName(busId)
	parms = ["-bus", SIBus]
	destList = AdminTask.listSIBDestinations(parms )

	dest = ""
	if (len(destList) > 0):
		for item in destList.split("\n"):
			item = item.rstrip()
			ident = AdminConfig.showAttribute(item.rstrip(), "identifier" )
			if (ident == destName):
				dest = item.rstrip()
				break
			#endIf
		#endFor
	#endIf

	if (dest == ""):        
		print "  Destination Name:  " + destName
		print "  Destination Type:  " + destType
		print "  Reliability:       " + reliability
                
		parms = ["-bus", SIBus, "-name", destName, "-type", destType, "-reliability", reliability]

		if (destType == "Queue"):
			if (len(optArgs) == 1):
				print "  Cluster Name:      " + clusterName
				parms.append("-cluster")
				parms.append(clusterName)
			elif (len(optArgs) == 2):
				print "  Node Name:         " + nodeName
				print "  Server Name:       " + serverName
				parms.append("-node")
				parms.append(nodeName)
				parms.append("-server")
				parms.append(serverName)
			#endElse
		#endIf

		dest = AdminTask.createSIBDestination(parms )
                
		print destName + " created successfully!"
	else:
		print destName + " already exists!"
	#endElse

	return dest
#endDef

def deleteSIBDestination(name):
	print " "
	print "Deleting SIB Destination " + name + "..."

	destList = AdminConfig.list("SIBDestination")
	dest = ""
	if (len(destList) > 0):
		for item in destList.split("\n"):
			item = item.rstrip()
			ident = AdminConfig.showAttribute(item.rstrip(), "identifier" )
			if (ident == name):
				dest = item
				break
			#endIf
		#endFor
	#endIf

	if (dest != ""):
		bus = dest[dest.rfind("/")+1 : dest.rfind("|")]
		parms = ["-bus", bus, "-name", name]
		AdminTask.deleteSIBDestination(parms)
		print name + " removed successfully!"
	else:
		print name + " not found!"
	#endElse
#endDef

#-----------------------------------------------------------------
# createOneOfNPolicy - Install the SIB JMS Resource Adapter
#            at the cell scope.
#-----------------------------------------------------------------
def createOneOfNPolicy ( name, alivePeriod, serverName, meName ):
	#    name        - name of HA policy
	#    alivePeriod - number of seconds the server is alive
	#    serverName  - name of pinned server
	#    meName      - name of corresponding messaging engine

	groupName = AdminTask.getDefaultCoreGroupName( )
	group = AdminConfig.getid("/CoreGroup:"+groupName+"/" )

	groupServer = AdminConfig.getid("/CoreGroupServer:"+serverName+"/" )

	print " "
	print "Creating OneOfNPolicy " + name + "..."

	# Check if the policy already exists
	policy = AdminConfig.getid("/OneOfNPolicy:\""+name+"\"/" )

	if (policy == ""):
		print "  Alive Period(s):  " + str(alivePeriod)
		print "  Server Name:      " + serverName
		print "  ME Name:          " + meName

		attrs = [["name", name], ["failback", "true"], ["isAlivePeriodSec", alivePeriod], ["policyFactory", "com.ibm.ws.hamanager.coordinator.policy.impl.OneOfNPolicyFactory"]]
                
		policy = AdminConfig.create("OneOfNPolicy", group, attrs, "policies" )
                
		attrs = [["preferredOnly", "true"], ["preferredServers", groupServer]]
		AdminConfig.modify(policy, attrs )

		attrs = [["name", "WSAF_SIB_MESSAGING_ENGINE"], ["value", meName]]
		AdminConfig.create("MatchCriteria", policy, attrs, "MatchCriteria" )

		attrs = [["name", "type"], ["value", "WSAF_SIB"]]
		AdminConfig.create("MatchCriteria", policy, attrs, "MatchCriteria" )

		print name + " created successfully!"
	else:
		print name + " already exists!"
	#endElse

	return policy
#endDef

def deleteOneOfNPolicy (name):
	print " "
	print "Deleting OneOfNPolicy " + name + "..."

	policyList = AdminConfig.list("OneOfNPolicy")
	policy = ""
	if (len(policyList) > 0):
		for item in policyList.split("\n"):
			item = item.rstrip()
			if (name == getName(item)):
				policy = item
				break
			#endIf
		#endFor
	#endIf

	if (policy != ""):
		AdminConfig.remove(policy)
		print name + " removed successfully!"
	else:
		print name + " not found!"
	#endElse
#endDef

#-----------------------------------------------------------------
# createJMSConnectionFactory - Create a new JMS Connection Factory
#            if one with the same name does not exist on the SIBus.
#            Otherwise, return the existing Connection Factory.
#-----------------------------------------------------------------
def createJMSConnectionFactory ( busId, cfName, cfType, jndiName, authAlias, scope ):
	# Create JMS Connection Factory
	#    SIBus      - SIBus name
	#    cfName     - connection factory name
	#    cfType     - connection factory type
	#    jndiName   - connection factory jndi name
	#    authAlias  - authentication alias name
	#    scope      - scope

	print " "
	print "Creating JMS " + cfType + " Connection Factory " + cfName + "..."

	# Check if the connection factory already exists

	parms = ["-type", cfType]
	cfList = AdminTask.listSIBJMSConnectionFactories(scope, parms )
	connectionFactory = ""
	if (len(cfList) > 0):
		for item in cfList.split("\n"):
			item = item.rstrip()
			if (item.find(cfName) >= 0):
				connectionFactory = item
				break
			#endIf
		#endFor
	#enfIf

	if (connectionFactory == "" ):
		print "  Connection Factory Name:  " + cfName
		print "  Connection Factory Type:  " + cfType
		print "  JNDI Name:                " + jndiName

		params = ["-name", cfName, "-jndiName", jndiName, "-busName", getName(busId), "-type", cfType, "-authDataAlias", authAlias]
		connectionFactory = AdminTask.createSIBJMSConnectionFactory(scope, params )
                
		print cfName + " created successfully!"
	else:
		print cfName + " already exists!"
	#endElse

	return connectionFactory
#endDef

def deleteJMSConnectionFactory(name):
	print " "
	print "Deleting JMS Connection Factory " + name + "..."

	temp = AdminConfig.getid("/J2CConnectionFactory:" + name + "/")
	if (temp):
		AdminTask.deleteSIBJMSConnectionFactory(temp)
		print name + " removed successfully!"
	else:
		print name + " not found!"
	#endElse
#endDef

#-----------------------------------------------------------------
# createJMSQueue - Create a new JMS Queue if one with the same
#            name does not exist at the specified scope. Otherwise,
#            return the existing JMS Queue.
#-----------------------------------------------------------------
def createJMSQueue ( qName, jndiName, SIBDest, delMode, scope ):
	#    qName    - queue name
	#    jndiName - queue jndi name
	#    SIBDest  - SIB destination
	#    delMode  - delivery mode
	#    scope    - scope

	print " "
	print "Creating JMS Queue " + qName + "..."

	# Check if the queue already exists

	qList = AdminTask.listSIBJMSQueues(scope )
	queue = ""
	if (len(qList) > 0):
		for item in qList.split("\n"):
			item = item.rstrip()
			if (item.find(qName) >= 0):
				queue = item
				break
			#endIf
		#endFor
	#endIf

	if (queue == ""):
		print "  Queue Name:       " + qName
		print "  JNDI Name:        " + jndiName
		print "  SIB Destination:  " + SIBDest
		print "  Delivery Mode:    " + delMode

		params = ["-name", qName, "-jndiName", jndiName, "-queueName", SIBDest, "-deliveryMode", delMode]
		queue = AdminTask.createSIBJMSQueue(scope, params )
                
		print qName + " created successfully!"
	else:
		print qName + " already exists!"
	#endElse

	return queue
#endDef

def deleteJMSQueue(queueName):
	print " "
	print "Deleting JMS Queue " + queueName + "..."

	temp = AdminConfig.getid("/J2CAdminObject:" + queueName + "/")
	if (temp):
		AdminTask.deleteSIBJMSQueue(temp)
		print queueName + " removed successfully!"
	else:
		print queueName + " not found!"
	#endElse
#endDef

#-----------------------------------------------------------------
# createJMSTopic - Create a new JMS Topic if one with the same
#            name does not exist at the specified scope. Otherwise,
#            return the existing JMS Topic.
#-----------------------------------------------------------------
def createJMSTopic ( tName, jndiName, tSpace, delMode, scope ):
	#    tName    - topic name
	#    jndiName - topic jndi name
	#    tSpace   - topic space
	#    delMode  - delivery mode
	#    scope    - scope

	print " "
	print "Creating JMS Topic " + tName + "..."

	# Check if the topic already exists

	tList = AdminTask.listSIBJMSTopics(scope )
	topic = ""
	if (len(tList) > 0):
		for item in tList.split("\n"):
			item = item.rstrip()
			if (item.find(tName) >= 0):
				topic = item
				break
			#endIf
		#endFor
	#endIf

	if (topic == ""):
		print "  Topic Name:     " + tName
		print "  JNDI Name:      " + jndiName
		print "  Topic Space:    " + tSpace
		print "  Delivery Mode:  " + delMode

		params = ["-name", tName, "-jndiName", jndiName, "-topicName", tName, "-topicSpace", tSpace, "-deliveryMode", delMode]
		topic = AdminTask.createSIBJMSTopic(scope, params )
                
		print tName + " created successfully!"
	else:
		print tName + " already exists!"
	#endElse

	return topic
#endDef

def deleteJMSTopic(topicName):
	print " "
	print "Deleting JMS Topic " + topicName + "..."

	temp = AdminConfig.getid("/J2CAdminObject:" + topicName + "/")
	if (temp):
		AdminTask.deleteSIBJMSTopic(temp)
		print topicName + " removed successfully!"
	else:
		print topicName + " not found!"
	#endElse
#endDef

#-----------------------------------------------------------------
# createMDBActivationSpec - Create a new MDB Activation Spec if one
#            with the same name does not exist at the specified
#            scope. Otherwise, return the existing Activation Spec.
#-----------------------------------------------------------------
def createMDBActivationSpec ( mdbName, jndiName, busId, JMSDestJndi, destType, authAlias, scope, durability ):
	#    mdbName     - MDB name
	#    jndiName    - activation spec jndi name
	#    SIBus       - SIBus name
	#    JMSDestJndi - JMS destination JNDI name
	#    destType    - destination type
	#    authAlias   - authentication alias name
	#    scope       - scope
	#    durability  - subscriptionDurability

	print " "
	print "Creating MDB Activation Spec " + mdbName + "..."

	# Check if the activation spec already exists

	asList = AdminTask.listSIBJMSActivationSpecs(scope )
	mdb = ""
	if (len(asList) > 0):
		for item in asList.split("\n"):
			item = item.rstrip()
			if (item.find(mdbName) >= 0):
				mdb = item
				break
			#endIf
		#endFor
	#endIf

	if (mdb == ""):
		print "  MDB Activation Spec Name:   " + mdbName
		print "  JNDI Name:                  " + jndiName
		print "  JMS Destination JNDI Name:  " + JMSDestJndi
		print "  Destination Type:           " + destType

		SIBus = getName(busId)
		params = ["-name", mdbName, "-jndiName", jndiName, "-busName", SIBus, "-destinationJndiName", JMSDestJndi, "-destinationType", destType, "-authenticationAlias", authAlias, "-subscriptionDurability", durability, "-clientId", mdbName, "-subscriptionName", mdbName]
		mdb = AdminTask.createSIBJMSActivationSpec(scope, params )
                
		print mdbName + " created successfully!"
	else:
		print mdbName + " already exists!"
	#endElse

	return mdb
#endDef

def deleteMDBActicationSpec (mdbName):
	print " "
	print "Deleting MDB Activation Spec " + mdbName + "..."

	temp = AdminConfig.getid("/J2CActivationSpec:" + mdbName + "/")
	if (temp):
		AdminTask.deleteSIBJMSActivationSpec(temp)
		print mdbName + " removed successfully!"
	else:
		print mdbName + " not found!"
	#endElse
#endDef

#-----------------------------------------------------------------
# addHostAliasToDefaultHost - Add the specified port to the default
#            host mappings.
#-----------------------------------------------------------------
def addHostAliasToDefaultHost ( port ):
	#    port - port number

	print " "
	print "Creating HostAlias for " + port + "..."

	# Check if the port already exists

	hostList = AdminConfig.list("HostAlias" )
	hostAlias = ""
	if (len(hostList) > 0):
		for item in hostList.split("\n"):
			item = item.rstrip()
			tmp = AdminConfig.showAttribute(item, "port" )
			if (tmp == port):
				hostAlias = item
				break
			#endIf
		#endFor
	#endIf

	if (hostAlias == ""):
		print "  Host Name:  *"
		print "  Port:       " + port

		vhList = AdminConfig.list("VirtualHost" )
		defaultHost = ""
		for item in vhList.split("\n"):
			item = item.rstrip()
			if (getName(item) == "default_host"): 
				defaultHost = item
			#endIf
		#endFor

		attrs = [["hostname", "*" ], ["port", port]]
		hostAlias = AdminConfig.create("HostAlias", defaultHost, attrs )

		print port + " created successfully!"
	else:
		print port + " already exists!"
	#endElse

	return hostAlias
#endDef

#-----------------------------------------------------------------
# createServer - Create a new server if one with the same name
#            does not exist. Otherwise, return the existing server.
#-----------------------------------------------------------------
def createServer ( serverName, nodeName ):
	#    serverName - server name
	#    nodeName   - node name

	print " "
	print "Creating Server " + serverName + "..."

	# Check if the server already exists

	server = AdminConfig.getid("/Node:"+nodeName+"/Server:"+serverName+"/")
                
	if (server == ""):
		print "  Server Name:  " + serverName
		print "  Node Name:    " + nodeName

		node = AdminConfig.getid("/Node:"+nodeName+"/" )

		templateList = AdminConfig.listTemplates("Server","APPLICATION_SERVER")
		template = ""
		for item in templateList.split("\n"):
			item = item.rstrip()
			if (getName(item) == "default"):
				template = item
				break
			#endIf
		#endFor                

		attrs = [["name", serverName]]
		server = AdminConfig.createUsingTemplate("Server", node, attrs, template )
                
		print serverName + " created successfully!"
	else:
		print serverName + " already exists!"
	#endElse

	return server
#endDef

#-----------------------------------------------------------------
# createCluster - Create a new cluster if one with the same name
#            does not exist. Otherwise, return the existing cluster.
#-----------------------------------------------------------------
def createCluster ( clusterName, preferLocal, description, cell ):
	#    clusterName - cluster name
	#    preferLocal - prefer local value
	#    description - cluster description
	#    cell        - cell

	print " "
	print "Creating Cluster " + clusterName + "..."

	# Check if the cluster already exists
	cluster = ""
	clusterList = AdminConfig.list("ServerCluster" )
	if (len(clusterList) > 0):
		for item in clusterList.split("\n"):
			item = item.rstrip()
			if (item.find(clusterName) >= 0):
				cluster = item
				break
			#endIf
		#endFor
	#endIf

	if (cluster == ""):
		print "  Cluster Name:  " + clusterName
		print "  Prefer Local:  " + preferLocal
		print "  Description:   " + description

		attrs = [["name", clusterName], ["preferLocal", preferLocal], ["description", "$description"]]
		cluster = AdminConfig.create("ServerCluster", cell, attrs )
                
		print clusterName + " created successfully!"
	else:
		print clusterName + " already exists!"
	#endElse

	return cluster
#endDef

#-----------------------------------------------------------------
# createClusterMember - Create a new cluster member if one with the
#            same name does not exist. Otherwise, return the
#            existing cluster member.
#-----------------------------------------------------------------
def createClusterMember ( memberName, nodeId, weight, clusterId ):
	#    memberName - member name
	#    node       - node
	#    weight     - weight
	#    cluster    - cluster

	print " "
	print "Creating Cluster Member " + memberName + "..."

	# Check if the cluster member already exists
	member = ""
	memberList = AdminConfig.list("ClusterMember" )
	if (len(memberList) > 0):
		for item in memberList.split("\n"):
			item = item.rstrip()
			if (item.find(memberName) >= 0):
				member = item
				break
			#endIf
		#endFor
	#endIf

	if (member == ""):
		print "  Member Name:  " + memberName
		print "  Node:         " + getName(nodeId)
		print "  Weight:       " + weight
		print "  Cluster:      " + getName(clusterId)

		attrs = [["memberName", memberName], ["weight", weight]]
		member = AdminConfig.createClusterMember(cluster, node, attrs )
        
		print memberName + " created successfully!"
	else:
		print memberName + " already exists!"
	#endElse

	return member
#endDef

#-----------------------------------------------------------------
# installApp - Install the specified application ear file if an
#            application with the same name does not exist.
#-----------------------------------------------------------------
def installApp ( appName, ear, deployejb, deployws, defaultBindings, earMetaData, dbType, target ):
	#    appName         - application name
	#    ear             - ear file
	#    deployejb       - deploy ejb (true|false)
	#    deployws        - deploy webservices (true|false)
	#    defaultBindings - use default binding (true|false)
	#    reloadEnabled   - check filesystem to reload changed files (true|false)
	#    earMetaData     - use MetaData from ear (true|false)
	#    dbType          - ejb deploy db type
	#    target[0]       - node name or cluster name
	#    target[1]       - server name

	print ""
	print "Installing application " + appName + "..."
	
	deployejb = deployejb.lower()
	deployws = deployws.lower()
	defaultBindings = defaultBindings.lower()
	earMetaData = earMetaData.lower()

	# Check if the application already exists
	app = ""
	appList = AdminApp.list( )
	if (len(appList) > 0):
		for item in appList.split("\n"):
			item = item.rstrip()
			if (item.find(appName) == 0):
				app = item
				break
			#endIf
		#endFor
	#endIf

	if (app == ""):
		print "  Application Name:      " + appName
		print "  Ear file:              " + ear
		if (len(target) == 1):
			cluster = target[0]
			print "  Target Cluster:        " + cluster
		else:
			node = target[0]
			server = target[1]
			print "  Target Node:           " + node
			print "  Target Server:         " + server
		#endElse
		print "  Deploy EJB:            " + deployejb
		print "  Deploy WebServices:    " + deployws
		print "  Use default bindings:  " + defaultBindings
		print "  Use Ear MetaData:      " + earMetaData
		print "  Deployed DB Type:      " + dbType

		parms = "-appname " + appName
		if (deployejb == "true"):
			parms += " -deployejb"
			parms += " -deployejb.dbtype " + dbType
		else:
			parms += " -nodeployejb"
		#endElse
		if (deployws == "true"):
			parms += " -deployws"
		else:
			parms += " -nodeployws"
		#endElse
		if (defaultBindings == "true"):
			parms += " -usedefaultbindings -defaultbinding.ee.defaults"
		#endIf
		if (earMetaData == "true"):
			parms += " -useMetaDataFromBinary"
		else:
			parms += " -nouseMetaDataFromBinary"
		#endElse

		if (len(target) == 1):
			parms += " -cluster " + cluster
		else:
			parms += " -node " + node + " -server " + server
		#endElse

		parms1 = [parms]

		print "Starting application install..."

		app = AdminApp.install(ear, parms1 )

		print "Install completed successfully!"
	else:
		print appName + " already exists!"
	#endElse

	return app
#endDef

#-----------------------------------------------------------------
# uninstallApp - Uninstall the specified application if it exists.
#-----------------------------------------------------------------
def uninstallApp ( appName ):
	#    appName - application name

	print ""
	print "Uninstalling application..."

	# Check if the application does not exist
	app = ""
	appList = AdminApp.list( )
	if (len(appList) > 0):
		for item in appList.split("\n"):
			item = item.rstrip()
			if (item.find(appName) >= 0):
				app = item
				break
			#endIf
		#endFor
	#endIf

	if (app != ""):
		AdminApp.uninstall(appName )

		print "Application uninstalled successfully!"
	else:
		print "Application does not exist!"
	#endElse
#endDef

