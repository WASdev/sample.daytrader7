/**
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
 */
package com.ibm.websphere.samples.daytrader.web.struts;

import java.util.Collection;
import java.util.Date;

import org.apache.struts2.convention.annotation.Action;
import org.apache.struts2.convention.annotation.Namespace;
import org.apache.struts2.convention.annotation.Namespaces;
import org.apache.struts2.convention.annotation.Result;

import com.ibm.websphere.samples.daytrader.TradeAction;
import com.ibm.websphere.samples.daytrader.entities.AccountDataBean;
 
@Action(value = "userStats", results = {
        @Result(name = "SUCCESS", location = "/struts2/userStats.jsp"),
        @Result(name = "ERROR", location = "/struts2/error.jsp") })
@Namespaces(value={@Namespace("/User"),@Namespace("/struts2")})
public class UserStatsAction {
	
	private final TradeAction tradeAction = new TradeAction();
 
    public String execute() throws Exception {
    	try {
            AccountDataBean accountData = tradeAction.getAccountData(userName);
            setId(accountData.getProfileID());
            setCreationDate(accountData.getCreationDate());
            setLastLogin(accountData.getLastLogin());
            setLoginCount(accountData.getLoginCount());
            setLogoutCount(accountData.getLogoutCount());
            
            Collection<?> holdingDataBeans = tradeAction.getHoldings(userName);
            setNumHoldings(holdingDataBeans.size());
        } catch (Exception e) {
            return "ERROR";
        }
    	
    	return "SUCCESS";
    }
     
    //Java Bean to hold the form parameters
    private String userName;
    private String id;
    private Date creationDate;
    private Date lastLogin;
    private int loginCount;
    private int logoutCount;
    private int numHoldings;
    
    public String getUserName() {
        return userName;
    }
    public void setUserName(String userName) {
        this.userName = userName;
    }
	public String getId() {
		return id;
	}
	public void setId(String id) {
		this.id = id;
	}
	public Date getCreationDate() {
		return creationDate;
	}
	public void setCreationDate(Date date) {
		this.creationDate = date;
	}
	public Date getLastLogin() {
		return lastLogin;
	}
	public void setLastLogin(Date date) {
		this.lastLogin = date;
	}
	public int getLoginCount() {
		return loginCount;
	}
	public void setLoginCount(int i) {
		this.loginCount = i;
	}
	public int getLogoutCount() {
		return logoutCount;
	}
	public void setLogoutCount(int logoutCount) {
		this.logoutCount = logoutCount;
	}
	public int getNumHoldings() {
		return numHoldings;
	}
	public void setNumHoldings(int numHoldings) {
		this.numHoldings = numHoldings;
	}
}