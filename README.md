# sample.daytrader7 [![Build Status](https://travis-ci.org/WASdev/sample.daytrader7.svg?branch=master)](https://travis-ci.org/WASdev/sample.daytrader7)

# Java EE7: DayTrader7 Sample

Java EE7 DayTrader7 Sample


This sample contains the DayTrader 7 benchmark, which is an application built around the paradigm of an online stock trading system. The application allows users to login, view their portfolio, lookup stock quotes, and buy or sell stock shares. With the aid of a Web-based load driver such as Apache JMeter, the real-world workload provided by DayTrader can be used to measure and compare the performance of Java Platform, Enterprise Edition (Java EE) application servers offered by a variety of vendors. In addition to the full workload, the application also contains a set of primitives used for functional and performance testing of various Java EE components and common design patterns.

DayTrader is an end-to-end benchmark and performance sample application. It provides a real world Java EE workload. DayTrader's new design spans Java EE 7, including the new WebSockets specification. Other Java EE features include JSPs, Servlets, EJBs, JPA, JDBC, JSF, CDI, Bean Validation, JSON, JMS, MDBs, and transactions (synchronous and asynchronous/2-phase commit).

This sample can be installed onto WAS Liberty runtime versions 8.5.5.6 and later. A prebuilt derby database is provided in resources/data

To run this sample, first [download](https://github.com/WASdev/sample.daytrader7/archive/master.zip) or clone this repo - to clone:
```
git clone git@github.com:WASdev/sample.daytrader7.git
```

From inside the sample.daytrader7 directory, build and start the application in Open Liberty with the following command:
```
mvn install
cd daytrader-ee7
mvn liberty:run
```

Once the server has been started, go to [http://localhost:9082/daytrader](http://localhost:9082/daytrader) to interact with the sample.

## Notice

© Copyright IBM Corporation 2015.

## License

```text
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
````
