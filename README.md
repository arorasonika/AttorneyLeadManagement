# Attorney Lead Management
Backend service using FastAPI for attorneys to manage the status of prospects and their data

**All APIs implemented:**

- API to get all the submitted leads (access restricted to authenticated attorneys only)
- API to update the state of a submitted lead (access restricted to authenticated attorneys only)
- API to delete all the submitted leads (access restricted to authenticated attorneys only)
- API to submit a lead form (unrestricted)
- Login API (unrestricted)
- API to get active user details (access restricted to authenticated attorney only)

**Steps needed to start the server:**

From alma_project directory and execute the following steps in the terminal:

This project is built using Python 3.12.3. Ensure you have atleast python version 3.11.6 to ensure all parts work as intended. 

Create a python virtual environment using steps here: https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/ 

Create the virtual environment: python3.11 -m venv venv

Activate the virtual environment: source venv/bin/activate

Install requirements.txt: pip install -r requirements.txt

Create a .env file in the project directory with the following: 
This is the email and app password used for sending the email when a lead is submitted. 
To generate app password for your gmail account, refer to: https://support.google.com/accounts/answer/185833?hl=en

ATTORNEY_EMAIL_ID=xxx@xxxx.com
ATTORNEY_EMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

Run the project by typing in terminal: uvicorn lead_management.app.main:app --reload

This should start the app at: http://127.0.0.1:8000 and you can head over to http://127.0.0.1:8000/docs to view all the available APIs.

If you wish to use test_leads.py to run the pytests: 
Look for #TODO: Change test email in test_leads.py and modify the "email": <enter test email> with the lead’s email you want to test with.
Run the file: python test_leads.py to see print outputs or use pytest test_leads.py to see pytest results. 
NOTE: This testing only works on unauthenticated APIs


**Usage:** 

Start the backend service by typing this in the terminal: uvicorn lead_management.app.main:app --reload

Head over to http://127.0.0.1:8000/docs to view the implemented APIs and try them out 

Documentation for how to navigate this page:  https://swagger.io/tools/swagger-ui/ 

For the APIs which show a lock symbol, click the lock and authenticate with the following username and password which is dummy data created for the purpose of testing logging in functionality:
Username: johndoe
Password: secret
OR
Username: alice
Password: secret2

**More details about login implementation:**

Warning: It is by no means an implementation of industry standards. It is set up in a basic way to use FastAPI login functionality using some fake attorney details. This is done keeping time and simplicity in mind for this project. It simulates how login would affect APIs. 


2 fake attorneys are created for sake of simplicity in a dictionary in main.py to simulate the login flow. You may use any of their username and passwords to login to execute the following apis:

- API to get all the submitted leads
- API to update the state of a submitted lead
- API to delete all the submitted leads
