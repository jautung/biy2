from enum import Enum, auto


class RuleClauseType(Enum):
    NOUN_CLAUSE = auto()
    ATTRIBUTE_CLAUSE = auto()
    IS = auto()
    HAS = auto()


class RuleType(Enum):
    NOUN_IS_ATTRIBUTE = auto()
    NOUN_IS_NOUN = auto()
    NOUN_HAS_NOUN = auto()


RULE_TYPES: dict[RuleType, list[RuleClauseType]] = {
    RuleType.NOUN_IS_ATTRIBUTE: [
        RuleClauseType.NOUN_CLAUSE,
        RuleClauseType.IS,
        RuleClauseType.ATTRIBUTE_CLAUSE,
    ],
    RuleType.NOUN_IS_NOUN: [
        RuleClauseType.NOUN_CLAUSE,
        RuleClauseType.IS,
        RuleClauseType.NOUN_CLAUSE,
    ],
    RuleType.NOUN_HAS_NOUN: [
        RuleClauseType.NOUN_CLAUSE,
        RuleClauseType.HAS,
        RuleClauseType.NOUN_CLAUSE,
    ],
}
