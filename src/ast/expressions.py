"""
表达式AST节点定义
包含所有表达式类型的AST节点
"""

from typing import Any, List, Optional
from dataclasses import dataclass

from .base import ASTNode, ASTVisitor
from ..lexer.token import Token, TokenType


class 表达式(ASTNode):
    """
    表达式基类
    所有表达式节点都应该继承这个类
    """
    pass


@dataclass
class 二元运算表达式(表达式):
    """
    二元运算表达式
    如: a + b, x > y, p && q
    """
    
    左操作数: 表达式
    运算符: Token
    右操作数: 表达式
    
    def __init__(self, 左操作数: 表达式, 运算符: Token, 右操作数: 表达式):
        super().__init__(运算符.行号, 运算符.列号)
        self.左操作数 = 左操作数
        self.运算符 = 运算符
        self.右操作数 = 右操作数
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_二元运算表达式(self)
    
    def get_children(self) -> List[ASTNode]:
        return [self.左操作数, self.右操作数]
    
    def __repr__(self) -> str:
        return f"二元运算表达式({self.左操作数} {self.运算符.值} {self.右操作数})"


@dataclass
class 一元运算表达式(表达式):
    """
    一元运算表达式
    如: -x, !flag
    """
    
    运算符: Token
    操作数: 表达式
    
    def __init__(self, 运算符: Token, 操作数: 表达式):
        super().__init__(运算符.行号, 运算符.列号)
        self.运算符 = 运算符
        self.操作数 = 操作数
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_一元运算表达式(self)
    
    def get_children(self) -> List[ASTNode]:
        return [self.操作数]
    
    def __repr__(self) -> str:
        return f"一元运算表达式({self.运算符.值}{self.操作数})"


@dataclass
class 字面量表达式(表达式):
    """
    字面量表达式
    如: 123, 3.14, "hello", true
    """
    
    值: Any
    类型: TokenType
    
    def __init__(self, token: Token):
        super().__init__(token.行号, token.列号)
        self.值 = token.值
        self.类型 = token.类型
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_字面量表达式(self)
    
    def get_children(self) -> List[ASTNode]:
        return []
    
    def __repr__(self) -> str:
        return f"字面量表达式({self.值!r})"


@dataclass
class 标识符表达式(表达式):
    """
    标识符表达式
    如: 变量名, 函数名
    """
    
    名称: str
    
    def __init__(self, token: Token):
        super().__init__(token.行号, token.列号)
        self.名称 = token.值
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_标识符表达式(self)
    
    def get_children(self) -> List[ASTNode]:
        return []
    
    def __repr__(self) -> str:
        return f"标识符表达式({self.名称})"


@dataclass
class 函数调用表达式(表达式):
    """
    函数调用表达式
    如: func(a, b), add(x, y)
    """
    
    函数: 表达式
    参数列表: List[表达式]
    
    def __init__(self, 函数: 表达式, 参数列表: List[表达式], 行号: int, 列号: int):
        super().__init__(行号, 列号)
        self.函数 = 函数
        self.参数列表 = 参数列表
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_函数调用表达式(self)
    
    def get_children(self) -> List[ASTNode]:
        return [self.函数] + list(self.参数列表)
    
    def __repr__(self) -> str:
        参数_str = ", ".join(str(arg) for arg in self.参数列表)
        return f"函数调用表达式({self.函数}({参数_str}))"


@dataclass
class 赋值表达式(表达式):
    """
    赋值表达式
    如: x = 123, y = a + b
    """
    
    目标: 表达式
    值: 表达式
    
    def __init__(self, 目标: 表达式, 值: 表达式, 行号: int, 列号: int):
        super().__init__(行号, 列号)
        self.目标 = 目标
        self.值 = 值
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_赋值表达式(self)
    
    def get_children(self) -> List[ASTNode]:
        return [self.目标, self.值]
    
    def __repr__(self) -> str:
        return f"赋值表达式({self.目标} = {self.值})"