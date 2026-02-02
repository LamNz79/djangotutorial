from enum import Enum


class DenyReason(str, Enum):
    ROLE_REQUIRED = "ROLE_REQUIRED"
    VOTING_CLOSED = "VOTING_CLOSED"
    INVALID_STATE = "INVALID_STATE"

