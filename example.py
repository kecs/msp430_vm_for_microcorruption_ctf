from utils import VM
from instructions import *


vm = VM()
    
def dbg(s, m):
    m = []
    inc(s.sp)
    print(s.sp)

# Setup
vm.runasm(
    [mov, 0x42, 'r15'],
    [inc, 'r15'],
    [clr, 'r13'],
    dbg,
    [ret]
)

vm.runasm('''
    mov #0x1234, r14
    mov #0x6789, r15
    clr r10 ''')

while VM.state.r11:
    vm.runasm(
        [mov, 'r15', 'r11'],
        [add, 0x2,  'r15'],
        [dec, 'r11']
    )

    

    

