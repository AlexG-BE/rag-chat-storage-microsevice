import factory

from app.models import ChatSession
from tests.factories.base import BaseSQLAlchemyFactory


class ChatSessionFactory(BaseSQLAlchemyFactory[ChatSession]):
    class Meta:
        model = ChatSession

    user_id = factory.Faker("uuid4")
    title = factory.Faker("pystr")
    is_favorite = factory.Faker("pybool")
