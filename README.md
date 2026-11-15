
# Security Log Monitoring and Threat Detection API

## Project Overview
A Python FastAPI application that monitors simulated security login events and detects possible brute-force attacks.

## Features
- Health check endpoint
- Security event submission
- Failed login monitoring
- Brute-force alert generation
- IP address validation

## Technologies
- Python
- FastAPI
- Pytest
- Jenkins
- Ansible
- Docker
- Kubernetes

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn security_log_api.main:app --app-dir src --reload
```

Open API documentation:

http://127.0.0.1:8000/docs

## Run Tests

```bash
PYTHONPATH=src pytest tests/ -v
```

