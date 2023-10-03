# ETL OFF A SQS QUEUE

## Table of Contents
### Objective
### Getting Started
### Prerequisites
### Installation
### Acknowledgements

## Objective
  1. Read JSON data containing user login behavior from an AWS SQS Queue, that is made
  available via a custom localstack image that has the data pre loaded.
  2. Hiding personal identifiable information (PII) should be implemented. The fields `device_id` and `ip`
  should be masked, but in a way where it is easy for data analysts to identify duplicate
  values in those fields.
  3. Once you have flattened the JSON data object and masked those two fields, write each
  record to a Postgres database that is made available via a custom postgres image that
  has the tables pre created.
      ## Note the target table's DDL is:
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
## Installation on Mac 
1) Install Docker on local machine using the link: https://docs.docker.com/get-docker/  
2) Run pip install awscli-local on the command line  
   If pip is not previously installed, First install Python and run pip command  
3) Install Postgresql using the link:  https://www.enterprisedb.com/downloads/postgres-postgresql-downloads  
### AWS Services and PostgresSQL Setup 
1) Once Docker is installed properly, make sure the Docker is started and running.  
   Mac shows a green light with Running on the top of the desktop bar once the Installation is completed
2)  Docker Images:
  Download the localstack and postgressql images from the below links:
    https://hub.docker.com/r/fetchdocker/data-takehome-postgres
    https://hub.docker.com/r/fetchdocker/data-takehome-localstack
