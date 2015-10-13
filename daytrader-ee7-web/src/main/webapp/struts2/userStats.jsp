<!-- 
 * (C) Copyright IBM Corporation 2015.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
-->
<%@ page language="java" contentType="text/html; charset=US-ASCII"
    pageEncoding="US-ASCII"%>
<%@ taglib uri="/struts-tags" prefix="s"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=US-ASCII">
<link rel="stylesheet" href="../style.css" type="text/css" />
<link rel="shortcut icon" href="../favicon.ico" />
<title>User Statistics</title>
</head>
<body>
<h2>User Statistics</h2>
<table class="table">
<thead>
<tr>
<th class="tableHeader" scope="col">User Name</th>
<th class="tableHeader" scope="col">Id</th>
<th class="tableHeader" scope="col">Creation Date</th>
<th class="tableHeader" scope="col">Last Login</th>
<th class="tableHeader" scope="col">Login Count</th>
<th class="tableHeader" scope="col">Logout Count</th>
<th class="tableHeader" scope="col"># Holdings</th>
</tr>
</thead>
<tbody>
<tr class="tableOddRow">
<td class="tableColumn">${action.userName}</td>
<td class="tableColumn">${action.id}</td>
<td class="tableColumn">${action.creationDate}</td>
<td class="tableColumn">${action.lastLogin}</td>
<td class="tableColumn">${action.loginCount}</td>
<td class="tableColumn">${action.logoutCount}</td>
<td class="tableColumn">${action.numHoldings}</td>
</tr>
</tbody>
</table>
<s:include value="userForm.jsp"></s:include>
</body>
</html>