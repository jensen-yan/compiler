"""
Token相关类定义
包含TokenType枚举和Token类
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    """
    Token类型枚举
    定义了所有可能的token类型
    """
    
    # 字面量
    整数 = auto()           # INTEGER: 123
    浮点数 = auto()         # FLOAT: 123.45
    字符串 = auto()         # STRING: "hello"
    布尔值 = auto()         # BOOLEAN: true, false
    
    # 标识符和关键字
    标识符 = auto()         # IDENTIFIER: variable_name
    
    # 关键字
    函数 = auto()           # FUNCTION: func
    返回 = auto()           # RETURN: return
    如果 = auto()           # IF: if
    否则 = auto()           # ELSE: else
    当 = auto()             # WHILE: while
    对于 = auto()           # FOR: for
    真 = auto()             # TRUE: true
    假 = auto()             # FALSE: false
    空 = auto()             # NULL: null
    
    # 运算符
    加 = auto()             # PLUS: +
    减 = auto()             # MINUS: -
    乘 = auto()             # MULTIPLY: *
    除 = auto()             # DIVIDE: /
    模 = auto()             # MODULO: %
    
    # 比较运算符
    等于 = auto()           # EQUAL: ==
    不等于 = auto()         # NOT_EQUAL: !=
    小于 = auto()           # LESS_THAN: <
    大于 = auto()           # GREATER_THAN: >
    小于等于 = auto()       # LESS_EQUAL: <=
    大于等于 = auto()       # GREATER_EQUAL: >=
    
    # 逻辑运算符
    与 = auto()             # AND: &&
    或 = auto()             # OR: ||
    非 = auto()             # NOT: !
    
    # 赋值运算符
    赋值 = auto()           # ASSIGN: =
    
    # 分隔符
    左括号 = auto()         # LEFT_PAREN: (
    右括号 = auto()         # RIGHT_PAREN: )
    左大括号 = auto()       # LEFT_BRACE: {
    右大括号 = auto()       # RIGHT_BRACE: }
    左方括号 = auto()       # LEFT_BRACKET: [
    右方括号 = auto()       # RIGHT_BRACKET: ]
    
    # 标点符号
    分号 = auto()           # SEMICOLON: ;
    逗号 = auto()           # COMMA: ,
    点 = auto()             # DOT: .
    
    # 特殊token
    换行 = auto()           # NEWLINE: \n
    文件结束 = auto()       # EOF: end of file
    
    # 错误token
    错误 = auto()           # ERROR: invalid character


@dataclass
class Token:
    """
    Token类
    表示词法分析器产生的一个token
    """
    
    类型: TokenType         # token类型
    值: Any                 # token的值
    行号: int = 1           # 所在行号
    列号: int = 1           # 所在列号
    
    def __str__(self) -> str:
        """返回token的字符串表示"""
        return f"Token({self.类型.name}, {self.值!r}, {self.行号}:{self.列号})"
    
    def __repr__(self) -> str:
        """返回token的调试字符串表示"""
        return self.__str__()
    
    def is_type(self, token_type: TokenType) -> bool:
        """检查token是否为指定类型"""
        return self.类型 == token_type
    
    def is_literal(self) -> bool:
        """检查token是否为字面量"""
        return self.类型 in {
            TokenType.整数,
            TokenType.浮点数,
            TokenType.字符串,
            TokenType.布尔值,
        }
    
    def is_operator(self) -> bool:
        """检查token是否为运算符"""
        return self.类型 in {
            TokenType.加, TokenType.减, TokenType.乘, TokenType.除, TokenType.模,
            TokenType.等于, TokenType.不等于, 
            TokenType.小于, TokenType.大于, TokenType.小于等于, TokenType.大于等于,
            TokenType.与, TokenType.或, TokenType.非,
            TokenType.赋值,
        }
    
    def is_keyword(self) -> bool:
        """检查token是否为关键字"""
        return self.类型 in {
            TokenType.函数, TokenType.返回, TokenType.如果, TokenType.否则,
            TokenType.当, TokenType.对于, TokenType.真, TokenType.假, TokenType.空,
        }


# 关键字映射表
KEYWORDS = {
    'func': TokenType.函数,
    'return': TokenType.返回,
    'if': TokenType.如果,
    'else': TokenType.否则,
    'while': TokenType.当,
    'for': TokenType.对于,
    'true': TokenType.真,
    'false': TokenType.假,
    'null': TokenType.空,
}