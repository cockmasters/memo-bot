import factory
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from backend.core.tests import test_session
from backend.user.models import User


class UserFactory(AsyncSQLAlchemyFactory):
    tg_id = factory.Sequence(lambda n: n)
    username = factory.Faker("first_name")

    class Meta:
        model = User
        sqlalchemy_session = test_session
