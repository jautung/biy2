from enum import Enum, auto


class RuleType(Enum):
    NOUN_CLAUSE_IS_ATTRIBUTE_CLAUSE = auto()
    NOUN_CLAUSE_IS_NOUN = auto()
    NOUN_CLAUSE_HAS_NOUN = auto()
