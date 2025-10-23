from enum import StrEnum


class ApiTagEnum(StrEnum):
    HEALTH_CHECK = "Health Check"
    CHAT_SESSION = "Chat Session"
    CHAT_MESSAGES = "Chat Message"


class AppEnvEnum(StrEnum):
    """
    Enum for app environments
    """

    LOCAL = "LOCAL"
    DEV = "DEV"
    STAGE = "STAGE"
    PROD = "PROD"
    TEST = "TEST"


class SenderTypeEnum(StrEnum):
    USER = "USER"
    AI = "AI"


class PGErrorCodeEnum(StrEnum):
    """
    Enum for pg_code exception codes
    For more info, check the following link: https://www.psycopg.org/docs/errors.html#sqlstate-exception-classes
    """

    FOREIGN_KEY_VIOLATION = "23503"
    NOT_NULL_VIOLATION = "23502"
    CONSTRAINT_VIOLATION = "23514"
    UNIQUE_VIOLATION = "23505"
