# ETL OFF A SQS QUEUE

## Table of Contents
### Objective
### Prerequisites
### Installation and Setup
### Code Overview 

## Objective
  1. Read JSON data containing user login behavior from an AWS SQS Queue, that is made
  available via a custom localstack image that has the data pre loaded.
  2. Hiding personal identifiable information (PII) should be implemented. The fields `device_id` and `ip`
  should be masked, but in a way where it is easy for data analysts to identify duplicate
  values in those fields.
  3. Once you have flattened the JSON data object and masked those two fields, write each
  record to a Postgres database that is made available via a custom postgres image that
  has the tables pre created.
Note the target table's DDL is:  
   Creation of user_logins table:  
   CREATE TABLE IF NOT EXISTS user_logins(  
    user_id varchar(128),  
    device_type varchar(32),  
    masked_ip varchar(256),  
    masked_device_id varchar(256),  
    locale varchar(32),  
    app_version integer,  
    create_date date  
    );  
You will have to make a number of decisions as you develop this solution:  
● How will you read messages from the queue?  
● What type of data structures should be used?  
● How will you mask the PII data so that duplicate values can be identified?  
● What will be your strategy for connecting and writing to Postgres?  
● Where and how will your application run?  
## Prerequisites
1) Install Docker on local machine using the link: <https://docs.docker.com/get-docker/> 
2) Run pip install awscli-local on the command line  
   If pip is not previously installed, First install Python usoing - <https://www.python.org/downloads/macos/> and run pip command  
3) Install Postgresql using the link:  <https://www.enterprisedb.com/downloads/postgres-postgresql-downloads>
4) Install psycopg2 to connect to the postgresql using the command **pip install psycopg2**
## Installation and Setup
### AWS Services and PostgresSQL Setup 
1) Once Docker is installed properly, make sure the Docker is started and running.  
   Mac shows a green light with Running on the top of the desktop bar once the Installation is completed and Docker is started.  
2)  Docker Images:  
    <https://hub.docker.com/r/fetchdocker/data-takehome-postgres>  
    <https://hub.docker.com/r/fetchdocker/data-takehome-localstack>  
    To Download the localstack and postgressql images from the above links copy the url from the DOCKER PULL COMMAND and run it on the terminal.  
    The 2 images which are pulled will be displayed in the Docker hub application as well.  
4) To start the containers, run the below commands  
      docker run -p 5432:5432 fetchdocker/data-takehome-postgres:latest  
      docker run -p 4566:4566 fetchdocker/data-takehome-localstack:latest  
  Issues: If there is any conflicting port that needs to be killed.  
  Check for conflicting ports with sudo lsof -I :5432  
  Use Sudo kill <PID>  for killing the conflicting process   
6) Once the images are ready you should be able to check them using the **docker ps ** command from the terminal. This contains the CONTAINER ID, IMAGE, COMMAND, CREATED, STATUS and PORTS

## Code Overview 
1) After the Docker setup has been established, it is now time to structure our code to connect to both the endpoint URL's of AWS SQS and POSTGRES and establish connectivity
2) This is achieved in the code area as doc strings but to be brief
   Firstly, we require the end point url, queue url and connection strings for these connections.
   Next Steps:
     1) Using the AWS SDK connect to the SQS using dummy credentials(as we are using localstack to fake the aws services), provide region  
     2) Connect to postgres using the endpoint url and connection parameters like username,password etc  
     3) Using the receive message of sqs pull the messages from the queue and load it into flattened json object  
     4) PII data is masked using the Hash function to make sure duplicate values are having same hash when retrieved  
     5) The final output is ingested to postgresql into the user_logins table using the cursor.execute   
### Verifying the PostgresSQL table before executing the python code 
1) SSH to the postgres image **fetchdocker/data-takehome-localstack** using the below command. Container id is obtained from the previous step.  
     docker exec -it <container-id> /bin/bash  
2) After entering into the localstack container run the below command to go to postgres#  
    psql -d postgres -U postgres -p 5432 -h localhost -W  
   ** The Database, Username, Password is **postgres** **
3) If the tables doesnot exists create one as below:  
CREATE TABLE IF NOT EXISTS user_logins(  
user_id varchar(128),  
app_version varchar(100),  
device_type varchar(32),  
masked_ip varchar(256),  
locale varchar(32),  
masked_device_id varchar(256)  
);  
Finally, Execute the python code with the python3 userlogins.py
Final output is available as a snippet in the image.png file
