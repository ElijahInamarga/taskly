import os
from dotenv import load_dotenv
from package import Canvas

load_dotenv()
API_URL = os.getenv("API_URL")
MY_TOKEN = os.getenv("CANVAS_TOKEN")

if __name__ == "__main__":
    canvas = Canvas(API_URL, MY_TOKEN)
    
    # Temporary
    for course in canvas.get_courses():
        if course["assignments"]:
            print(course["name"] + ": ")
            print(course["assignments"])
        else:
            print(course["name"])
