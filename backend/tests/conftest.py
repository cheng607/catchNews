"""pytest 全局 conftest — 确保 PYTHONPATH 包含 core 和 personal。"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent

for sub in ("core", "personal"):
    p = str(_ROOT / sub)
    if p not in sys.path:
        sys.path.insert(0, p)

_backend = str(_ROOT)
if _backend not in sys.path:
    sys.path.insert(0, _backend)
