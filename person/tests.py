import json
import os
import unittest

from paste.deploy import appconfig
from pyramid import testing
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from webtest import TestApp
from person import Session, main
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


here = os.path.dirname(__file__)
settings = appconfig('config:' + os.path.join(here, '../', 'test.ini'))

class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
        cls.Session = sessionmaker()

    def setUp(self):
        connection = self.engine.connect()

        # begin a non-ORM transaction
        self.trans = connection.begin()

        # bind an individual Session to the connection
        Session.configure(bind=connection)
        self.session = self.Session(bind=connection)
        #Entity.session = self.session


class IntegrationTestBase(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = main({}, **settings)
        super(IntegrationTestBase, cls).setUpClass()

    def setUp(self):
        self.app = TestApp(self.app)
        self.config = testing.setUp()
        super(IntegrationTestBase, self).setUp()


class IntegrationTestViews(IntegrationTestBase):


    def test_create_and_read_person_profile(self):
        """
        It creates a person profile, and reads it afterwards.
        :return:
        """
        data = {
            "first_name": "Roha",
            "surname": "Ahmed",
            "date_of_birth": "Sep 20 2015",
            "sex": "M",
            "email": "roha.ahmed@gmail.com"
        }
        post_response = self.app.post('/person/', params=json.dumps(data).encode('utf-8'))

        post_result = json.loads(post_response.body.decode('utf-8'))

        person_id = post_result['person_id']
        get_response = self.app.get('/person/' + str(person_id))


        get_result = json.loads(get_response.body.decode('utf-8'))
        self.assertEqual(get_result['first_name'], "Roha")



