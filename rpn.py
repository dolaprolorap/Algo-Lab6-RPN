import math
import re
from enum import Enum

class StackCalcExc(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class TokenType(Enum):
    WHITESPACE = 0
    NUM = 1
    OPER = 2
    NONE = 3

class StackCalc:
    def __init__(self):
        self.tokens = []
        self.tokens_ptr = 0
        self.bin_operators = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
            "^": lambda x, y: x ^ y
        }
        self.un_operators = {
            "sin": lambda x: math.sin(x),
            "cos": lambda x: math.cos(x),
            "tg": lambda x: math.tan(x),
            "ctg": lambda x: 1 / math.tan(x),
            "!": lambda x: math.factorial(int(x))
        }
        self.max_parser_buf_sz = 20

    def calc(self, str : str) -> float:
        self.parse_str_to_tokens(str)
        return self.inner_calc(False)

    def calc_infix(self, str : str) -> float:
        pass

    def inner_calc(self, in_brackets : bool) -> float:
        stack = []
        for token_pos in range(self.tokens_ptr, len(self.tokens)):
            token = self.tokens[token_pos]
            try_num = self.is_number(token)
            if isinstance(try_num, float):
                stack.append(try_num)
            elif token in self.bin_operators:
                if len(stack) <= 1: 
                    raise StackCalcExc("There is too few elements for bin operator")
                val2 = stack.pop()
                val1 = stack.pop()
                if not isinstance(val1, float | int) or not isinstance(val2, float | int):
                    raise StackCalcExc("Bin operator's operands are not numbers")
                stack.append(self.bin_operators[token](val1, val2))
            elif token in self.un_operators:
                if len(stack) == 0: 
                    raise StackCalcExc("There is too few elements for un operator")
                val = stack.pop()
                if not isinstance(val, float | int):
                    raise StackCalcExc("Un operator's operand is not number")
                stack.append(self.un_operators[token](val))
            elif token == "(":
                calc_val = self.inner_calc(True)
                stack.append(calc_val)
            elif token == ")":
                self.tokens_ptr += 1
                return stack.pop()
            else:
                raise StackCalcExc("Undefined token: {token}")
            self.tokens_ptr += 1
        if in_brackets: raise StackCalcExc("Did not find closing bracket")
        else: return stack.pop()

    def parse_str_to_tokens(self, str: str) -> None:
        buf = ""
        in_buf = TokenType.NONE

        for s in str:
            new_in_buf = self.get_symb_type(s)
            if in_buf != TokenType.NONE:
                if in_buf != new_in_buf:
                    if in_buf != TokenType.WHITESPACE:
                        parse_res = self.try_parse_token(buf)
                        if parse_res != None:
                            self.tokens.append(parse_res)
                        else:
                            raise StackCalcExc("Undefined token")
                    buf = ""
                elif new_in_buf == TokenType.OPER:
                    parse_res = self.try_parse_token(buf)
                    if parse_res != None:
                        self.tokens.append(parse_res)
                        buf = ""
            in_buf = new_in_buf
            buf += s
        if len(buf) != 0 and in_buf != TokenType.WHITESPACE:
            parse_res = self.try_parse_token(buf)
            if parse_res != None:
                self.tokens.append(parse_res)
            else:
                raise StackCalcExc("Undefined token")
            
    def try_parse_token(self, str : str) -> str | float | None:
        try_num = self.is_number(str)
        if not isinstance(try_num, bool):
            return try_num
        elif str in self.bin_operators or \
            str in self.un_operators or \
            str == "(" or \
            str == ")":
            return str
        else: return None

    def get_symb_type(self, str : str) -> TokenType:
        if str.isdigit() or str == ".":
            return TokenType.NUM
        elif str.isspace():
            return TokenType.WHITESPACE
        else:
            return TokenType.OPER
    
    def is_number(self, str : str) -> float | bool:
        try:
            return float(str)
        except ValueError:
            return False
