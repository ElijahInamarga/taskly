import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_URL = os.getenv("API_URL")
my_token = os.getenv("CANVAS_TOKEN")
headers = {"Authorization": "Bearer " + my_token}

def get_courses() -> list:
    response = requests.get(f"{API_URL}/courses?enrollment_state=active", headers=headers)
    courses = []
    for course in response.json():
        courses.append({"name": course["name"], "assignments": get_assignments(course["id"])})
    return courses

def get_assignments(course_id : str) -> list:
    response = requests.get(f"{API_URL}/courses/{course_id}/assignments", headers=headers)
    assignments = []
    for assignment in response.json():
        assignments.append(assignment["name"])
    return assignments

if __name__ == "__main__":
    # Temporary
    for course in get_courses():
        if course["assignments"]:
            print(course["name"] + ": ")
            print(course["assignments"])
        else:
            print(course["name"])
