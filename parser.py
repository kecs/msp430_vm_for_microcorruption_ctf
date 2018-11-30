import re

from instructions import *


patterns = {
    'mov\s*(\w+),\s*(\w+)': mov,
}


def parse_asm_line(l):
    pass
    
def parse_asm_lines(s):
    return [parse_asm_line(l) for l in s.split('\n') if l.strip()]
