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

import java.io.Serializable;

import org.apache.struts2.convention.annotation.Action;
import org.apache.struts2.convention.annotation.Actions;
import org.apache.struts2.convention.annotation.Namespace;
import org.apache.struts2.convention.annotation.Namespaces;
import org.apache.struts2.convention.annotation.Result;
 

@Namespaces(value={@Namespace("/User"),@Namespace("/struts2")})
@Result(location="/struts2/primitive.jsp")
@Actions(value={@Action("primitive")})
public class PrimitiveAction implements Serializable {

    private static final long serialVersionUID = -8740690568973864665L;

    private static int hitCount = 0;

    public PrimitiveAction() {

    }

    public int getHitCount() {
        return hitCount;
    }

    public String execute() {
        hitCount++;
        return "success";
    }
}
