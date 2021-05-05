# Bhavcopy Equities

Everyday BSE releases data of the performance of all equities of that day over [here](https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx).<br>
This web application helps to view the performance of all the equities on that day by showin:
* equity code
* open
* close
* high
* low

features of the equity in a consolidated view.<br>
The application allows you to search for certain equities and download them in the form of a CSV file for personal usage.

The technology stack used is:

* Django
    * Django is used to serve up the application and providing a framework for database and frontend to interact with each other.

* Vue
    * Vue is used in the frontend of the application.

* Redis
    * Redis is used as the database in this application. All data regarding the equities are stored and fetched from redis.

* Celery
    * Celery is used for periodically running the task of downloading the Bhavcopy of the current day equity statistics at 6pm.

## Application setup
___After setting up the application via running the below steps, please wait till 6pm for the database to be populated. This is only a one time thing so don't worry! ;)___

Ensure you have git installed.<br>
Open your terminal(Linux/Mac) or command window(Windows).<br>

Run command -> `git clone https://github.com/pranav1601/bhavcopy-equities.git`<br>
Run command -> `cd bhavcopy-equities`<br>

This application requires your system to have pip installed on your system. You can head over [here](https://pip.pypa.io/en/stable/installing/) to install pip. There are 2 ways to setup the application further.

### Using Docker

This method requires your system to have Docker Engine and Docker Compose to be installed. Head over [here](https://docs.docker.com/engine/install/) and [here](https://docs.docker.com/engine/install/) for their installation respectively.<br>

Run command -> `docker-compose up --build`<br>
_If facing permission error please add `sudo` before the above command_

The application will be served on `http://0.0.0.0:8000`.

### Without Docker

This method required you to have Python, django, redis, Celery, and django_celery_beat installed.
Head over [here](https://www.python.org/downloads/) to install Python.<br>
Run the following command on the terminal:<br>
`pip install -r requirements.txt`<br>

Then run:<br>
`redis-server`<br>

Open another terminal and run the following command:<br>
`.\manage.py runserver`<br>

Open another terminal and run the following command:<br>
`celery -A bhavcopy worker -B -l INFO`<br>

The application will be served up on `http://127.0.0.1:8000`.



