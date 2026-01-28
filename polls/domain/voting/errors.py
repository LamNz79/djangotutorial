from enum import Enum


class VotingError(str, Enum):
    CHOICE_NOT_FOUND = "CHOICE_NOT_FOUND"
    INVALID_VOTE_STATE = "INVALID_VOTE_STATE"
