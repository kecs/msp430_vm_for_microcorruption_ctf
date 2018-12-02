import re
import pdb

from instructions import *


# TODO: there are basically 2 type of regexes............
PATTERNS = {
    'mov\s+#*(@*\w+),\s+(\w+)': mov,
    'add\s+#*(@*\w+),\s+(\w+)': add,
    'sub\s+#*(@*\w+),\s+(\w+)': sub,
    '_and\s+#*(@*\w+),\s+(\w+)': _and,
    'inc\s+(\w+)': inc,
    'dec\s+(\w+)': dec,
    'clr\s+(\w+)': clr,
    'sxt\s+(\w+)': sxt,
    'push\s+(\w+)': push,
    'pop\s+(\w+)': pop,
    'ret\s+(\w+)': ret,

}

PT = {1: '\s+(\w+)', 2: '\s+#*(@*\w+),\s+(\w+)'}

def cast(s):
    m = re.search('0x(\w+)', s)
    if m:
        return int(m.group(), 16)
    else:
        return s


def parse_asm_line(line):
    for regex, fn in PATTERNS.items():
        m = re.search(regex, line)
        if m and len(m.groups()) == 1:
            return (fn, cast(m.groups[0]))
        elif m and len(m.groups()) == 2:
            return (fn, cast(m.groups()[0]), cast(m.groups()[1]))

        
def parse_asm_lines(s):
    return [parse_asm_line(l) for l in s.split('\n') if l.strip()]
