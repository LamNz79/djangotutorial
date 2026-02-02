import logging
from typing import Optional

from polls.security.actions import Actions
from polls.security.deny_reasons import DenyReason

audit_logger = logging.getLogger("audit")


def log_audit_event(
        *,
        user_id: int,
        action: Actions,
        resource: str,
        allowed: bool,
        reason: Optional[DenyReason] = None,
):
    audit_logger.info(
        "audit_event",
        extra={
            "user_id": user_id,
            "action": action.value,
            "resource": resource,
            "allowed": allowed,
            "reason": reason.value if reason else None,
        },
    )
