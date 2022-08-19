This repo contains the files necessary to run the microservice that solves the Fetch Backend Engineering exercise.

### Running the app
There are a couple of ways to run and interact with this app. These instructions assume a basic understanding of github and Python specifically. You will need Python version 3.9 or higher to run this app without errors.

#### Option 1: Run locally
Clone the repo to your local machine. This app requires a few Python libraries that are not part of the standard library and need to be installed. Install these requirements using pip (a virtual environment is recommended, but not required). From the top-level directory:

```console
pip install -r requirements.txt
```

Once all required libraries are installed, run the app from the top-level directory (`fetch-backend-exercise`) with the command:
```console
uvicorn app.main:app
```

You should see something similar to the below, which indicates the app is running locally:
```console
❯ uvicorn app.main:app         
INFO:     Started server process [65094]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
A truncated description of the exercise is as follows:

Create a simple webservice that accepts HTTP requests and returns responses based on conditions outlined below.

The repo has the following folder structure:


```console
fetch-backend-exercise/
├── __init__.py
├── database.py
├── main.py
├── models.py
├── README.md
├── requirements.txt
├── schemas.py
```

`database.py` contains code that defines the sqlite database used to store
