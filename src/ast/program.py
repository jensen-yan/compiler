"""
程序AST节点定义
程序是整个AST的根节点
"""

from typing import Any, List
from dataclasses import dataclass

from .base import ASTNode, ASTVisitor
from .statements import 语句


@dataclass
class 程序(ASTNode):
    """
    程序节点
    表示整个程序，包含所有顶级语句
    """
    
    语句列表: List[语句]
    
    def __init__(self, 语句列表: List[语句]):
        super().__init__(1, 1)  # 程序从第1行第1列开始
        self.语句列表 = 语句列表
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_程序(self)
    
    def get_children(self) -> List[ASTNode]:
        return list(self.语句列表)
    
    def __repr__(self) -> str:
        return f"程序({len(self.语句列表)}个语句)"