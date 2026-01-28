from polls.permissions.abac import CanVote
from polls.permissions.permissions import IsVoter
from polls.security.deny_reasons import DenyReason
from polls.security.policy.decision import PolicyDecision


def can_vote(request, view, choice) -> PolicyDecision:
    # RBAC
    if not IsVoter().has_permission(request, view):
        return PolicyDecision(
            allowed=False,
            reason=DenyReason.ROLE_REQUIRED
        )
    if not CanVote().has_object_permission(request, view, choice):
        return PolicyDecision(
            allowed=False,
            reason=DenyReason.VOTING_CLOSED
        )
    return PolicyDecision(allowed=True)
