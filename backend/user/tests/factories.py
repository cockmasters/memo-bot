import factory
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from core.tests import test_session
from user.models import User


class UserFactory(AsyncSQLAlchemyFactory):
    tg_id = factory.Sequence(lambda n: n)
    vk_id = factory.Sequence(lambda n: n)
    ds_id = factory.Sequence(lambda n: n)

    class Meta:
        model = User
        sqlalchemy_session = test_session
