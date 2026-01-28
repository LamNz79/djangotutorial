# polls/permissions.py

from polls.permissions.rbac import HasRole


class IsVoter(HasRole):
    required_roles = {"voter"}


class IsModerator(HasRole):
    required_roles = {"moderator"}
