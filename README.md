# Account Management Flask App
Project Name: Account_management
Project Name: Account_management
Project Owner: 蕭逸
Docker Hub: https://hub.docker.com/r/s1021332/account_management-flask-app

Project Objective:
Design and implement two RESTful HTTP APIs for creating and verifying an account and password. The solution should accept a JSON payload as input and return a JSON payload as output, with appropriate error handling and input validation. The implementation should be in Python and must follow RESTful style principles, including the use of HTTP methods (GET, POST, PUT, DELETE), resource naming, and HTTP status codes. The solution must also be packaged in a Docker container, pushed to Docker Hub, and hosted in a GitHub repository. Additionally, please provide an API document and user guide on how to run the container with Docker.
 
## Table of Contents

- [Prerequisites](#prerequisites)
- [API Documentation](#apidocumention)
- [User Guide](#user-guide)

## Prerequisites

1.Ensure Docker is installed on your system
2.Ensure Postman is installed on your system
3.Having a Docker Hub account.

## API Documentation
API 1: /accounts
Method: ‘Post’
Description: Create an account
Condition:
    "username": a string representing the desired username for the account, with a
                minimum length of 3 characters and a maximum length of 32 characters.
    "password": a string representing the desired password for the account, with a
                minimum length of 8 characters and a maximum length of 32 characters, containing at least 1 uppercase letter, 1 lowercase letter, and 1 number.
    
HTTP Status Codes:
1. ‘201 OK’: Account successfully created.
2. ‘400 Bad request’: Failure reason
3. ‘500 Error’: Internal Server error.
 

API 2: /accounts/verify
Method: ‘Post’
Description: Verify Account & Password
 Condition:
    "username": a string representing the username of the account being accessed.
    "password": a string representing the password being used to access the account.

HTTP Status Codes:
	’200 OK’: Password verify successfully.
	‘400 Bad request’: Failure reason 
	‘429 Attempt failure: Too many attempts, If the password verification fails five times, the user should wait one minute before attempting to verify the password again.
 
## User Guide
The User Guide will take you through how to pull the Docker image from Docker Hub, set up the MySQL database, and run the Flask application container.


Step1.Pulling the Docker Image from Docker Hub
1.	Login the Docker Hub
Open the terminal and login to Docker Hub
Commend:
    "docker login"
 
2.	Pull the Docker Image
Pull the Flask API Docker Image form Docker Hub
Commend:
    "docker pull s1021332/account_managment-flask-app"

3.  Setting Up the MySQL Database
Run the MySQL Container.
Commend:
    "docker run --name some_mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=some_mysql -p 3307:3306 -d mysql:latest"
 
4.  Connect Flask Application Container with MySQL Container 
Commend:
    "docker run --name flask-app-container --link some_mysql:db -p 5000:5000 -d s1021332/account_management-flask-app"

5.  Check containers status
The MySQL container (some_mysql) is running on Port 3307:3306 and the Flask Application (flask-app-container) is running on Port 5000:5000
 

6.  Use Postman to run the Flask Application Container
 
Based on the API documentation, input the corresponding API method and parameters, then execute it on localhost:5000. Click "send," and the output field will display the corresponding execution results.




Access the APIs:
You can now access the Flask application APIs using the following endpoints:
Create Account: POST http://localhost:5000/accounts
Verify Account: POST http://localhost:5000/accounts/verify

Step6. Stopping and Removing Containers
To stop and remove the running containers, you can use the following commands:
1.	Stop the Containers
 Commend:
    "docker stop flask-app-container some_mysql"

2.	Remove the Containers
  Commend:
    "docker rm flask-app-container some_mysql"

By following this guide, you should be able to successfully install Docker, pull the Docker image, set up the MySQL database, and run the Flask application container.
