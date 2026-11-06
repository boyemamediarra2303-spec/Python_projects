from check import raises
from exceptions import (ComplianceError, InvalidTransactionError, DuplicateTransactionError,
                        DataFormatError, EmptyQueueError, EmptyStackError,
                        InvalidRuleConfigError, InsufficientDataError)
from utils import parse_amount, format_xof
 
# --- exception hierarchy: one base class, catch them all with a single except
for exc in [InvalidTransactionError, DuplicateTransactionError, DataFormatError, EmptyQueueError,
            EmptyStackError, InvalidRuleConfigError, InsufficientDataError]:
    assert issubclass(exc, ComplianceError)
assert issubclass(ComplianceError, Exception)
 
# --- parse_amount: messy real-world text -> float
assert parse_amount("3500000") == 3500000.0
assert parse_amount("3,500,000") == 3500000.0
assert parse_amount("3 500 000") == 3500000.0
# narrow no-break spaces (French formatting)
assert parse_amount("3\u202f500\u202f000 XOF") == 3500000.0
assert parse_amount("  12 000 000 fcfa ") == 12000000.0          # case-insensitive suffix, outer spaces
assert parse_amount("12.5") == 12.5
assert parse_amount("-5") == -5.0                                # parsing is NOT validation
assert isinstance(parse_amount("100"), float)
for bad in ["", "   ", "abc", "nan", "inf", "-inf", "12 XOF 000", "1,2,x"]:
    assert raises(InvalidTransactionError, parse_amount, bad)
assert raises(InvalidTransactionError, parse_amount, 5000)       # must receive text
assert raises(InvalidTransactionError, parse_amount, None)
 
# --- format_xof: float -> display string
assert format_xof(3500000) == "3 500 000 XOF"
assert format_xof(0) == "0 XOF"
assert format_xof(12) == "12 XOF"
assert format_xof(1234.0) == "1 234 XOF"
assert format_xof(999.6) == "1 000 XOF"                          # rounds to the nearest whole franc
assert format_xof(27_499_999.0) == "27 499 999 XOF"
print("Part 0 OK")