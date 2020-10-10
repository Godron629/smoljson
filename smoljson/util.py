import re


REGEX_NUMBER = re.compile(
    pattern=r"""
    -?                # optional negative sign
    (?:0|[1-9]\d*)    # starts with 0 digit OR 1-9 digit followed by 0+ digits
    (?:\.\d+)?        # optional decimal followed by 1+ digits
    (?:[eE][-+]?\d+)? # optional exponential notation
    """,
    flags=re.VERBOSE,
)
