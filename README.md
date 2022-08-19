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

#### Option 2: Run with Docker
Coming soon...

### Interacting with the app
There are 4 endpoints that accept requests:
- `add-transaction` accepts POST requests representing points transactions that have the format:
    ```
    { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
    { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }
    { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }
    { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }
    { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }
    ```
