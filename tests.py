import time
import unittest

from instructions import *
from vm import VM
from asm_parser import (parse_asm_line,
                    parse_asm_lines,)


class TestParser(unittest.TestCase):    
    def test_parse_asm_line_2operand_reg_to_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov     sp, r15   # comment'),
                         (mov, 'sp', 'r15'))

    def test_parse_asm_line_2operand_reg_addr_plus_offset_to_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41 mov 0x2(r4), r11  # comment'),
                         (mov, '@r4+2', 'r11'))

    def test_parse_asm_line_2operand_reg_addr_to_reg_plus_offset(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41 mov r13, 0x13(r13)  # comment'),
                         (mov, 'r13', '@r13+19'))

    def test_parse_asm_line_2operand_reg_addr_plus_offset_to_reg_plus_offset(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41 mov 0x3(r4), 0x2(r11)  # comment'),
                         (mov, '@r4+3', '@r11+2'))
        
    def test_parse_asm_line_2operand_const_to_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov  #0xff, r11   # comment'),
                         (mov, 0xff, 'r11'))

    def test_parse_asm_line_2operand_addr_to_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov  @r10, r10   # comment'),
                         (mov, '@r10', 'r10'))

    def test_parse_asm_line_2operand_0x0_reg_to_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov  0x0(r10), r10   # comment'),
                         (mov, '@r10', 'r10'))

    def test_parse_asm_line_2operand_reg_to_0x0_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov  r10, 0x0(r10)   # comment'),
                         (mov, 'r10', '@r10'))

    def test_parse_asm_line_2operand_0x0_reg_to_0x0_reg_1(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     mov  0x0(r10), 0x0(r11)   # comment'),
                         (mov, '@r10', '@r11'))

    def test_parse_asm_line_2operand_0x0_reg_to_0x0_reg_2(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     and  0x0(r10), 0x0(r11)   # comment'),
                         (and_, '@r10', '@r11'))

    def test_parse_asm_line_1operand_reg(self):
        self.assertEqual(parse_asm_line('4ba2:  0f41     sxt  r10   # comment'),
                         (sxt, 'r10'))


class TestInstructions(unittest.TestCase):
    def setUp(self):
        self.vm = VM() 
        self.state, self.mem = self.vm.state, self.vm.mem

    def test_mov_const_to_reg(self):
        mov(0x3, 'r8', self.state, self.mem)
        self.assertEqual(self.state.r8, 0x3)

    def test_mov_reg_to_reg(self):
        self.state.r4 = 0x3
        mov('r4', 'r8', self.state, self.mem)
        self.assertEqual(3, self.state.r8)

    def test_mov_addr_to_reg(self):
        self.mem[0x666] = 0x1234
        self.state.r4 = 0x666
        mov('@r4', 'r4', self.state, self.mem)
        self.assertEqual(0x1234, self.state.r4)

    def test_mov_addr_plus_offset_to_reg(self):
        self.mem[0x66a] = 0x1234
        self.state.r4 = 0x666
        mov('@r4+4', 'r4', self.state, self.mem)
        self.assertEqual(0x1234, self.state.r4)

    def test_mov_addr_to_reg(self):
        self.mem[0x666] = 0x1234
        self.state.r4 = 0x666
        self.state.r5 = 0x555
        mov('@r4', '@r5', self.state, self.mem)
        self.assertEqual(0x1234, self.mem[0x555])
    
    def test_mov_addr_plus_offset_to_reg_plus_offset(self):
        self.mem[0x66a] = 0x1234
        self.state.r4 = 0x666
        self.state.r5 = 0x555
        mov('@r4+4', '@r6+3', self.state, self.mem)
        self.assertEqual(0x1234, self.mem[0x558])
        
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
