## Building and running the sample using the command line

### Clone Git Repo
:pushpin: [Switch to Eclipse example](/docs/Using-WDT.md/#clone-git-repo)

```bash

$ git clone https://github.com/WASdev/sample.daytrader7.git

```

### Building the sample
:pushpin: [Switch to Eclipse example](/docs/Using-WDT.md/#building-the-sample-in-eclipse)

This sample can be built using either [Gradle](#gradle-commands) or [Maven](#apache-maven-commands).

###### [Gradle](http://gradle.org/) commands

```bash
$ gradle build
```

If you want to also run the functional tests then you need to [Download WAS Liberty](/docs/Downloading-WAS-Liberty.md) and set the libertyRoot property in the gradle.properties file to point to your Liberty install.

###### [Apache Maven](http://maven.apache.org/) commands

```bash
$ mvn install
```

If you want to also run the functional tests then you need to [Download WAS Liberty](/docs/Downloading-WAS-Liberty.md) and pass in the location of your install as the system property libertyRoot:

```bash
$ mvn -DlibertyRoot=<LibertyInstallLocation> install
```

The built ear file is copied into the apps directory of the server configuration located in the daytrader-ee7-wlpcfg directory:

```text
daytrader-ee7-wlpcfg
 +- servers
     +- daytrader-ee7-wlpcfg                   <-- specific server configuration
        +- server.xml                          <-- server configuration
        +- apps                                <- directory for applications
           +- daytrader-ee7.ear                <- sample application
        +- logs                                <- created by running the server locally
        +- workarea                            <- created by running the server locally
```

### Running the application locally
:pushpin: [Switch to Eclipse example](/docs/Using-WDT.md/#running-the-application-locally)

Pre-requisite: [Download WAS Liberty](/docs/Downloading-WAS-Liberty.md)

Use the following to start the server and run the application:

```bash
$ export WLP_USER_DIR=/path/to/sample.daytrader7/daytrader-ee7-wlpcfg
$ /path/to/wlp/bin/server start daytrader7Sample

1.  Confirm web browser opens on "http://localhost:9082/daytrader/" or "http://localhost:9082/daytrader/index.faces"
2.  In the web browser, Click on the configuration tab.
3.  Click on '(Re)-create  DayTrader Database Tables and Indexes' to create the database.
4.  Click on '(Re)-populate  DayTrader Database' to populate the database.
5.  Restart the server-> .  Now the application will be ready for use.
$ /path/to/wlp/bin/server stop daytrader7Sample
$ /path/to/wlp/bin/server start daytrader7Sample
```

* `start` runs the server in the background. Look in the logs directory for console.log to see what's going on, e.g.
* `stop` stop the server in the background. Look in the logs directory for console.log to see what's going on, e.g.
* `run` runs the server in the foreground.

```bash
$ tail -f ${WLP_USER_DIR}/servers/daytrader7Sample/logs/console.log
```

