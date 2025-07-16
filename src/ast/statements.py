"""
语句AST节点定义
包含所有语句类型的AST节点
"""

from typing import Any, List, Optional
from dataclasses import dataclass

from .base import ASTNode, ASTVisitor
from .expressions import 表达式
from ..lexer.token import Token


class 语句(ASTNode):
    """
    语句基类
    所有语句节点都应该继承这个类
    """
    pass


@dataclass
class 表达式语句(语句):
    """
    表达式语句
    如: x + y; func(a, b);
    """
    
    表达式: 表达式
    
    def __init__(self, 表达式: 表达式):
        super().__init__(表达式.行号, 表达式.列号)
        self.表达式 = 表达式
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_表达式语句(self)
    
    def get_children(self) -> List[ASTNode]:
        return [self.表达式]
    
    def __repr__(self) -> str:
        return f"表达式语句({self.表达式})"


@dataclass
class 变量声明语句(语句):
    """
    变量声明语句
    如: let x = 123; var y = "hello";
    """
    
    名称: str
    初始值: Optional[表达式]
    
    def __init__(self, 名称: str, 初始值: Optional[表达式], 行号: int, 列号: int):
        super().__init__(行号, 列号)
        self.名称 = 名称
        self.初始值 = 初始值
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_变量声明语句(self)
    
    def get_children(self) -> List[ASTNode]:
        return [self.初始值] if self.初始值 else []
    
    def __repr__(self) -> str:
        if self.初始值:
            return f"变量声明语句({self.名称} = {self.初始值})"
        else:
            return f"变量声明语句({self.名称})"


@dataclass
class 函数声明语句(语句):
    """
    函数声明语句
    如: func add(a, b) { return a + b; }
    """
    
    名称: str
    参数列表: List[str]
    函数体: '代码块语句'
    
    def __init__(self, 名称: str, 参数列表: List[str], 函数体: '代码块语句', 行号: int, 列号: int):
        super().__init__(行号, 列号)
        self.名称 = 名称
        self.参数列表 = 参数列表
        self.函数体 = 函数体
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_函数声明语句(self)
    
    def get_children(self) -> List[ASTNode]:
        return [self.函数体]
    
    def __repr__(self) -> str:
        参数_str = ", ".join(self.参数列表)
        return f"函数声明语句({self.名称}({参数_str}))"


@dataclass
class 返回语句(语句):
    """
    返回语句
    如: return x; return a + b;
    """
    
    返回值: Optional[表达式]
    
    def __init__(self, 返回值: Optional[表达式], 行号: int, 列号: int):
        super().__init__(行号, 列号)
        self.返回值 = 返回值
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_返回语句(self)
    
    def get_children(self) -> List[ASTNode]:
        return [self.返回值] if self.返回值 else []
    
    def __repr__(self) -> str:
        if self.返回值:
            return f"返回语句({self.返回值})"
        else:
            return "返回语句()"


@dataclass
class 如果语句(语句):
    """
    如果语句
    如: if (condition) { ... } else { ... }
    """
    
    条件: 表达式
    then分支: 语句
    else分支: Optional[语句]
    
    def __init__(self, 条件: 表达式, then分支: 语句, else分支: Optional[语句], 行号: int, 列号: int):
        super().__init__(行号, 列号)
        self.条件 = 条件
        self.then分支 = then分支
        self.else分支 = else分支
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_如果语句(self)
    
    def get_children(self) -> List[ASTNode]:
        children = [self.条件, self.then分支]
        if self.else分支:
            children.append(self.else分支)
        return children
    
    def __repr__(self) -> str:
        if self.else分支:
            return f"如果语句(if {self.条件} then {self.then分支} else {self.else分支})"
        else:
            return f"如果语句(if {self.条件} then {self.then分支})"


@dataclass
class 当语句(语句):
    """
    当语句(while循环)
    如: while (condition) { ... }
    """
    
    条件: 表达式
    循环体: 语句
    
    def __init__(self, 条件: 表达式, 循环体: 语句, 行号: int, 列号: int):
        super().__init__(行号, 列号)
        self.条件 = 条件
        self.循环体 = 循环体
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_当语句(self)
    
    def get_children(self) -> List[ASTNode]:
        return [self.条件, self.循环体]
    
    def __repr__(self) -> str:
        return f"当语句(while {self.条件} do {self.循环体})"


@dataclass
class 代码块语句(语句):
    """
    代码块语句
    如: { statement1; statement2; ... }
    """
    
    语句列表: List[语句]
    
    def __init__(self, 语句列表: List[语句], 行号: int, 列号: int):
        super().__init__(行号, 列号)
        self.语句列表 = 语句列表
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_代码块语句(self)
    
    def get_children(self) -> List[ASTNode]:
        return list(self.语句列表)
    
    def __repr__(self) -> str:
        return f"代码块语句({len(self.语句列表)}个语句)"