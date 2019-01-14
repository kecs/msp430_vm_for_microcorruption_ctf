import re
import pdb
from collections import OrderedDict
from numpy import uint16 as i16

import instructions


def load_fn(instruction_name):
    """ Translate asm fn name to python fn name, handle reserved words. """
    
    if instruction_name.endswith('.b'):
        return getattr(instructions, instruction_name.replace('.', ''))
    elif instruction_name == 'and':
        return instructions.and_
    else:
        return getattr(instructions, instruction_name)

    
def parse_arg(s):
    """ Translate addresses to IL """

    if re.match('r\d{1,2}|@.+|sp|pc', s):
        return s

    m = re.search('(-?)0x(\w+)\((\w+)\)', s)
    if m:
        offset = (m.groups()[0] and '-' or '+') + m.groups()[1]
        return f'@{m.groups()[2]}{offset}'

    raise ValueError(f'Cannot parse string: {s} {type(s)}')
        
    
def parse_first_arg(s):
    if s.startswith('#'):
        return i16(int(s[1:], 16))
    else:
        return parse_arg(s)
        

def parse_asm_line(line):
    splitted = re.split(',?\s+', line)
    fn = load_fn(splitted[0])
    
    if len(splitted) == 1:
        return (fn, )
    elif len(splitted) == 2:
        if fn.__name__.startswith('j'):
            return (fn, int(splitted[1]))
        elif fn.__name__ == 'call':
            return (fn, splitted[1])
        else:
            return (fn, parse_first_arg(splitted[1]))
    elif len(splitted) == 3:
        return (fn, parse_first_arg(splitted[1]), parse_arg(splitted[2]))
    else:
        raise ValueError(f'Cannot parse line: {line}')
    

def parse_asm_lines(s):
    return [parse_asm_line(l.strip()) for l in s.split('\n') if l.strip()]

