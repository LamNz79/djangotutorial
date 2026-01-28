# polls/permissions.py

from polls.permissions.rbac import HasRole
from polls.security.roles import Roles


class IsVoter(HasRole):
    required_roles = {Roles.VOTER}


class IsModerator(HasRole):
    required_roles = {Roles.MODERATOR}
