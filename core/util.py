from __future__ import annotations
from typing import Callable, Optional

LogFn = Callable[[str, Optional[int]], None]
def noop_log(msg: str, pct: Optional[int] = None) -> None:
    pass

from typing import Callable, Optional
from contextvars import ContextVar

# the active logger for this request/job
_current_log: ContextVar[Callable[[str, Optional[int]], None]] = ContextVar("_current_log", default=lambda *_: None)

def set_progress_logger(fn: Callable[[str, Optional[int]], None]):
    """Activate a logger for the current context."""
    _current_log.set(fn)

def emit(msg: str, pct: Optional[int] = None):
    """Log progress anywhere in the call stack without passing a param."""
    _current_log.get()(msg, pct)