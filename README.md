SWE574 SOFTWARE DEVELOPMENT AS A TEAM FALL 2022
=====

Project Overview
-----

**Helloworld** is an online platform where users can create new spaces to learn, discuss and develop each other. Within those spaces, users can create textual content to share their knowledge, quiz to test each other and competition by case-study feature to provide interactive environment. When user submitted a file to created case-study, other users can download the file to rate and grade the study. It allows to emerge collaborative environment where people can interact each other and criticize their studies. Space owner can add collaborative members to space who can modify space content as space owner can do. Other users can see all spaces, search them by either a keyword or tags. Moreover, if user enrols to a space, the space is listed learn page of the user. Beside all these features, Helloworld platform presents Question & Answer application in it where users can freely ask questions and take advantages of knowledge of the other members. Helloworld website is creative, interactive, and collaborative learning environment for all users.

Project Team
-----

| **No** | **Team Member** |
| --- | --- |
| 1 | [Kardelen Oğlakcıoğlu](https://github.com/koglak/)|
| 2 | [Mert Can Geyik](https://github.com/bharaddur)|
| 3 | [Sabahattin Erdem Turanlıoğlu](https://github.com/turanlioglu)|
| 4 | [Murat Mert Şentürk](https://github.com/musentur)|
| 5 | [Ömer Bahar](https://github.com/omerbahaar)|

## Prerequisites

*  Python: [Download Python](https://www.python.org/downloads/)
*  Docker: [Download Docker](https://docs.docker.com/desktop/install/windows-install/)


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

6. Go to your local host: [http://localhost:8000/](http://127.0.0.1:8000/)

7. Get your container id

        docker container ls
        
8. Create superuser for django admin

        docker exec -it container_id python manage.py createsuperuser
