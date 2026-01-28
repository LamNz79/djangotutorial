class PolicyDecision:
    def __init__(self, allowed: bool, reason=None):
        self.allowed = allowed
        self.reason = reason
