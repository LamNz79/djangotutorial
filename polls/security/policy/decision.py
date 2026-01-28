# class PolicyDecision:
#     def __init__(self, allowed: bool, reason=None):
#         self.allowed = allowed
#         self.reason = reason
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: Optional[str] = None
