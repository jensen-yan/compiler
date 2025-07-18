"""
AST (抽象语法树) 模块
定义了所有AST节点类型
"""

from .base import ASTNode, ASTVisitor
from .expressions import (
    表达式,
    二元运算表达式,
    一元运算表达式,
    字面量表达式,
    标识符表达式,
    函数调用表达式,
    赋值表达式,
)
from .statements import (
    语句,
    表达式语句,
    变量声明语句,
    函数声明语句,
    返回语句,
    如果语句,
    当语句,
    代码块语句,
)
from .program import 程序

__all__ = [
    # 基础类
    "ASTNode",
    "ASTVisitor",
    
    # 表达式
    "表达式",
    "二元运算表达式",
    "一元运算表达式", 
    "字面量表达式",
    "标识符表达式",
    "函数调用表达式",
    "赋值表达式",
    
    # 语句
    "语句",
    "表达式语句",
    "变量声明语句",
    "函数声明语句",
    "返回语句",
    "如果语句",
    "当语句",
    "代码块语句",
    
    # 程序
    "程序",
]