"""Personas koda pārbaude (CR-1). Noteikumi vienkāršoti mācību vajadzībām."""

import re
from datetime import date

# 11 cipari; defise drīkst būt tikai pēc 6. cipara.
_FORMAT = re.compile(r"\d{11}|\d{6}-\d{5}")
# Jaunais formāts: pirmais cipars 3, otrais 2–9.
_NEW_FORMAT = re.compile(r"3[2-9]\d{9}")
_CHECK_WEIGHTS = (1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
_CENTURIES = {"0": 1800, "1": 1900, "2": 2000}


def normalize(value: str) -> str | None:
    """Atgriež kodu bez atstarpēm un defises vai None, ja kods nav derīgs."""
    compact = "".join(value.split())
    if not _FORMAT.fullmatch(compact):
        return None
    digits = compact.replace("-", "")
    if _NEW_FORMAT.fullmatch(digits):
        return digits
    return digits if _is_valid_old_format(digits) else None


def _is_valid_old_format(digits: str) -> bool:
    # DDMMGG-XNNNN: X ir gadsimts, pēdējais cipars ir kontrolcipars.
    century = _CENTURIES.get(digits[6])
    if century is None:
        return False
    try:
        date(century + int(digits[4:6]), int(digits[2:4]), int(digits[0:2]))
    except ValueError:
        return False
    total = sum(int(d) * w for d, w in zip(digits[:10], _CHECK_WEIGHTS, strict=True))
    return (1101 - total) % 11 == int(digits[10])
