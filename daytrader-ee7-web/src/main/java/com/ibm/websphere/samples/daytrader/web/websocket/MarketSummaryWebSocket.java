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
package com.ibm.websphere.samples.daytrader.web.websocket;

import java.io.IOException;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

import javax.annotation.Resource;
import javax.enterprise.concurrent.ManagedScheduledExecutorService;
import javax.enterprise.event.Observes;
import javax.jms.Message;
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonObjectBuilder;
import javax.json.JsonValue;
import javax.websocket.CloseReason;
import javax.websocket.EndpointConfig;
import javax.websocket.OnClose;
import javax.websocket.OnError;
import javax.websocket.OnMessage;
import javax.websocket.OnOpen;
import javax.websocket.Session;
import javax.websocket.server.ServerEndpoint;

import com.ibm.websphere.samples.daytrader.TradeAction;
import com.ibm.websphere.samples.daytrader.util.Log;
import com.ibm.websphere.samples.daytrader.util.WebSocketJMSMessage;


/** This class is a WebSocket EndPoint that sends the Market Summary in JSON form when requested 
 *  and sends stock price changes when received from an MDB through a CDI event
 * */

@ServerEndpoint(value = "/marketsummary",decoders=ActionDecoder.class)
public class MarketSummaryWebSocket {

    @Resource
    private ManagedScheduledExecutorService managedScheduledExecutorService;

	private static final List<Session> SESSIONS = new CopyOnWriteArrayList<>();
    private static final int SCHEDULER_PERIOD = Integer.parseInt(System.getProperty("dt.ws.period", "2"));
    private final CountDownLatch latch = new CountDownLatch(1);

    private static boolean sendRecentQuotePriceChangeList = false;
    private static ScheduledFuture<?> scheduler = null;


    @OnOpen
    public void onOpen(final Session session, EndpointConfig ec) {
        if (Log.doTrace()) {
            Log.trace("MarketSummaryWebSocket:onOpen -- session -->" + session + "<--");
        }

        synchronized(SESSIONS) {
            if (SESSIONS.size() == 0) {
                 if (Log.doTrace()) {
                    Log.trace("MarketSummaryWebSocket:onOpen -- start scheduler");
                 }
                startScheduler();
            }

            SESSIONS.add(session);
        }
  
        latch.countDown();
    } 
    
    @OnMessage
    public void sendMarketSummary(ActionMessage message, Session currentSession) {

        String action = message.getDecodedAction();
        
        if (Log.doTrace()) {
            if (action != null ) {
                Log.trace("MarketSummaryWebSocket:sendMarketSummary -- received -->" + action + "<--");
            } else {
                Log.trace("MarketSummaryWebSocket:sendMarketSummary -- received -->null<--");
            }
        }

        // Make sure onopen is finished
        try {
            latch.await();
        } catch (InterruptedException e) {
            e.printStackTrace();
            return;
        }
        
        if (action != null && action.equals("update")) {
            TradeAction tAction = new TradeAction();
                            
            JsonObject mkSummary = null;
            try {
                mkSummary = tAction.getMarketSummary().toJSON();
            } catch (Exception e) {
                e.printStackTrace();
                return;
            }

            if (Log.doTrace()) {
                Log.trace("MarketSummaryWebSocket:sendMarketSummary -- sending -->" + mkSummary + "<--");
            }
                            
            if (RecentStockChangeList.isEmpty()) {
                synchronized (currentSession) {
                    if (currentSession.isOpen()) {
                        try {
                            currentSession.getBasicRemote().sendText(mkSummary.toString());
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                }   
            }
            else { // Merge Objects 
                JsonObject recentChangeList = RecentStockChangeList.stockChangesInJSON();
                if (currentSession.isOpen()) {
                    try {
                        currentSession.getBasicRemote().sendText(mergeJsonObjects(mkSummary,recentChangeList).toString());
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                } 
            }
        }
    }

    @OnError
    public void onError(Throwable t, Session currentSession) {
        if (Log.doTrace()) {
            Log.trace("MarketSummaryWebSocket:onError -- session -->" + currentSession + "<--");
        }
        t.printStackTrace();
    }

    @OnClose
    public void onClose(Session session, CloseReason reason) {

        if (Log.doTrace()) {
            Log.trace("MarketSummaryWebSocket:onClose -- session -->" + session + "<--");
        }

        synchronized(SESSIONS) {
            SESSIONS.remove(session);
            if (SESSIONS.size() == 0) {  
                if (Log.doTrace()) {
                    Log.trace("MarketSummaryWebSocket:onClose -- cancel scheduler");
                }
                scheduler.cancel(false);
            }
        }

    }
    
    public static void onJMSMessage(@Observes @WebSocketJMSMessage Message message) {
    	
    	if (Log.doTrace()) {
            Log.trace("MarketSummaryWebSocket:onJMSMessage");
        }
        RecentStockChangeList.addStockChange(message);
        sendRecentQuotePriceChangeList = true;
    }    

    private void sendRecentQuotePriceChangeList() {
        JsonObject stockChangeJson = RecentStockChangeList.stockChangesInJSON();
  
        for (Session session : SESSIONS) {
            synchronized (session) {
                if (session.isOpen()) {
                    try {
                        session.getBasicRemote().sendText(stockChangeJson.toString());
                    } catch (IOException e) {
                        e.printStackTrace();
                    }      
                }
            }
        }
    }
    

    private void startScheduler() {
		scheduler = managedScheduledExecutorService.scheduleAtFixedRate(() -> {
        Log.trace("MarketSummaryWebSocket: Executing static scheduled task at: " + System.currentTimeMillis());
        if (sendRecentQuotePriceChangeList) {
          Log.trace("MarketSummaryWebSocket: sendList = true");
          sendRecentQuotePriceChangeList();
          sendRecentQuotePriceChangeList = false;
        } else {
          Log.trace("MarketSummaryWebSocket: sendList = false");
        }
      }, 1, SCHEDULER_PERIOD, TimeUnit.SECONDS);
	}
    
    private JsonObject mergeJsonObjects(JsonObject obj1, JsonObject obj2) {
        
        JsonObjectBuilder jObjectBuilder = Json.createObjectBuilder();
        
        Set<String> keys1 = obj1.keySet();
        Iterator<String> iter1 = keys1.iterator();
        
        while(iter1.hasNext()) {
            String key = (String)iter1.next();
            JsonValue value = obj1.get(key);
            
            jObjectBuilder.add(key, value);
            
        }
        
        Set<String> keys2 = obj2.keySet();
        Iterator<String> iter2 = keys2.iterator();
        
        while(iter2.hasNext()) {
            String key = (String)iter2.next();
            JsonValue value = obj2.get(key);
            
            jObjectBuilder.add(key, value);
            
        }
        
        return jObjectBuilder.build();
    }
}
