import factory
from factory import fuzzy

from app.core.enums import SenderTypeEnum
from app.models import ChatMessage
from tests.factories.base import BaseSQLAlchemyFactory
from tests.factories.chat_session import ChatSessionFactory


class ChatMessageFactory(BaseSQLAlchemyFactory[ChatMessage]):
    class Meta:
        model = ChatMessage
        exclude = ("session",)

    session = factory.SubFactory(ChatSessionFactory)
    session_id = factory.SelfAttribute("session.id")

    sender = fuzzy.FuzzyChoice(SenderTypeEnum)
    content = factory.Faker("pystr")
    context = factory.Faker("pydict", value_types=(str,))
