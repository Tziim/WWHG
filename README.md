# Our vision:
#### https://app.diagrams.net/#G1nocvMKmed4BNdgx2SBwohUJZ_-FVUWY2

# How to Run the Project:

To run this project, follow these steps:

**Step 1**: Download the project by clicking on the "Download ZIP" button.

**Step 2**: Extract the downloaded zip file to a directory of your choice.

**Step 3**: Open a command prompt (CMD) in the same directory where the `manage.py` file is located.

**Step 4**: Run the following commands one by one:

    pip install -r requirements.txt

    python manage.py makemigrations

    python manage.py migrate

    python manage.py runserver

**Step 5**: Make new database in your `MySQL Workbench`:

    CREATE DATABASE IF NOT EXISTS wwhg_db;

**Step 6**:  For accessing the admin panel and creating a superuser, execute the following command:

    python manage.py createsuperuser

# Demo video:

#### https://youtu.be/QHpJ_4J1BsU
