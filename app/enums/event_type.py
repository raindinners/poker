from enum import Enum


class EventType(str, Enum):
    CREATE = "CREATE"
    EXECUTE_ACTION = "EXECUTE_ACTION"
    EXIT = "EXIT"
    JOIN = "JOIN"
