import factory
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from core.tests import test_session
from user.note.models import Note, Tag, association_table
from user.tests.factories import UserFactory


class NoteFactory(AsyncSQLAlchemyFactory):
    user_id = factory.SubFactory(UserFactory)
    title = factory.Faker("name_female")
    body = factory.Faker("paragraph")

    class Meta:
        model = Note
        sqlalchemy_session = test_session


class TagFactory(AsyncSQLAlchemyFactory):
    name = factory.Faker("job")

    class Meta:
        model = Tag
        sqlalchemy_session = test_session


class NoteTagFactory(AsyncSQLAlchemyFactory):
    note_id = factory.SubFactory(NoteFactory)
    tag_id = factory.SubFactory(TagFactory)

    class Meta:
        model = association_table
        sqlalchemy_session = test_session
