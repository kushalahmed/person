import json
import unittest

from pyramid import testing

from person.views import create_person


class UnitTestsViews(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_create_person_invalid_sex_value(self):
        request = testing.DummyRequest()
        data = {
          "first_name": "Kushal",
          "surname": "Ahmed",
          "date_of_birth": "Dec 20 1984",
          "sex": "R",
          "email": "kushal.ahmed@griffithuni.edu.au"
        }
        request.body = json.dumps(data).encode('utf-8')
        response = create_person(request)
        self.assertEqual(response['error'], "The value of 'sex' field must be either 'M' or 'F'.")

    def test_create_person_invalid_date_of_birth_value(self):
        request = testing.DummyRequest()
        data = {
            "first_name": "Kushal",
            "surname": "Ahmed",
            "date_of_birth": "20 Dec 1984",
            "sex": "M",
            "email": "kushal.ahmed@griffithuni.edu.au"
        }
        request.body = json.dumps(data).encode('utf-8')
        response = create_person(request)
        self.assertEqual(response['error'], "Date of birth is in incorrect format.")

    def test_create_person_null_first_name_value(self):
        request = testing.DummyRequest()
        data = {
            #"first_name": "Kushal",
            "surname": "Ahmed",
            "date_of_birth": "Dec 20 1984",
            "sex": "M",
            "email": "kushal.ahmed@griffithuni.edu.au"
        }
        request.body = json.dumps(data).encode('utf-8')
        response = create_person(request)
        self.assertEqual(response['error'], "Person's profile could not be created.")

    def test_create_person_null_email_value(self):
        request = testing.DummyRequest()
        data = {
            "first_name": "Kushal",
            "surname": "Ahmed",
            "date_of_birth": "Dec 20 1984",
            "sex": "M",
            #"email": "kushal.ahmed@griffithuni.edu.au"
        }
        request.body = json.dumps(data).encode('utf-8')
        response = create_person(request)
        self.assertEqual(response['error'], "Person's profile could not be created.")



class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_create_person_invalid_sex_value(self):
        request = testing.DummyRequest()
        data = {
          "first_name": "Kushal",
          "surname": "Ahmed",
          "date_of_birth": "Dec 20 1984",
          "sex": "R",
          "email": "kushal.ahmed@griffithuni.edu.au"
        }
        request.body = json.dumps(data).encode('utf-8')
        response = create_person(request)
        self.assertEqual(response['error'], "The value of 'sex' field must be either 'M' or 'F'.")

