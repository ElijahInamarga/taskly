import requests

class Canvas():
    """Canvas API class
    
    Constructor Arguments:
        URL {str} -- Link to canvas API specific to each school/university
        TOKEN {str} -- Your own canvas API token (Generate from canvas)
    """
    
    def __init__(self, URL: str, TOKEN: str):
        self.API_URL = URL
        self.MY_TOKEN = TOKEN
        self.headers = {"Authorization": "Bearer " + self.MY_TOKEN}

    def get_courses(self) -> list:
        response = requests.get(f"{self.API_URL}/courses?enrollment_state=active", headers=self.headers)
        courses = []
        for course in response.json():
            courses.append({"name": course["name"], "assignments": self.__get_assignments(course["id"])})
        return courses

    def __get_assignments(self, course_id : str) -> list:
        response = requests.get(f"{self.API_URL}/courses/{course_id}/assignments", headers=self.headers)
        assignments = []
        for assignment in response.json():
            assignments.append(assignment["name"])
        return assignments
    
    def print_courses_and_assignments(self):
        for course in self.get_courses():
            if course["assignments"]:
                print(course["name"] + ": ")
                print(course["assignments"])
            else:
                print(course["name"])