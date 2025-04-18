import requests

class Canvas():
    def __init__(self, URL: str, TOKEN: str):
        self.__API_URL = URL
        self.__MY_TOKEN = TOKEN
        self.__HEADERS = {"Authorization": "Bearer " + self.__MY_TOKEN}

    def get_course_data(self) -> list:
        """Finds currently enrolled course names, IDs, and assignments

        Returns:
            list: List of dictionaries filled with course name, id, and list of assignments 
            
            "courses": [
            {
                "name": "BIOL101",
                "id": "123456",
                "assignments": ['Homework 1', 'Homework 2', ...],
                "quizzes": [{'name': 'BIOL 101 Syllabus Quiz', 'due_date': '2025-02-15T07:59:00Z'}, {...}, ...]
            },
            {
                ...
            }]
        """
        response = requests.get(f"{self.__API_URL}/courses?enrollment_state=active", headers=self.__HEADERS)
        courses = []
        for course in response.json():
            courses.append({"name": course["name"], 
                            "id": course["id"], 
                            "assignments": self.__get_assignments(course["id"]), 
                            "quizzes": self.__get_quizzes(course["id"])})
        return courses

    def __get_assignments(self, course_id: str) -> list:
        response = requests.get(f"{self.__API_URL}/courses/{course_id}/assignments", headers=self.__HEADERS)
        assignments = []
        for assignment in response.json():
            assignments.append(assignment["name"])
        return assignments
    
    def __get_quizzes(self, course_id: str) -> list:
        try:
            response = requests.get(f"{self.__API_URL}/courses/{course_id}/quizzes", headers=self.__HEADERS)
            quizzes = []
            for quiz in response.json():
                quizzes.append({"name": quiz["title"],
                                "due_date": self.__get_quiz_due_date(quiz["all_dates"])})
            return quizzes
        except Exception as e:
            # Some JSON data does not have a quiz "title" or a quiz
            print(f"Course ID: {course_id} has disabled complete access")
            return quizzes 
        
    def __get_quiz_due_date(self, all_due_dates: list) -> str:
        """Parses through a given list to find a valid due date

        Args:
            all_due_dates (list): A provided list containing dicts of quiz due date data
            
            "all_dates": [
            {
                "due_at": "2025-02-15T07:59:00Z",
                "unlock_at": "2025-01-21T08:00:00Z",
                "lock_at": "2025-05-23T06:59:00Z",
                "base": true # Latest due date
            },
            {
                ...
            }]

        Returns:
            str: Due date
        """
        for due_date in all_due_dates:
            if due_date["base"] == True:
                return due_date["due_at"]
        return "N/A"
    
    def print_all_course_data(self):
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