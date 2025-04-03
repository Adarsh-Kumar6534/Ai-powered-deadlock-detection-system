from enum import Enum, auto

class DeadlockType(Enum):
    NONE = auto()
    MUTUAL_EXCLUSION = auto()
    NO_PREEMPTION = auto()
    CIRCULAR_WAIT = auto()
    HOLD_AND_WAIT = auto()

    def __str__(self):
        names = {
            self.NONE: "No Deadlock",
            self.MUTUAL_EXCLUSION: "🔴 Mutual Exclusion Deadlock",
            self.NO_PREEMPTION: "🟡 No Preemption Deadlock",
            self.CIRCULAR_WAIT: "🟠 Circular Wait Deadlock",
            self.HOLD_AND_WAIT: "🔵 Hold and Wait Deadlock"
        }
        return names[self]
