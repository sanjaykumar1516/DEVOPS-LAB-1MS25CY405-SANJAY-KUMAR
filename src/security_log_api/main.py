
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from collections import defaultdict
import ipaddress

app = FastAPI(
    title="Security Log Monitoring API",
    description="Detects suspicious login activity",
    version="1.0.0"
)

# Store security events in memory
events = []
failed_attempts = defaultdict(int)
alerts = []

# Threshold for suspicious login activity
MAX_FAILED_ATTEMPTS = 5


class SecurityEvent(BaseModel):
    source_ip: str
    username: str
    event_type: Literal["failed_login", "successful_login"]


@app.get("/")
def home():
    return {
        "message": "Security Log Monitoring API is running"
    }


@app.post("/events")
def submit_event(event: SecurityEvent):

    # Validate IP address
    try:
        ipaddress.ip_address(event.source_ip)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid IP address"
        )

    # Store event
    record = event.model_dump()
    events.append(record)

    if event.event_type == "failed_login":

        failed_attempts[event.source_ip] += 1

        if failed_attempts[event.source_ip] == MAX_FAILED_ATTEMPTS:

            alert = {
                "source_ip": event.source_ip,
                "username": event.username,
                "failed_attempts": MAX_FAILED_ATTEMPTS,
                "alert": "Possible brute-force attack"
            }

            alerts.append(alert)

    elif event.event_type == "successful_login":
        failed_attempts[event.source_ip] = 0

    return {
        "message": "Security event recorded",
        "total_events": len(events)
    }


@app.get("/alerts")
def get_alerts():
    return {
        "total_alerts": len(alerts),
        "alerts": alerts
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Security Log Monitoring API"
    }
