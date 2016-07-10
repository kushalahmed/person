import sqlalchemy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from person.models import Base, Session


#Base = declarative_base()
#Engine = None
#Session = None

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    engine = engine_from_config(settings, 'sqlalchemy.')
    if create_database_schema_if_not_exists(settings.get('sqlalchemy.url')):
        Base.metadata.create_all(engine)

    Session.configure(bind=engine)

    #global Engine
    #Engine = engine
    #global Session
    #Session = sessionmaker(bind=Engine)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route(name='create_person', pattern='/person/')
    config.add_route(name='read_person', pattern='/person/{person_id}')

    config.scan()
    return config.make_wsgi_app()


# Returns True if created, False otherwise
def create_database_schema_if_not_exists(schema_url):
    engine = sqlalchemy.create_engine(schema_url)
    if not database_exists(engine.url):
        create_database(engine.url)
        return True
    return False