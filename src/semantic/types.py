"""
类型系统定义
包含类型表示、类型检查、类型推导等功能
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from enum import Enum, auto
from dataclasses import dataclass

from ..lexer.token import TokenType


class 基本类型枚举(Enum):
    """基本类型枚举"""
    整数 = auto()
    浮点数 = auto()
    字符串 = auto()
    布尔值 = auto()
    空值 = auto()
    未知 = auto()


class 类型(ABC):
    """类型基类"""
    
    @abstractmethod
    def __str__(self) -> str:
        """返回类型的字符串表示"""
        pass
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        """类型相等性比较"""
        pass
    
    @abstractmethod
    def is_compatible_with(self, other: '类型') -> bool:
        """检查是否与另一个类型兼容"""
        pass
    
    def is_numeric(self) -> bool:
        """检查是否为数值类型"""
        return False
    
    def is_assignable_from(self, other: '类型') -> bool:
        """检查是否可以从另一个类型赋值"""
        return self.is_compatible_with(other)


@dataclass
class 基本类型(类型):
    """基本类型实现"""
    
    类型值: 基本类型枚举
    
    def __str__(self) -> str:
        type_names = {
            基本类型枚举.整数: "整数",
            基本类型枚举.浮点数: "浮点数",
            基本类型枚举.字符串: "字符串",
            基本类型枚举.布尔值: "布尔值",
            基本类型枚举.空值: "空值",
            基本类型枚举.未知: "未知",
        }
        return type_names.get(self.类型值, "未知类型")
    
    def __eq__(self, other) -> bool:
        return isinstance(other, 基本类型) and self.类型值 == other.类型值
    
    def is_compatible_with(self, other: 类型) -> bool:
        if isinstance(other, 基本类型):
            # 数值类型间的兼容性
            if self.is_numeric() and other.is_numeric():
                return True
            # 相同类型兼容
            return self.类型值 == other.类型值
        return False
    
    def is_numeric(self) -> bool:
        return self.类型值 in {基本类型枚举.整数, 基本类型枚举.浮点数}
    
    def is_assignable_from(self, other: 类型) -> bool:
        if isinstance(other, 基本类型):
            # 整数可以赋值给浮点数
            if self.类型值 == 基本类型枚举.浮点数 and other.类型值 == 基本类型枚举.整数:
                return True
            # 相同类型可以赋值
            return self.类型值 == other.类型值
        return False


@dataclass
class 函数类型(类型):
    """函数类型实现"""
    
    参数类型列表: List[类型]
    返回类型: 类型
    
    def __str__(self) -> str:
        params = ", ".join(str(param) for param in self.参数类型列表)
        return f"函数({params}) -> {self.返回类型}"
    
    def __eq__(self, other) -> bool:
        return (isinstance(other, 函数类型) and 
                self.参数类型列表 == other.参数类型列表 and
                self.返回类型 == other.返回类型)
    
    def is_compatible_with(self, other: 类型) -> bool:
        if isinstance(other, 函数类型):
            # 参数类型必须完全匹配
            if len(self.参数类型列表) != len(other.参数类型列表):
                return False
            
            for self_param, other_param in zip(self.参数类型列表, other.参数类型列表):
                if not self_param.is_compatible_with(other_param):
                    return False
            
            # 返回类型必须兼容
            return self.返回类型.is_compatible_with(other.返回类型)
        
        return False


class 类型系统:
    """
    类型系统管理器
    负责类型推导、类型检查、类型转换等
    """
    
    def __init__(self):
        """初始化类型系统"""
        # 预定义的基本类型
        self.整数类型 = 基本类型(基本类型枚举.整数)
        self.浮点数类型 = 基本类型(基本类型枚举.浮点数)
        self.字符串类型 = 基本类型(基本类型枚举.字符串)
        self.布尔值类型 = 基本类型(基本类型枚举.布尔值)
        self.空值类型 = 基本类型(基本类型枚举.空值)
        self.未知类型 = 基本类型(基本类型枚举.未知)
        
        # 二元运算符类型规则
        self.二元运算符类型规则 = {
            # 算术运算符
            TokenType.加: self._算术运算类型规则,
            TokenType.减: self._算术运算类型规则,
            TokenType.乘: self._算术运算类型规则,
            TokenType.除: self._算术运算类型规则,
            TokenType.模: self._算术运算类型规则,
            
            # 比较运算符
            TokenType.等于: self._比较运算类型规则,
            TokenType.不等于: self._比较运算类型规则,
            TokenType.小于: self._比较运算类型规则,
            TokenType.大于: self._比较运算类型规则,
            TokenType.小于等于: self._比较运算类型规则,
            TokenType.大于等于: self._比较运算类型规则,
            
            # 逻辑运算符
            TokenType.与: self._逻辑运算类型规则,
            TokenType.或: self._逻辑运算类型规则,
        }
        
        # 一元运算符类型规则
        self.一元运算符类型规则 = {
            TokenType.减: self._一元减法类型规则,
            TokenType.非: self._一元非类型规则,
        }
    
    def infer_literal_type(self, token_type: TokenType, value: Any) -> 类型:
        """
        推导字面量类型
        
        Args:
            token_type: token类型
            value: 字面量值
            
        Returns:
            推导出的类型
        """
        if token_type == TokenType.整数:
            return self.整数类型
        elif token_type == TokenType.浮点数:
            return self.浮点数类型
        elif token_type == TokenType.字符串:
            return self.字符串类型
        elif token_type == TokenType.布尔值:
            return self.布尔值类型
        elif value is None:
            return self.空值类型
        else:
            return self.未知类型
    
    def check_binary_operation(self, left_type: 类型, operator: TokenType, right_type: 类型) -> Optional[类型]:
        """
        检查二元运算的类型
        
        Args:
            left_type: 左操作数类型
            operator: 运算符
            right_type: 右操作数类型
            
        Returns:
            运算结果类型，如果类型不匹配返回None
        """
        if operator in self.二元运算符类型规则:
            return self.二元运算符类型规则[operator](left_type, right_type)
        return None
    
    def check_unary_operation(self, operator: TokenType, operand_type: 类型) -> Optional[类型]:
        """
        检查一元运算的类型
        
        Args:
            operator: 运算符
            operand_type: 操作数类型
            
        Returns:
            运算结果类型，如果类型不匹配返回None
        """
        if operator in self.一元运算符类型规则:
            return self.一元运算符类型规则[operator](operand_type)
        return None
    
    def check_assignment(self, target_type: 类型, value_type: 类型) -> bool:
        """
        检查赋值操作的类型兼容性
        
        Args:
            target_type: 目标类型
            value_type: 值类型
            
        Returns:
            如果可以赋值返回True
        """
        return target_type.is_assignable_from(value_type)
    
    def check_function_call(self, func_type: 类型, arg_types: List[类型]) -> Optional[类型]:
        """
        检查函数调用的类型
        
        Args:
            func_type: 函数类型
            arg_types: 参数类型列表
            
        Returns:
            函数返回类型，如果参数不匹配返回None
        """
        if not isinstance(func_type, 函数类型):
            return None
        
        # 检查参数数量
        if len(arg_types) != len(func_type.参数类型列表):
            return None
        
        # 检查参数类型
        for arg_type, param_type in zip(arg_types, func_type.参数类型列表):
            if not param_type.is_assignable_from(arg_type):
                return None
        
        return func_type.返回类型
    
    def _算术运算类型规则(self, left_type: 类型, right_type: 类型) -> Optional[类型]:
        """算术运算类型规则"""
        if isinstance(left_type, 基本类型) and isinstance(right_type, 基本类型):
            # 如果有未知类型，返回未知类型
            if (left_type.类型值 == 基本类型枚举.未知 or 
                right_type.类型值 == 基本类型枚举.未知):
                return self.未知类型
            
            # 两个都是数值类型
            if left_type.is_numeric() and right_type.is_numeric():
                # 如果有浮点数，结果是浮点数
                if (left_type.类型值 == 基本类型枚举.浮点数 or 
                    right_type.类型值 == 基本类型枚举.浮点数):
                    return self.浮点数类型
                else:
                    return self.整数类型
            
            # 字符串加法
            if (left_type.类型值 == 基本类型枚举.字符串 and 
                right_type.类型值 == 基本类型枚举.字符串):
                return self.字符串类型
        
        return None
    
    def _比较运算类型规则(self, left_type: 类型, right_type: 类型) -> Optional[类型]:
        """比较运算类型规则"""
        if isinstance(left_type, 基本类型) and isinstance(right_type, 基本类型):
            # 如果有未知类型，返回布尔值类型
            if (left_type.类型值 == 基本类型枚举.未知 or 
                right_type.类型值 == 基本类型枚举.未知):
                return self.布尔值类型
            
            # 数值类型可以比较
            if left_type.is_numeric() and right_type.is_numeric():
                return self.布尔值类型
            
            # 相同类型可以比较
            if left_type.类型值 == right_type.类型值:
                return self.布尔值类型
        
        return None
    
    def _逻辑运算类型规则(self, left_type: 类型, right_type: 类型) -> Optional[类型]:
        """逻辑运算类型规则"""
        if isinstance(left_type, 基本类型) and isinstance(right_type, 基本类型):
            # 如果有未知类型，返回布尔值类型
            if (left_type.类型值 == 基本类型枚举.未知 or 
                right_type.类型值 == 基本类型枚举.未知):
                return self.布尔值类型
            
            # 布尔值可以进行逻辑运算
            if (left_type.类型值 == 基本类型枚举.布尔值 and 
                right_type.类型值 == 基本类型枚举.布尔值):
                return self.布尔值类型
        
        return None
    
    def _一元减法类型规则(self, operand_type: 类型) -> Optional[类型]:
        """一元减法类型规则"""
        if isinstance(operand_type, 基本类型):
            # 如果是未知类型，返回未知类型
            if operand_type.类型值 == 基本类型枚举.未知:
                return self.未知类型
            # 数值类型可以取负
            if operand_type.is_numeric():
                return operand_type
        return None
    
    def _一元非类型规则(self, operand_type: 类型) -> Optional[类型]:
        """一元非类型规则"""
        if isinstance(operand_type, 基本类型):
            # 如果是未知类型，返回布尔值类型
            if operand_type.类型值 == 基本类型枚举.未知:
                return self.布尔值类型
            # 布尔值可以取非
            if operand_type.类型值 == 基本类型枚举.布尔值:
                return self.布尔值类型
        return None
    
    def get_common_type(self, type1: 类型, type2: 类型) -> Optional[类型]:
        """
        获取两个类型的公共类型
        
        Args:
            type1: 类型1
            type2: 类型2
            
        Returns:
            公共类型，如果没有返回None
        """
        if type1 == type2:
            return type1
        
        if isinstance(type1, 基本类型) and isinstance(type2, 基本类型):
            # 数值类型的公共类型
            if type1.is_numeric() and type2.is_numeric():
                if (type1.类型值 == 基本类型枚举.浮点数 or 
                    type2.类型值 == 基本类型枚举.浮点数):
                    return self.浮点数类型
                else:
                    return self.整数类型
        
        return None