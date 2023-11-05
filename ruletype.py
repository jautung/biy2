from enum import Enum, auto


class RuleType(Enum):
    NOUN_IS_ATTRIBUTE = auto()
    NOUN_IS_NOUN = auto()
    NOUN_HAS_NOUN = auto()
