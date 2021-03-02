# RideShare

### Introduction

This project is a cloud based RideShare application, that can be used to pool rides.
The RideShare application allows the users to create a new ride if they are travelling from Point A to Point B. The application can
* Add a new user
* Delete an existing user
* Create a new ride
* Search for an existing ride between a source and a destination
* Join an existing ride
* Delete a ride

### Design

The monolithic REST service is split up into 2 microservices - one catering to the user management, and another catering to the ride management.
These 2 microservices is started in separate docker containers running on one AWS instance. The microservices talk to each other via their respective REST interfaces.

For the rides microservice, the web server port within the container (usually 80) is mapped to localhost 8000. Similarly, for the users microservice, the web server port within the container (usually 80) is mapped to localhost 8080. Each microservice has it's own database running in the container itself. Nginx is used for each microservice.
