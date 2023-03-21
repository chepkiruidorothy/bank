## Bank App
This is a simple bank app.

# Features:

- Create a new account
- Deposit money
- Withdraw money
- Send money to other accounts
- Receive money

# Getting Started

To run the app locally, you need to have the following software installed on your computer:

- Python 3
- Django
- PostgreSQL

You also need to set up a PostgreSQL database and configure the app to use it. To do this, follow these steps:

Create a new database in PostgreSQL using the following command:

```python
createdb bank
```
Open the bank_app/settings.py file and update the DATABASES setting with your PostgreSQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bank',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Make sure to replace your_username and your_password with your actual PostgreSQL credentials.

Install the app dependencies using the following command:

```python
pip install -r requirements.txt
```
Run database migrations using the following command:

```python
python manage.py migrate
```
Create a superuser account using the following command:

```python
python manage.py createsuperuser
```
Follow the prompts to create a new superuser account.

Run the app using the following command:

```python
python manage.py runserver
```
The app should now be running on http://localhost:8000.

# Usage

To use the app, open a web browser and navigate to http://localhost:8000. You should see a login page where you can enter your credentials to access your account.

Once you're logged in, you can perform various actions such as viewing your account balance, depositing or withdrawing funds, transferring money to other accounts, and sending or receiving money to/from other users.

# Contributing
If you'd like to contribute to this project, feel free to submit a pull request or open an issue. We welcome all contributions and feedback!


