import requests
import json

class Canvas():
    def __init__(self, URL: str, TOKEN: str):
        self.API_URL = URL
        self.MY_TOKEN = TOKEN
        self.HEADERS = {"Authorization": "Bearer " + self.MY_TOKEN}

    def get_course_data(self) -> list:
        """Finds currently enrolled course names, IDs, and assignments

        Returns:
            list: List of dictionaries filled with course name, id, and list of assignments 
        """
        response = requests.get(f"{self.API_URL}/courses?enrollment_state=active", headers=self.HEADERS)
        courses = []
        for course in response.json():
            courses.append({"name": course["name"], 
                            "id": course["id"], 
                            "assignments": self.__get_assignments(course["id"]), 
                            "quizzes": self.__get_quizzes(course["id"])})
        return courses

    def __get_assignments(self, course_id: str) -> list:
        """Helper function for method get_course_data() to get course assignments using course id

        Args:
            course_id (str): 6 digit id specific to course

        Returns:
            list: Name of all assignments in course (str)
        """
        response = requests.get(f"{self.API_URL}/courses/{course_id}/assignments", headers=self.HEADERS)
        assignments = []
        for assignment in response.json():
            assignments.append(assignment["name"])
        return assignments
    
    def __get_quizzes(self, course_id: str) -> list:
        """Helper function for method get_course_data() to get course quizzes using course id

        Args:
            course_id (str): 6 digit id specific to course

        Returns:
            list: Name of all quizes in course (str)
        """
        try:
            response = requests.get(f"{self.API_URL}/courses/{course_id}/quizzes", headers=self.HEADERS)
            quizzes = []
            for quiz in response.json():
                quizzes.append(quiz["title"])
            return quizzes
        except Exception as e:
            # Some JSON data does not have a "title"
            print(f"Course ID: {course_id} has disabled access")
            return quizzes # empty list
    
    def print_courses_and_assignments(self):
        for course in self.get_course_data():
            if course["assignments"] and course["quizzes"]:
                print(f"{course["name"]}: {course["id"]}")
                print(course["assignments"])
                print(course["quizzes"])
                print()
            elif course["assignments"]:
                print(f"{course["name"]}: {course["id"]}")
                print(course["assignments"])
                print()
            elif course["quizzes"]:
                print(f"{course["name"]}: {course["id"]}")
                print(course["quizzes"])
                print()
            else:
                print(course["name"])
                print()