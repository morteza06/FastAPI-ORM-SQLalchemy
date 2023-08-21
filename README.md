# FastAPI 
 FastAPI is simple project from API developed in python with a lot of concept.
 
 
this project is a learning course from Sanjeev Thiyagarajan.
https://github.com/Sanjeev-Thiyagarajan/fastapi-course

**Description of all content:**

## In this course build simple API with full featuer includes: ##

- Authentication  
+ CRUD operation   
* Schema Validation    
- Setup  Documentation.

Dependency package for run project needs to insatll.
Authentication ==>  pip install python-jose [cryptography]  

Learning some SQL command that commented in the code.
Use SQL in two different methods : 
1. SQL query(postgresql = types of sql database)        
1. ORM(SQLALCHEMY = sql object oriented package in python) 
[pip install sqlalchemy]

For Create table and add column we need a Alembic package to migration Database in development projects.
So setup this package with this command.
 [pip install alembic]
 with some of commands ==> 
 [alembic --help]
 [alembic init alembic dir]
 [alembic revision --help]
 [alembic revision -m "create post table"]
 [upgarde , downgrade database in migration ]

## Setting up Github ##
use evnvironment variable for run dynamic setup at config.

### For test API app we needs to use Postman tools at 2 reason: ### 
1. http packet  
1. development.
Automation Integration Testing by pytest Done.

At the end for deployment API we use 2 different Senario:
1. Ubuntu. 
Create account cloude machine includes: 
-digital Ocean and Settings NGINX for use HTTP, HTTPS, PROXY settings. at the end we use access firewall for SSL in this machine.

1. Heroku: 
Create account cloude service and run app in runner processing.

Set settings a postgresql and run alembic in heroku
push source to github.

Run all project with Github Action runner and test them.


Create Docker file for API apps and generate image in dockers.
Use docker compose for app and run projects with a container.


