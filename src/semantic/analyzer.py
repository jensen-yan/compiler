"""
语义分析器实现
负责类型检查、作用域分析、符号表管理等
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from ..ast import *
from ..lexer.token import Token, TokenType
from .types import 类型, 基本类型, 函数类型, 类型系统, 基本类型枚举
from .symbols import 符号, 变量符号, 函数符号, 参数符号, 符号表, 作用域管理器, create_builtin_symbols


class 语义错误(Exception):
    """语义分析错误"""
    
    def __init__(self, message: str, 行号: int = 0, 列号: int = 0):
        super().__init__(f"语义错误在 {行号}:{列号} - {message}")
        self.message = message
        self.行号 = 行号
        self.列号 = 列号


@dataclass
class 分析结果:
    """语义分析结果"""
    类型: 类型
    是否可赋值: bool = False
    
    def __str__(self) -> str:
        return f"分析结果(类型: {self.类型}, 可赋值: {self.是否可赋值})"


class 语义分析器(ASTVisitor[分析结果]):
    """
    语义分析器
    使用访问者模式遍历AST，进行类型检查和作用域分析
    """
    
    def __init__(self):
        self.类型系统 = 类型系统()
        self.作用域管理器 = 作用域管理器()
        self.错误列表: List[语义错误] = []
        self.当前函数返回类型: Optional[类型] = None
        self.在赋值左侧 = False  # 标志是否在赋值表达式的左侧
        
        # 初始化全局作用域
        self.作用域管理器.enter_scope("全局作用域")
        
        # 添加内置符号
        for builtin in create_builtin_symbols():
            self.作用域管理器.define_symbol(builtin)
    
    def error(self, message: str, 行号: int = 0, 列号: int = 0) -> None:
        """记录语义错误"""
        error = 语义错误(message, 行号, 列号)
        self.错误列表.append(error)
    
    def analyze(self, ast: 程序) -> List[语义错误]:
        """
        分析AST
        
        Args:
            ast: 程序AST节点
            
        Returns:
            错误列表
        """
        self.错误列表.clear()
        self.visit(ast)
        return self.错误列表
    
    def visit_程序(self, node: 程序) -> 分析结果:
        """访问程序节点"""
        for stmt in node.语句列表:
            self.visit(stmt)
        
        return 分析结果(self.类型系统.空值类型)
    
    def visit_函数声明语句(self, node: 函数声明语句) -> 分析结果:
        """访问函数声明语句"""
        # 检查函数名是否已存在
        existing_symbol = self.作用域管理器.lookup_symbol_current_scope(node.名称)
        if existing_symbol:
            self.error(f"函数 '{node.名称}' 已经定义", node.行号, node.列号)
            return 分析结果(self.类型系统.未知类型)
        
        # 创建函数参数类型列表（暂时都设为未知类型，实际项目中可以从类型注解推导）
        参数类型列表: List[类型] = [self.类型系统.未知类型 for _ in node.参数列表]
        
        # 创建函数类型（返回类型暂时设为未知，后续通过return语句推导）
        函数类型_obj = 函数类型(参数类型列表, self.类型系统.未知类型)
        
        # 创建函数符号并定义
        函数符号_obj = 函数符号(node.名称, 函数类型_obj, node.参数列表, node.行号, node.列号)
        self.作用域管理器.define_symbol(函数符号_obj)
        
        # 进入函数作用域
        self.作用域管理器.enter_scope(f"函数_{node.名称}")
        
        # 定义参数符号
        for i, param_name in enumerate(node.参数列表):
            param_symbol = 参数符号(param_name, self.类型系统.未知类型, i, node.行号, node.列号)
            if not self.作用域管理器.define_symbol(param_symbol):
                self.error(f"参数 '{param_name}' 重复定义", node.行号, node.列号)
        
        # 保存当前函数返回类型上下文
        old_return_type = self.当前函数返回类型
        self.当前函数返回类型 = None
        
        # 分析函数体
        self.visit(node.函数体)
        
        # 推导函数返回类型
        if self.当前函数返回类型:
            函数类型_obj.返回类型 = self.当前函数返回类型
        else:
            # 如果没有return语句，返回类型为void
            函数类型_obj.返回类型 = self.类型系统.空值类型
        
        # 恢复函数返回类型上下文
        self.当前函数返回类型 = old_return_type
        
        # 退出函数作用域
        self.作用域管理器.exit_scope()
        
        # 标记函数为已定义
        函数符号_obj.mark_defined()
        
        return 分析结果(函数类型_obj)
    
    def visit_返回语句(self, node: 返回语句) -> 分析结果:
        """访问返回语句"""
        返回值类型 = self.类型系统.空值类型
        
        if node.返回值:
            result = self.visit(node.返回值)
            返回值类型 = result.类型
        
        # 更新当前函数的返回类型
        if self.当前函数返回类型 is None:
            self.当前函数返回类型 = 返回值类型
        elif (not self.当前函数返回类型.is_compatible_with(返回值类型) and 
              返回值类型 != self.类型系统.未知类型 and
              self.当前函数返回类型 != self.类型系统.未知类型):
            self.error(f"返回类型不一致：期望 {self.当前函数返回类型}，实际 {返回值类型}", 
                      node.行号, node.列号)
        
        return 分析结果(返回值类型)
    
    def visit_变量声明语句(self, node: 变量声明语句) -> 分析结果:
        """访问变量声明语句"""
        # 检查变量名是否已存在
        existing_symbol = self.作用域管理器.lookup_symbol_current_scope(node.名称)
        if existing_symbol:
            self.error(f"变量 '{node.名称}' 已经定义", node.行号, node.列号)
            return 分析结果(self.类型系统.未知类型)
        
        变量类型 = self.类型系统.未知类型
        是否已初始化 = False
        
        # 如果有初始值，推导类型
        if node.初始值:
            result = self.visit(node.初始值)
            变量类型 = result.类型
            是否已初始化 = True
        
        # 创建变量符号并定义
        变量符号_obj = 变量符号(node.名称, 变量类型, node.行号, node.列号, 是否已初始化)
        self.作用域管理器.define_symbol(变量符号_obj)
        
        return 分析结果(变量类型)
    
    def visit_表达式语句(self, node: 表达式语句) -> 分析结果:
        """访问表达式语句"""
        return self.visit(node.表达式)
    
    def visit_代码块语句(self, node: 代码块语句) -> 分析结果:
        """访问代码块语句"""
        # 进入新作用域
        self.作用域管理器.enter_scope("代码块")
        
        # 分析所有语句
        for stmt in node.语句列表:
            self.visit(stmt)
        
        # 退出作用域
        self.作用域管理器.exit_scope()
        
        return 分析结果(self.类型系统.空值类型)
    
    def visit_如果语句(self, node: 如果语句) -> 分析结果:
        """访问如果语句"""
        # 分析条件表达式
        condition_result = self.visit(node.条件)
        
        # 检查条件是否为布尔类型（允许未知类型）
        if (isinstance(condition_result.类型, 基本类型) and 
            condition_result.类型.类型值 != 基本类型枚举.布尔值 and
            condition_result.类型.类型值 != 基本类型枚举.未知):
            self.error(f"条件必须是布尔类型，实际是 {condition_result.类型}", node.行号, node.列号)
        
        # 分析then分支
        self.visit(node.then分支)
        
        # 分析else分支
        if node.else分支:
            self.visit(node.else分支)
        
        return 分析结果(self.类型系统.空值类型)
    
    def visit_当语句(self, node: 当语句) -> 分析结果:
        """访问当语句（while循环）"""
        # 分析条件表达式
        condition_result = self.visit(node.条件)
        
        # 检查条件是否为布尔类型（允许未知类型）
        if (isinstance(condition_result.类型, 基本类型) and 
            condition_result.类型.类型值 != 基本类型枚举.布尔值 and
            condition_result.类型.类型值 != 基本类型枚举.未知):
            self.error(f"while条件必须是布尔类型，实际是 {condition_result.类型}", node.行号, node.列号)
        
        # 分析循环体
        self.visit(node.循环体)
        
        return 分析结果(self.类型系统.空值类型)
    
    def visit_赋值表达式(self, node: 赋值表达式) -> 分析结果:
        """访问赋值表达式"""
        # 分析值
        value_result = self.visit(node.值)
        
        # 检查目标是否为标识符（变量）
        if isinstance(node.目标, 标识符表达式):
            var_name = node.目标.名称
            existing_symbol = self.作用域管理器.lookup_symbol(var_name)
            
            if existing_symbol is None:
                # 如果变量不存在，创建新变量（隐式声明）
                var_symbol = 变量符号(var_name, value_result.类型, node.行号, node.列号, True)
                self.作用域管理器.define_symbol(var_symbol)
                return 分析结果(value_result.类型)
            else:
                # 如果变量存在，检查赋值兼容性
                if not isinstance(existing_symbol, (变量符号, 参数符号)):
                    self.error(f"'{var_name}' 不是变量", node.行号, node.列号)
                    return 分析结果(self.类型系统.未知类型)
                
                # 检查类型兼容性（未知类型可以赋值给任何类型）
                if (existing_symbol.类型 != self.类型系统.未知类型 and 
                    not self.类型系统.check_assignment(existing_symbol.类型, value_result.类型)):
                    self.error(f"类型不兼容：无法将 {value_result.类型} 赋值给 {existing_symbol.类型}", 
                              node.行号, node.列号)
                
                # 如果变量类型是未知的，更新为实际类型
                if existing_symbol.类型 == self.类型系统.未知类型:
                    existing_symbol.类型 = value_result.类型
                
                # 标记变量为已初始化
                if isinstance(existing_symbol, 变量符号):
                    existing_symbol.mark_initialized()
                
                return 分析结果(existing_symbol.类型)
        else:
            # 其他类型的赋值目标（如数组元素等，目前不支持）
            self.error("不支持的赋值目标", node.行号, node.列号)
            return 分析结果(self.类型系统.未知类型)
    
    def visit_二元运算表达式(self, node: 二元运算表达式) -> 分析结果:
        """访问二元运算表达式"""
        # 分析左右操作数
        left_result = self.visit(node.左操作数)
        right_result = self.visit(node.右操作数)
        
        # 检查运算类型
        result_type = self.类型系统.check_binary_operation(
            left_result.类型, node.运算符.类型, right_result.类型
        )
        
        if result_type is None:
            self.error(f"不支持的二元运算：{left_result.类型} {node.运算符.值} {right_result.类型}", 
                      node.行号, node.列号)
            result_type = self.类型系统.未知类型
        
        return 分析结果(result_type)
    
    def visit_一元运算表达式(self, node: 一元运算表达式) -> 分析结果:
        """访问一元运算表达式"""
        # 分析操作数
        operand_result = self.visit(node.操作数)
        
        # 检查运算类型
        result_type = self.类型系统.check_unary_operation(
            node.运算符.类型, operand_result.类型
        )
        
        if result_type is None:
            self.error(f"不支持的一元运算：{node.运算符.值}{operand_result.类型}", 
                      node.行号, node.列号)
            result_type = self.类型系统.未知类型
        
        return 分析结果(result_type)
    
    def visit_函数调用表达式(self, node: 函数调用表达式) -> 分析结果:
        """访问函数调用表达式"""
        # 分析函数表达式
        func_result = self.visit(node.函数)
        
        # 分析参数
        arg_results = [self.visit(arg) for arg in node.参数列表]
        arg_types = [result.类型 for result in arg_results]
        
        # 检查函数调用类型
        if isinstance(func_result.类型, 函数类型):
            # 检查参数数量
            if len(arg_types) != len(func_result.类型.参数类型列表):
                self.error(f"函数调用参数不匹配：期望 {len(func_result.类型.参数类型列表)} 个参数，实际 {len(arg_types)} 个", 
                          node.行号, node.列号)
                result_type = self.类型系统.未知类型
            else:
                # 对于未知类型的参数，我们允许任何类型
                result_type = func_result.类型.返回类型
        else:
            self.error(f"'{func_result.类型}' 不是函数类型", node.行号, node.列号)
            result_type = self.类型系统.未知类型
        
        return 分析结果(result_type)
    
    def visit_标识符表达式(self, node: 标识符表达式) -> 分析结果:
        """访问标识符表达式"""
        # 查找符号
        symbol = self.作用域管理器.lookup_symbol(node.名称)
        
        if symbol is None:
            self.error(f"未定义的标识符 '{node.名称}'", node.行号, node.列号)
            return 分析结果(self.类型系统.未知类型, True)
        
        # 检查变量是否已初始化
        if isinstance(symbol, 变量符号) and not symbol.是否已初始化:
            self.error(f"变量 '{node.名称}' 在初始化前使用", node.行号, node.列号)
        
        # 变量和参数可以赋值
        是否可赋值 = isinstance(symbol, (变量符号, 参数符号))
        
        return 分析结果(symbol.类型, 是否可赋值)
    
    def visit_字面量表达式(self, node: 字面量表达式) -> 分析结果:
        """访问字面量表达式"""
        # 推导字面量类型
        literal_type = self.类型系统.infer_literal_type(node.类型, node.值)
        return 分析结果(literal_type)
    
    def get_symbol_table_info(self) -> str:
        """获取符号表信息（用于调试）"""
        return str(self.作用域管理器)
    
    def has_errors(self) -> bool:
        """检查是否有错误"""
        return len(self.错误列表) > 0
    
    def get_error_summary(self) -> str:
        """获取错误摘要"""
        if not self.错误列表:
            return "没有语义错误"
        
        summary = [f"发现 {len(self.错误列表)} 个语义错误:"]
        for i, error in enumerate(self.错误列表, 1):
            summary.append(f"  {i}. {error}")
        
        return "\n".join(summary)