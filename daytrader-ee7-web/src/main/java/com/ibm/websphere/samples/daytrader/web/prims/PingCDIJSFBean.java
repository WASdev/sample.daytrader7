package com.ibm.websphere.samples.daytrader.web.prims;
	
import java.io.Serializable;

import javax.enterprise.context.SessionScoped;
import javax.inject.Named;

@Named
@SessionScoped
public class PingCDIJSFBean implements Serializable {

	private static final long serialVersionUID = -7475815494313679416L;
	private int hitCount=0;
		
		
    public int getHitCount() {
        return ++hitCount;
    }
}
