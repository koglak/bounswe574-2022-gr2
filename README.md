SWE573 SOFTWARE DEVELOPMENT PRACTICE BOUN 2022 SPRING
=====

This file has been created as guide for the project.

Project Overview
-----

**Welcome to my repository!**  🥳

This is a guidance that I will complete whole instructions of the lecture throughout the semester. Throughout the semester, I developed a collaborative learning environment where people can easily interact and improve themselves. My project name is "Helloworld"! 

**Check [Deliverables Table](https://github.com/koglak/SWE573/wiki/Deliverables-Table)!**

Topics
-----

<strong> Week1: </strong> Introduction, Logistics, Overview

<strong> Week2: </strong> Effective use of Software Development Tools

<strong> Week3: </strong> Requirements Specificaiton - Elicitation and SRS preperation

<strong> Week4: </strong> Plan - Work, Milestones, Deliverables

<strong> Week5: </strong> Design: Use case, Class and Sequence diagrams

<strong> Week6: </strong> Implementation: Continuous implementation with proper practices

<strong> Week7: </strong> Testing: User Testing

<strong> Week8: </strong> Virtualization and Deployment


Instructions to install app
-----

**Check deployed app: http://ec2-44-202-83-160.compute-1.amazonaws.com/**

## Prerequisites

*  Python: [Download Python](https://www.python.org/downloads/)
*  Django: `python -m pip install Django`
*  Virtual Environment: `python -m venv myvenv`    
*  PostgreSQL: [Download PostgreSQL](https://www.postgresql.org/download/)


1. Clone repository:

        git clone https://github.com/koglak/SWE573.git
        
2. Activate virtual environment:
      
        python3 -m venv myvenv
        
3. Run requirments:

        pip install -r requirements.txt
        
4. Create docker images:

        docker build . -t <container_name>
        
5. Run docker container:

        docker-compose up

6. Go to your local host: [http://localhost](http://127.0.0.1:8000/)
