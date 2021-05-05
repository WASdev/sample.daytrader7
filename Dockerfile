FROM open-liberty:full

COPY --chown=1001:0 daytrader-ee7/src/main/liberty/config/server.xml /config/server.xml
COPY --chown=1001:0 daytrader-ee7/target/daytrader-ee7.ear /config/apps

COPY --chown=1001:0 daytrader-ee7/target/liberty/wlp/usr/shared/resources/DerbyLibs/derby-10.14.2.0.jar /opt/ol/wlp/usr/shared/resources/DerbyLibs/derby-10.14.2.0.jar
COPY --chown=1001:0 daytrader-ee7/target/liberty/wlp/usr/shared/resources/data /opt/ol/wlp/usr/shared/resources/data

#RUN configure.sh



