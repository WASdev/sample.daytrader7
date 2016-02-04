package com.ibm.websphere.samples.daytrader.web.prims;

import java.util.Set;

import javax.enterprise.context.RequestScoped;
import javax.enterprise.inject.spi.Bean;
import javax.enterprise.inject.spi.BeanManager;
import javax.naming.InitialContext;

@RequestScoped
public class PingCDIBean {

	private static int helloHitCount=0;
	private static int getBeanManagerHitCount=0;
	
    public int hello() {
        return ++helloHitCount;
    }

    public int getBeanMangerViaJNDI() throws Exception {
        BeanManager beanManager = (BeanManager) new InitialContext().lookup("java:comp/BeanManager");
        Set<Bean<?>> beans = beanManager.getBeans(Object.class);
        if (beans.size() > 0) {
            return ++getBeanManagerHitCount;
        }
        return 0;
        
    }
}

