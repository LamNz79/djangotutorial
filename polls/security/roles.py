from enum import Enum


class Roles(str, Enum):
    VOTER = "voter"
    MODERATOR = "moderator"