import re
import pdb
from collections import OrderedDict

import instructions


def load(instruction_name):
    " Translate asm fn name to python fn name, handle reserved. "
    
    if instruction_name.endswith('.b'):
        return getattr(instructions, instruction_name.replace('.', ''))
    if instruction_name == 'and':
        return instructions.and_
    else:
        return getattr(instructions, instruction_name)


OP2_OPERANDS = OrderedDict((
    # 1st arg is an addr (@)
    ('\s+@(\w+),\s+(\w+)\((\w+)\)', lambda f, a, offs, b: (load(f), '@' + a, '@{}+{}'.format(b, offs))),
    ('\s+@(\w+),\s+0x0\((\w+)\)', lambda f, a, b: (load(f), '@' + a, '@' + b)),
    ('\s+@(\w+),\s+(\w+)', lambda f, a, b: (load(f), '@' + a, b)),
    
    # Replaces 0x0(r) with @r
    ('\s+#?-?0x0\((\w+)\),\s+0x0\((\w+)\)', lambda f, a, b: (load(f), '@' + a, '@' + b)),
    ('\s+#?-?0x0\((\w+)\),\s+(\w+)', lambda f, a, b: (load(f), '@' + a, b)),
    ('\s+#?-?(\w+),\s+0x0\((\w+)\)', lambda f, a, b: (load(f), a, '@' + b)),
    
    # Replace 0x33(r) with @r+33
    ('\s+#?-?(\w+)\((\w+)\),\s+(\w+)\((\w+)\)', lambda f, offs1, a, offs2, b: (load(f), '@{}+{}'.format(a, offs1), '@{}+{}'.format(b, offs2))),
    ('\s+#?-?(\w+),\s+(\w+)\((\w+)\)', lambda f, a, offs, b: (load(f), a, '@{}+{}'.format(b, offs))),
    ('\s+#?-?(\w+)\((\w+)\),\s+(\w+)', lambda f, offs, a, b: (load(f), '@{}+{}'.format(a, offs), b)),
    
    # TODO: it's swallowing `+` for @rxx+
    ('\s+#?-?(@*\w+)\+?,\s+(\w+)', lambda f, a, b: (load(f), a, b)),
))

OP2_PATTERNS = OrderedDict(
    (('(mov|mov\.b|add|sub|and|cmp|cmp\.b)' + k, v) for k, v in OP2_OPERANDS.items())
)

OP1_PATTERNS = OrderedDict({
    '(inc|dec|push|pop|clr|sxt|call|ret|tst|tst\.b|jmp|jz|jnz|jl|jge|jne)\s+#?(-?\w+)': lambda f, arg: (load(f), arg),
})

def cast(s):
    m = re.search('-?0x(\w+)', s)
    if m and ('+' not in s):
        return int(m.group(), 16)
    else:
        return s

OP_PATTERNS = OrderedDict()
OP_PATTERNS.update(OP1_PATTERNS)
OP_PATTERNS.update(OP2_PATTERNS)

def parse_asm_line(line):
    for regex, fn in OP_PATTERNS.items():
        m = re.search(regex, line)
        if m:
            return fn(*[cast(s) for s in m.groups()])
        
    raise ValueError('Cannot parse line: ' + line)
            
def parse_asm_lines(s):
    return [parse_asm_line(l.strip()) for l in s.split('\n') if l.strip()]
