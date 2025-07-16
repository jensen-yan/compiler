"""
符号表系统
包含符号定义、符号表管理、作用域管理等
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum, auto

from .types import 类型, 基本类型, 函数类型


class 符号种类(Enum):
    """符号种类枚举"""
    变量 = auto()
    函数 = auto()
    参数 = auto()


class 符号(ABC):
    """符号基类"""
    
    def __init__(self, 名称: str, 类型: 类型, 行号: int = 0, 列号: int = 0):
        self.名称 = 名称
        self.类型 = 类型
        self.行号 = 行号
        self.列号 = 列号
    
    @abstractmethod
    def get_种类(self) -> 符号种类:
        """获取符号种类"""
        pass
    
    def __str__(self) -> str:
        return f"{self.get_种类().name}({self.名称}: {self.类型})"
    
    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class 变量符号(符号):
    """变量符号"""
    
    是否已初始化: bool = False
    
    def __init__(self, 名称: str, 类型: 类型, 行号: int = 0, 列号: int = 0, 是否已初始化: bool = False):
        super().__init__(名称, 类型, 行号, 列号)
        self.是否已初始化 = 是否已初始化
    
    def get_种类(self) -> 符号种类:
        return 符号种类.变量
    
    def mark_initialized(self):
        """标记为已初始化"""
        self.是否已初始化 = True


@dataclass
class 函数符号(符号):
    """函数符号"""
    
    参数列表: List[str]
    是否已定义: bool = False
    
    def __init__(self, 名称: str, 函数类型: 函数类型, 参数列表: List[str], 
                 行号: int = 0, 列号: int = 0, 是否已定义: bool = False):
        super().__init__(名称, 函数类型, 行号, 列号)
        self.参数列表 = 参数列表
        self.是否已定义 = 是否已定义
    
    def get_种类(self) -> 符号种类:
        return 符号种类.函数
    
    def mark_defined(self):
        """标记为已定义"""
        self.是否已定义 = True
    
    def get_函数类型(self) -> 函数类型:
        """获取函数类型"""
        if isinstance(self.类型, 函数类型):
            return self.类型
        else:
            # 这种情况理论上不应该发生，但为了类型安全
            raise TypeError(f"符号 {self.名称} 的类型不是函数类型")


@dataclass
class 参数符号(符号):
    """参数符号"""
    
    参数位置: int
    
    def __init__(self, 名称: str, 类型: 类型, 参数位置: int, 行号: int = 0, 列号: int = 0):
        super().__init__(名称, 类型, 行号, 列号)
        self.参数位置 = 参数位置
    
    def get_种类(self) -> 符号种类:
        return 符号种类.参数


class 符号表:
    """
    符号表类
    管理单个作用域内的符号
    """
    
    def __init__(self, 名称: str = ""):
        self.名称 = 名称
        self.符号映射: Dict[str, 符号] = {}
    
    def define(self, 符号: 符号) -> bool:
        """
        定义符号
        
        Args:
            符号: 要定义的符号
            
        Returns:
            如果成功定义返回True，如果已存在返回False
        """
        if 符号.名称 in self.符号映射:
            return False
        
        self.符号映射[符号.名称] = 符号
        return True
    
    def lookup(self, 名称: str) -> Optional[符号]:
        """
        查找符号
        
        Args:
            名称: 符号名称
            
        Returns:
            找到的符号，如果不存在返回None
        """
        return self.符号映射.get(名称)
    
    def exists(self, 名称: str) -> bool:
        """
        检查符号是否存在
        
        Args:
            名称: 符号名称
            
        Returns:
            如果存在返回True
        """
        return 名称 in self.符号映射
    
    def get_all_symbols(self) -> List[符号]:
        """获取所有符号"""
        return list(self.符号映射.values())
    
    def get_symbol_count(self) -> int:
        """获取符号数量"""
        return len(self.符号映射)
    
    def __str__(self) -> str:
        symbols = [f"  {symbol}" for symbol in self.符号映射.values()]
        return f"符号表({self.名称}):\n" + "\n".join(symbols) if symbols else f"符号表({self.名称}): 空"
    
    def __repr__(self) -> str:
        return self.__str__()


class 作用域管理器:
    """
    作用域管理器
    管理多层作用域的符号表栈
    """
    
    def __init__(self):
        self.作用域栈: List[符号表] = []
        self.全局作用域: Optional[符号表] = None
    
    def enter_scope(self, 名称: str = "") -> None:
        """
        进入新作用域
        
        Args:
            名称: 作用域名称
        """
        new_scope = 符号表(名称)
        self.作用域栈.append(new_scope)
        
        # 如果是第一个作用域，设为全局作用域
        if self.全局作用域 is None:
            self.全局作用域 = new_scope
    
    def exit_scope(self) -> Optional[符号表]:
        """
        退出当前作用域
        
        Returns:
            退出的符号表，如果没有作用域返回None
        """
        if self.作用域栈:
            return self.作用域栈.pop()
        return None
    
    def current_scope(self) -> Optional[符号表]:
        """
        获取当前作用域
        
        Returns:
            当前符号表，如果没有作用域返回None
        """
        return self.作用域栈[-1] if self.作用域栈 else None
    
    def define_symbol(self, 符号: 符号) -> bool:
        """
        在当前作用域定义符号
        
        Args:
            符号: 要定义的符号
            
        Returns:
            如果成功定义返回True
        """
        current = self.current_scope()
        if current:
            return current.define(符号)
        return False
    
    def lookup_symbol(self, 名称: str) -> Optional[符号]:
        """
        查找符号（从当前作用域向上搜索）
        
        Args:
            名称: 符号名称
            
        Returns:
            找到的符号，如果不存在返回None
        """
        # 从当前作用域向上搜索
        for scope in reversed(self.作用域栈):
            symbol = scope.lookup(名称)
            if symbol:
                return symbol
        return None
    
    def lookup_symbol_current_scope(self, 名称: str) -> Optional[符号]:
        """
        仅在当前作用域查找符号
        
        Args:
            名称: 符号名称
            
        Returns:
            找到的符号，如果不存在返回None
        """
        current = self.current_scope()
        if current:
            return current.lookup(名称)
        return None
    
    def is_global_scope(self) -> bool:
        """检查是否在全局作用域"""
        return len(self.作用域栈) == 1
    
    def get_scope_depth(self) -> int:
        """获取作用域深度"""
        return len(self.作用域栈)
    
    def get_all_scopes(self) -> List[符号表]:
        """获取所有作用域"""
        return self.作用域栈.copy()
    
    def __str__(self) -> str:
        if not self.作用域栈:
            return "作用域管理器: 空"
        
        result = ["作用域管理器:"]
        for i, scope in enumerate(self.作用域栈):
            indent = "  " * i
            result.append(f"{indent}作用域 {i}: {scope.名称}")
            for symbol in scope.get_all_symbols():
                result.append(f"{indent}  {symbol}")
        
        return "\n".join(result)
    
    def __repr__(self) -> str:
        return self.__str__()


def create_builtin_symbols() -> List[符号]:
    """
    创建内置符号
    
    Returns:
        内置符号列表
    """
    from .types import 类型系统
    
    type_system = 类型系统()
    builtins = []
    
    # 内置函数：print
    print_func_type = 函数类型(
        [type_system.字符串类型], 
        type_system.空值类型
    )
    print_symbol = 函数符号(
        "print", 
        print_func_type, 
        ["message"], 
        是否已定义=True
    )
    builtins.append(print_symbol)
    
    # 内置函数：len
    len_func_type = 函数类型(
        [type_system.字符串类型], 
        type_system.整数类型
    )
    len_symbol = 函数符号(
        "len", 
        len_func_type, 
        ["s"], 
        是否已定义=True
    )
    builtins.append(len_symbol)
    
    # 内置函数：str
    str_func_type = 函数类型(
        [type_system.整数类型], 
        type_system.字符串类型
    )
    str_symbol = 函数符号(
        "str", 
        str_func_type, 
        ["value"], 
        是否已定义=True
    )
    builtins.append(str_symbol)
    
    return builtins