"""
AST基础类定义
包含所有AST节点的基类和访问者模式接口
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional, TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')


class ASTNode(ABC):
    """
    AST节点基类
    所有AST节点都应该继承这个类
    """
    
    def __init__(self, 行号: int = 1, 列号: int = 1):
        """
        初始化AST节点
        
        Args:
            行号: 节点在源代码中的行号
            列号: 节点在源代码中的列号
        """
        self.行号 = 行号
        self.列号 = 列号
    
    @abstractmethod
    def accept(self, visitor: 'ASTVisitor[T]') -> T:
        """
        访问者模式接口
        
        Args:
            visitor: 访问者对象
            
        Returns:
            访问者处理结果
        """
        pass
    
    def __repr__(self) -> str:
        """返回节点的字符串表示"""
        return f"{self.__class__.__name__}({self.行号}:{self.列号})"
    
    def get_children(self) -> List['ASTNode']:
        """
        获取子节点列表
        用于遍历AST
        
        Returns:
            子节点列表
        """
        return []
    
    def get_position(self) -> tuple[int, int]:
        """
        获取节点在源代码中的位置
        
        Returns:
            (行号, 列号)
        """
        return (self.行号, self.列号)


class ASTVisitor(ABC, Generic[T]):
    """
    AST访问者基类
    使用访问者模式遍历和处理AST
    """
    
    def visit(self, node: ASTNode) -> T:
        """
        访问节点的通用方法
        
        Args:
            node: 要访问的节点
            
        Returns:
            访问结果
        """
        return node.accept(self)
    
    def visit_children(self, node: ASTNode) -> List[T]:
        """
        访问所有子节点
        
        Args:
            node: 父节点
            
        Returns:
            子节点访问结果列表
        """
        return [self.visit(child) for child in node.get_children()]
    
    # 表达式访问方法
    @abstractmethod
    def visit_二元运算表达式(self, node: '二元运算表达式') -> T:
        """访问二元运算表达式"""
        pass
    
    @abstractmethod
    def visit_一元运算表达式(self, node: '一元运算表达式') -> T:
        """访问一元运算表达式"""
        pass
    
    @abstractmethod
    def visit_字面量表达式(self, node: '字面量表达式') -> T:
        """访问字面量表达式"""
        pass
    
    @abstractmethod
    def visit_标识符表达式(self, node: '标识符表达式') -> T:
        """访问标识符表达式"""
        pass
    
    @abstractmethod
    def visit_函数调用表达式(self, node: '函数调用表达式') -> T:
        """访问函数调用表达式"""
        pass
    
    @abstractmethod
    def visit_赋值表达式(self, node: '赋值表达式') -> T:
        """访问赋值表达式"""
        pass
    
    # 语句访问方法
    @abstractmethod
    def visit_表达式语句(self, node: '表达式语句') -> T:
        """访问表达式语句"""
        pass
    
    @abstractmethod
    def visit_变量声明语句(self, node: '变量声明语句') -> T:
        """访问变量声明语句"""
        pass
    
    @abstractmethod
    def visit_函数声明语句(self, node: '函数声明语句') -> T:
        """访问函数声明语句"""
        pass
    
    @abstractmethod
    def visit_返回语句(self, node: '返回语句') -> T:
        """访问返回语句"""
        pass
    
    @abstractmethod
    def visit_如果语句(self, node: '如果语句') -> T:
        """访问如果语句"""
        pass
    
    @abstractmethod
    def visit_当语句(self, node: '当语句') -> T:
        """访问当语句"""
        pass
    
    @abstractmethod
    def visit_代码块语句(self, node: '代码块语句') -> T:
        """访问代码块语句"""
        pass
    
    # 程序访问方法
    @abstractmethod
    def visit_程序(self, node: '程序') -> T:
        """访问程序"""
        pass


# 导入循环引用的类型
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .expressions import (
        二元运算表达式, 一元运算表达式, 字面量表达式, 
        标识符表达式, 函数调用表达式, 赋值表达式
    )
    from .statements import (
        表达式语句, 变量声明语句, 函数声明语句, 返回语句,
        如果语句, 当语句, 代码块语句
    )
    from .program import 程序