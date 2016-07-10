import datetime
import json

from pyramid.view import view_config

from person import Session
from person.models import Person


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'person'}


@view_config(route_name='create_person', renderer='json', request_method='POST')
def create_person(request):

    body = json.loads(request.body.decode('utf-8'))
    first_name = None
    if 'first_name' in body:
        first_name = body['first_name']

    surname = None
    if 'surname' in body:
        surname = body['surname']

    try:
        date_of_birth = None
        if 'date_of_birth' in body:
            date_of_birth = datetime.datetime.strptime(body['date_of_birth'], '%b %d %Y').date()
    except:
        return {"error": "Date of birth is in incorrect format."}

    sex = None
    if 'sex' in body:
        sex = body['sex']
        if sex not in ['M', 'F']:
            return {"error": "The value of 'sex' field must be either 'M' or 'F'."}

    email = None
    if 'email' in body:
        email = body['email']

    try:
        session = Session()
        person = Person(first_name=first_name, surname=surname, date_of_birth=date_of_birth, sex=sex, email=email)
        session.add(person)
        session.commit()
    except:
        return {"error": "Person's profile could not be created."}

    response = {
        'id': person.person_id
    }

    return response

@view_config(route_name='read_person', renderer='json', request_method='GET')
def read_person(request):

    person_id = request.matchdict.get('person_id')

    session = Session()
    person = session.query(Person).filter_by(person_id=int(person_id)).first()

    if person is None:
        return {"error": "User not found"}

    response = {
        "first_name": person.first_name,
        "surname": person.surname,
        "date_of_birth": str(person.date_of_birth),
        "sex": person.sex,
        "email": person.email
    }

    return response