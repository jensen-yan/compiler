"""
运算符优先级和结合性定义
"""

from enum import Enum, auto
from typing import Dict, Tuple

from ..lexer.token import TokenType


class 结合性(Enum):
    """运算符结合性"""
    左结合 = auto()
    右结合 = auto()
    无结合 = auto()


class 运算符优先级:
    """
    运算符优先级管理
    数字越大优先级越高
    """
    
    # 优先级定义：(优先级, 结合性)
    _优先级表: Dict[TokenType, Tuple[int, 结合性]] = {
        # 赋值运算符 (最低优先级)
        TokenType.赋值: (1, 结合性.右结合),
        
        # 逻辑或
        TokenType.或: (2, 结合性.左结合),
        
        # 逻辑与
        TokenType.与: (3, 结合性.左结合),
        
        # 相等性比较
        TokenType.等于: (4, 结合性.左结合),
        TokenType.不等于: (4, 结合性.左结合),
        
        # 关系比较
        TokenType.小于: (5, 结合性.左结合),
        TokenType.大于: (5, 结合性.左结合),
        TokenType.小于等于: (5, 结合性.左结合),
        TokenType.大于等于: (5, 结合性.左结合),
        
        # 加减运算
        TokenType.加: (6, 结合性.左结合),
        TokenType.减: (6, 结合性.左结合),
        
        # 乘除模运算
        TokenType.乘: (7, 结合性.左结合),
        TokenType.除: (7, 结合性.左结合),
        TokenType.模: (7, 结合性.左结合),
        
        # 一元运算符 (最高优先级)
        TokenType.非: (8, 结合性.右结合),
        # 一元加减在解析时特殊处理
    }
    
    @classmethod
    def get_优先级(cls, token_type: TokenType) -> int:
        """
        获取运算符优先级
        
        Args:
            token_type: token类型
            
        Returns:
            优先级数值，数字越大优先级越高
        """
        return cls._优先级表.get(token_type, (0, 结合性.无结合))[0]
    
    @classmethod
    def get_结合性(cls, token_type: TokenType) -> 结合性:
        """
        获取运算符结合性
        
        Args:
            token_type: token类型
            
        Returns:
            结合性枚举值
        """
        return cls._优先级表.get(token_type, (0, 结合性.无结合))[1]
    
    @classmethod
    def is_二元运算符(cls, token_type: TokenType) -> bool:
        """
        检查是否为二元运算符
        
        Args:
            token_type: token类型
            
        Returns:
            如果是二元运算符返回True
        """
        return token_type in cls._优先级表
    
    @classmethod
    def is_一元运算符(cls, token_type: TokenType) -> bool:
        """
        检查是否为一元运算符
        
        Args:
            token_type: token类型
            
        Returns:
            如果是一元运算符返回True
        """
        return token_type in {TokenType.非, TokenType.减}
    
    @classmethod
    def is_右结合(cls, token_type: TokenType) -> bool:
        """
        检查运算符是否为右结合
        
        Args:
            token_type: token类型
            
        Returns:
            如果是右结合返回True
        """
        return cls.get_结合性(token_type) == 结合性.右结合