## Description
During the covid-19, it's hard for the pet owner to care for pets due to quarantine. As a result, we create a website for people nearby to take care of the pets. We use Django framework(HTML/CSS/JavaScripts as front end, Python as backend, MySQL as the database).

## Run the code
1.	Install dependencies
    ```
    pip install requirements.txt
    ```

2.	Initialize the database
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
    
3.  run the project
    ```
    python manage.py runserver
    ```
    Open your browser and type: `http://127.0.0.1:8000/main` or `http://localhost:8000/main`

## Features
1. Search for a breeder near you and order services
   Search nearby breeders by pet type, address, time, etc. and order the services they offer (boarding, dog walking, house sitting, etc.)
   
2. 1-1 Chat
    During the transaction, customers can chat one-on-one with the breeder in real time, exchange information about their pets, and ask each other to send photos to find out the latest status of their pets.

3. Rate the breeder
   After the transaction is completed, you can rate and evaluate the breeder.
 
4. Pet blog
  Communicate with pet lovers, post articles, view articles, comment on articles, and click on the article author's or commenter's avatar below to enter a one-on-one chat room.
