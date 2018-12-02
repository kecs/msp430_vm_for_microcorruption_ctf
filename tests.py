import time
import unittest

from instructions import *
from vm import VM
from utils import print_state
from parser import (parse_asm_line,
                    parse_asm_lines,)


class TestParser(unittest.TestCase):    
    def test_parse_asm_line_mov_reg_to_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov     sp, r15   # comment'),
                         (mov, 'sp', 'r15'))

    def test_parse_asm_line_mov_const_to_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov  #0xff, r11   # comment'),
                         (mov, 0xff, 'r11'))

    def test_parse_asm_line_mov_addr_to_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov  @r10, r10   # comment'),
                         (mov, '@r10', 'r10'))



class TestInstructions(unittest.TestCase):
    def setUp(self):
        self.vm = VM() 
        self.state, self.mem = self.vm.state, self.vm.mem

    def test_mov_const_to_reg(self):
        mov(0x3, 'r8', self.state, self.mem)

        self.assertEqual(self.state.r8, 0x3)


    def test_mov_reg_to_reg(self):
        mov(0x3, 'r4', self.state, self.mem)
        mov('r4', 'r8', self.state, self.mem)
        print_state(self.state, self.mem)
        self.assertEqual(self.state.r4, self.state.r8)

#     @unittest.skip("Not now")
#     def test_setz(self):
#         pass

#     @unittest.skip("Not now")
#     def test_add(self):
#         pass

#     @unittest.skip("Not now")
#     def test_sub(self):
#         pass

#     @unittest.skip("Not now")
#     def test_inc(self):
#         pass

#     @unittest.skip("Not now")
#     def test_dec(self):
#         pass

#     @unittest.skip("Not now")
#     def test_clr(self):
#         pass

#     @unittest.skip("Not now")
#     def test_sxt(self):
#         pass

#     @unittest.skip("Not now")
#     def test__and(self):
#         pass

#     @unittest.skip("Not now")
#     def test_push(self):
#         pass

#     @unittest.skip("Not now")
#     def test_pop(self):
#         pass

#     @unittest.skip("Not now")
#     def test_call(self):
#         pass

#     @unittest.skip("Not now")
#     def test_ret(self):
#         pass

#     @unittest.skip("Not now")
#     def test_tst(self):
#         pass

#     @unittest.skip("Not now")
#     def test_tstb(self):
#         pass

#     @unittest.skip("Not now")
#     def test_from_addr(self):
#         pass

#     @unittest.skip("Not now")
#     def test_jmp(self):
#         pass

#     @unittest.skip("Not now")
#     def test_jz(self):
#         pass

#     @unittest.skip("Not now")
#     def test_cmp(self):
#         pass

#     @unittest.skip("Not now")
#     def test_cmpb(self):
#         pass

#     @unittest.skip("Not now")
#     def test_jnz(self):
#         pass
    
#     @unittest.skip("Not now")
#     def test_jeq(self):
#         pass

#     @unittest.skip("Not now")
#     def test_jge(self):
#         pass

#     @unittest.skip("Not now")
#     def test_jl(self):
#         pass


unittest.main()
