"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball tournaments",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create your own masterpieces",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "isabella@mergington.edu"]
    },
    "Drama Club": {
        "description": "Participate in plays and improve your acting skills",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["lucas@mergington.edu", "harper@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging math problems and prepare for competitions",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["elijah@mergington.edu", "charlotte@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["james@mergington.edu", "sophia@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn and practice tennis skills, and participate in matches",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 10,
        "participants": ["grace@mergington.edu", "henry@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.get("/activities/{activity_name}")
def get_activity(activity_name: str):
    """Get details of a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activities[activity_name]


class SignupRequest(BaseModel):
    email: EmailStr


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, signup_request: SignupRequest):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if signup_request.email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")

    # Validate maximum participants
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(signup_request.email)
    return {"message": f"Signed up {signup_request.email} for {activity_name}"}


@app.delete("/activities/{activity_name}/remove")
def remove_participant(activity_name: str, email: EmailStr):
    """Remove a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student not signed up for this activity")

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}


@app.delete("/activities/{activity_name}")
def delete_activity(activity_name: str):
    """Delete an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Delete activity
    del activities[activity_name]
    return {"message": f"Deleted activity {activity_name}"}
