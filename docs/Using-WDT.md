## Eclipse / WDT

The WebSphere Development Tools (WDT) for Eclipse can be used to control the server (start/stop/dump/etc.), it also supports incremental publishing with minimal restarts, working with a debugger to step through your applications, etc.

WDT also provides:

* content-assist for server configuration (a nice to have: server configuration is minimal, but the tools can help you find what you need and identify finger-checks, etc.)
* automatic incremental publish of applications so that you can write and test your changes locally without having to go through a build/publish cycle or restart the server (which is not that big a deal given the server restarts lickety-split, but less is more!).

Installing WDT on Eclipse is as simple as a drag-and-drop, but the process is explained [on wasdev.net] [wasdev-wdt].

*Note: Start eclipse with a full SDK, not a JRE.*

[wasdev-wdt]: https://developer.ibm.com/wasdev/downloads/liberty-profile-using-eclipse/

### Clone Git Repo
:pushpin: [Switch to cmd line example](/docs/Using-cmd-line.md/#clone-git-repo)

If the sample git repository hasn't been cloned yet, WDT has git tools integrated into the IDE:

1.  Open the Git repositories view
    * *Window -> Show View -> Other*
    * Type "git" in the filter box, and select *Git Repositories*
2.  Copy Git repo url by finding the textbox under "HTTPS clone URL" at the top of this page, and select *Copy to clipboard*
3.  In the Git repositories view, select the hyperlink `Clone a Git repository`
4.  The git repo url should already be filled in.  Select *Next -> Next -> Finish*
5.  The "sample.daytrader7 [master]" repo should appear in the view

### Building the sample in Eclipse
:pushpin: [Switch to cmd line example](/docs/Using-cmd-line.md/#building-the-sample)

This sample can be built using either [Gradle](#building-with-gradle) or [Maven](#building-with-maven).

#building-with-gradle
#### Building with [Gradle](http://gradle.org/)

###### Import Gradle projects into WDT

This assumes you have the Gradle [Buildship](https://projects.eclipse.org/projects/tools.buildship) tools installed into Eclipse Mars.

1. In the Git Repository view, expand the daytrader7 repo to see the "Working Directory" folder
2. Right-click on this folder, and select *Copy path to Clipboard*
3. Select menu *File -> Import -> Gradle -> Gradle Project*
4. In the *Project root directory* folder textbox, Paste in the repository directory.
5. Click *Next* twice
6. Five projects should be listed in the *Gradle project structure* click *Finish*
7. This will create 5 projects in Eclipse: sample.daytrader7, daytrader-ee7, daytrader-ee7-ejb, daytrader-ee7-web, daytrader-ee7-wlpcfg
8. Go to the *Gradle Tasks* view in Eclipse and navigate to the *sample.daytrader7* project
9. Double click on the *eclipse* task to generate all the Eclipse files
10. In the *Enterprise Explorer* view in Eclipse right click on the five projects mentioned in step 7 and click refresh

:star: *Note:* If you did not use Eclipse/WDT to clone the git repository, follow from step 3, but navigate to the cloned repository directory rather than pasting its name in step 4.

###### Run Gradle build

1. Go to the *Gradle Tasks* view in Eclipse and navigate to the *sample.daytrader7* project
2. Double click: build

#building-with-maven
#### Building with [Maven](http://maven.apache.org/)

###### Import Maven projects into WDT

1.  In the Git Repository view, expand the daytrader7 repo to see the "Working Directory" folder
2.  Right-click on this folder, and select *Copy path to Clipboard*
3.  Select menu *File -> Import -> Maven -> Existing Maven Projects*
4.  In the Root Directory textbox, Paste in the repository directory.
5.  Select *Browse...* button and select *Finish* (confirm it finds 5 pom.xml files)
6.  This will create 5 projects in Eclipse: sample.daytrader7, daytrader-ee7, daytrader-ee7-ejb, daytrader-ee7-web, daytrader-ee7-wlpcfg

:star: *Note:* If you did not use Eclipse/WDT to clone the git repository, follow from step 3, but navigate to the cloned repository directory rather than pasting its name in step 4.

###### Run Maven install

1. Right-click on sample.daytrader7/pom.xml
2. *Run As > Maven build...*
3. In the *Goals* section enter "install"
4. Click *Run*

### Running the application locally
:pushpin: [Switch to cmd line example](/docs/Using-cmd-line.md/#running-the-application-locally)

Pre-requisite: [Download WAS Liberty](/docs/Downloading-WAS-Liberty.md)

For the purposes of this sample, we will create the Liberty server (step 3 in the wasdev.net instructions) a little differently to create and customize a Runtime Environment that will allow the server to directly use the configuration in the `daytrader-ee7-wlpcfg` project.

###### Create a Runtime Environment in Eclipse

1. Open the 'Runtime Explorer' view:
    * *Window -> Show View -> Other*
    * type `runtime` in the filter box to find the view (it's under the Server heading).
2. Right-click in the view, and select *New -> Runtime Environment*
3. Give the Runtime environment a name, e.g. `wlp-2015.6.0.0` if you're using the June 2015 beta.
4. Either:
    * Select an existing installation (perhaps what you downloaded earlier, if you followed those instructions), or
    * select *Install from an archive or a repository* to download a new Liberty archive.
    * Choose an option with Java EE7 Full Platform.  
5. Follow the prompts (and possibly choose additional features to install) until you *Finish* creating the Runtime Environment

###### Add the User directory from the maven or Gradle project, and create a server

1. Right-click on the Runtime Environment created above in the 'Runtime Explorer' view, and select *Edit*
2. Click the `Advanced Options...` link
3. If the `daytrader-ee7-wlpcfg` directory is not listed as a User Directory, we need to add it:
    1. Click New
    2. Select the `daytrader-ee7-wlpcfg` project
    3. Select *Finish*, *OK*, *Finish*
4. Right-click on the `daytrader-ee7-wlpcfg` user directory listed under the target Runtime Environment in the Runtime Explorer view, and select *New Server*.
5. The resulting dialog should be pre-populated with the `daytrader7Sample` Liberty profile server.
   The default name for this server can vary, you might also opt to rename it from the Right-click menu in the Servers view to make it easier to identify.
6. Click *Finish*


###### Running Liberty, the sample application, and populating the database from WDT

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

1.  Select the Servers tab
2.  Right-click on the appropriate server (as created above) and select *Start* (For now, ignore any EJB errors) 
3.  Confirm web browser opens on "http://localhost:9082/daytrader/" or "http://localhost:9082/daytrader/index.faces"
4.  In the web browser, Click on the configuration tab.
5.  Click on '(Re)-create  DayTrader Database Tables and Indexes' to create the database.
6.  Click on '(Re)-populate  DayTrader Database' to populate the database.
7.  Back on the Servers tab,  Right-click on the appropriate server (as created above) and select *Restart*-> .  Now the application will be ready for use.

#### Tips

* When importing the existing maven project into Eclipse, Eclipse will (by default) "helpfully" add this project to an (extraneous) ear. To turn this off, go to Preferences -> Java EE -> Project, and uncheck "Add project to an EAR" before you import the project. If you forgot to do this, just delete the ear project; no harm.
