"""
AST节点的单元测试
"""

import pytest
from src.ast import *
from src.lexer.token import Token, TokenType


class TestASTExpressions:
    """表达式AST节点测试"""
    
    def test_字面量表达式(self):
        """测试字面量表达式"""
        token = Token(TokenType.整数, 123, 1, 1)
        expr = 字面量表达式(token)
        
        assert expr.值 == 123
        assert expr.类型 == TokenType.整数
        assert expr.行号 == 1
        assert expr.列号 == 1
        assert expr.get_children() == []
    
    def test_标识符表达式(self):
        """测试标识符表达式"""
        token = Token(TokenType.标识符, "variable", 2, 3)
        expr = 标识符表达式(token)
        
        assert expr.名称 == "variable"
        assert expr.行号 == 2
        assert expr.列号 == 3
        assert expr.get_children() == []
    
    def test_二元运算表达式(self):
        """测试二元运算表达式"""
        left = 字面量表达式(Token(TokenType.整数, 1, 1, 1))
        right = 字面量表达式(Token(TokenType.整数, 2, 1, 5))
        op = Token(TokenType.加, "+", 1, 3)
        
        expr = 二元运算表达式(left, op, right)
        
        assert expr.左操作数 == left
        assert expr.右操作数 == right
        assert expr.运算符 == op
        assert expr.行号 == 1
        assert expr.列号 == 3
        assert expr.get_children() == [left, right]
    
    def test_一元运算表达式(self):
        """测试一元运算表达式"""
        operand = 字面量表达式(Token(TokenType.整数, 42, 1, 2))
        op = Token(TokenType.减, "-", 1, 1)
        
        expr = 一元运算表达式(op, operand)
        
        assert expr.运算符 == op
        assert expr.操作数 == operand
        assert expr.行号 == 1
        assert expr.列号 == 1
        assert expr.get_children() == [operand]
    
    def test_函数调用表达式(self):
        """测试函数调用表达式"""
        func = 标识符表达式(Token(TokenType.标识符, "add", 1, 1))
        arg1 = 字面量表达式(Token(TokenType.整数, 1, 1, 5))
        arg2 = 字面量表达式(Token(TokenType.整数, 2, 1, 8))
        
        expr = 函数调用表达式(func, [arg1, arg2], 1, 1)
        
        assert expr.函数 == func
        assert expr.参数列表 == [arg1, arg2]
        assert expr.行号 == 1
        assert expr.列号 == 1
        assert expr.get_children() == [func, arg1, arg2]
    
    def test_赋值表达式(self):
        """测试赋值表达式"""
        target = 标识符表达式(Token(TokenType.标识符, "x", 1, 1))
        value = 字面量表达式(Token(TokenType.整数, 42, 1, 5))
        
        expr = 赋值表达式(target, value, 1, 1)
        
        assert expr.目标 == target
        assert expr.值 == value
        assert expr.行号 == 1
        assert expr.列号 == 1
        assert expr.get_children() == [target, value]


class TestASTStatements:
    """语句AST节点测试"""
    
    def test_表达式语句(self):
        """测试表达式语句"""
        expr = 字面量表达式(Token(TokenType.整数, 123, 1, 1))
        stmt = 表达式语句(expr)
        
        assert stmt.表达式 == expr
        assert stmt.行号 == 1
        assert stmt.列号 == 1
        assert stmt.get_children() == [expr]
    
    def test_变量声明语句_有初始值(self):
        """测试带初始值的变量声明语句"""
        初始值 = 字面量表达式(Token(TokenType.整数, 42, 1, 7))
        stmt = 变量声明语句("x", 初始值, 1, 1)
        
        assert stmt.名称 == "x"
        assert stmt.初始值 == 初始值
        assert stmt.行号 == 1
        assert stmt.列号 == 1
        assert stmt.get_children() == [初始值]
    
    def test_变量声明语句_无初始值(self):
        """测试无初始值的变量声明语句"""
        stmt = 变量声明语句("y", None, 1, 1)
        
        assert stmt.名称 == "y"
        assert stmt.初始值 is None
        assert stmt.行号 == 1
        assert stmt.列号 == 1
        assert stmt.get_children() == []
    
    def test_返回语句_有返回值(self):
        """测试带返回值的返回语句"""
        返回值 = 字面量表达式(Token(TokenType.整数, 42, 1, 8))
        stmt = 返回语句(返回值, 1, 1)
        
        assert stmt.返回值 == 返回值
        assert stmt.行号 == 1
        assert stmt.列号 == 1
        assert stmt.get_children() == [返回值]
    
    def test_返回语句_无返回值(self):
        """测试无返回值的返回语句"""
        stmt = 返回语句(None, 1, 1)
        
        assert stmt.返回值 is None
        assert stmt.行号 == 1
        assert stmt.列号 == 1
        assert stmt.get_children() == []
    
    def test_代码块语句(self):
        """测试代码块语句"""
        stmt1 = 表达式语句(字面量表达式(Token(TokenType.整数, 1, 1, 1)))
        stmt2 = 表达式语句(字面量表达式(Token(TokenType.整数, 2, 2, 1)))
        
        block = 代码块语句([stmt1, stmt2], 1, 1)
        
        assert block.语句列表 == [stmt1, stmt2]
        assert block.行号 == 1
        assert block.列号 == 1
        assert block.get_children() == [stmt1, stmt2]
    
    def test_如果语句_有else分支(self):
        """测试带else分支的如果语句"""
        条件 = 字面量表达式(Token(TokenType.布尔值, True, 1, 4))
        then分支 = 表达式语句(字面量表达式(Token(TokenType.整数, 1, 1, 1)))
        else分支 = 表达式语句(字面量表达式(Token(TokenType.整数, 2, 1, 1)))
        
        stmt = 如果语句(条件, then分支, else分支, 1, 1)
        
        assert stmt.条件 == 条件
        assert stmt.then分支 == then分支
        assert stmt.else分支 == else分支
        assert stmt.行号 == 1
        assert stmt.列号 == 1
        assert stmt.get_children() == [条件, then分支, else分支]
    
    def test_如果语句_无else分支(self):
        """测试无else分支的如果语句"""
        条件 = 字面量表达式(Token(TokenType.布尔值, True, 1, 4))
        then分支 = 表达式语句(字面量表达式(Token(TokenType.整数, 1, 1, 1)))
        
        stmt = 如果语句(条件, then分支, None, 1, 1)
        
        assert stmt.条件 == 条件
        assert stmt.then分支 == then分支
        assert stmt.else分支 is None
        assert stmt.行号 == 1
        assert stmt.列号 == 1
        assert stmt.get_children() == [条件, then分支]
    
    def test_当语句(self):
        """测试当语句(while循环)"""
        条件 = 字面量表达式(Token(TokenType.布尔值, True, 1, 7))
        循环体 = 表达式语句(字面量表达式(Token(TokenType.整数, 1, 1, 1)))
        
        stmt = 当语句(条件, 循环体, 1, 1)
        
        assert stmt.条件 == 条件
        assert stmt.循环体 == 循环体
        assert stmt.行号 == 1
        assert stmt.列号 == 1
        assert stmt.get_children() == [条件, 循环体]
    
    def test_函数声明语句(self):
        """测试函数声明语句"""
        函数体 = 代码块语句([], 1, 1)
        stmt = 函数声明语句("add", ["a", "b"], 函数体, 1, 1)
        
        assert stmt.名称 == "add"
        assert stmt.参数列表 == ["a", "b"]
        assert stmt.函数体 == 函数体
        assert stmt.行号 == 1
        assert stmt.列号 == 1
        assert stmt.get_children() == [函数体]


class TestASTProgram:
    """程序AST节点测试"""
    
    def test_程序(self):
        """测试程序节点"""
        stmt1 = 表达式语句(字面量表达式(Token(TokenType.整数, 1, 1, 1)))
        stmt2 = 表达式语句(字面量表达式(Token(TokenType.整数, 2, 2, 1)))
        
        program = 程序([stmt1, stmt2])
        
        assert program.语句列表 == [stmt1, stmt2]
        assert program.行号 == 1
        assert program.列号 == 1
        assert program.get_children() == [stmt1, stmt2]


class TestASTNodeBase:
    """AST节点基类测试"""
    
    def test_position_tracking(self):
        """测试位置跟踪"""
        token = Token(TokenType.整数, 123, 5, 10)
        expr = 字面量表达式(token)
        
        assert expr.get_position() == (5, 10)
    
    def test_repr(self):
        """测试字符串表示"""
        token = Token(TokenType.整数, 123, 1, 1)
        expr = 字面量表达式(token)
        
        assert "字面量表达式" in str(expr)
        assert "123" in str(expr)


class 测试访问者(ASTVisitor):
    """测试用的访问者类"""
    
    def __init__(self):
        self.visited_nodes = []
    
    def visit_二元运算表达式(self, node: 二元运算表达式) -> str:
        self.visited_nodes.append(node)
        return f"({self.visit(node.左操作数)} {node.运算符.值} {self.visit(node.右操作数)})"
    
    def visit_一元运算表达式(self, node: 一元运算表达式) -> str:
        self.visited_nodes.append(node)
        return f"({node.运算符.值}{self.visit(node.操作数)})"
    
    def visit_字面量表达式(self, node: 字面量表达式) -> str:
        self.visited_nodes.append(node)
        return str(node.值)
    
    def visit_标识符表达式(self, node: 标识符表达式) -> str:
        self.visited_nodes.append(node)
        return node.名称
    
    def visit_函数调用表达式(self, node: 函数调用表达式) -> str:
        self.visited_nodes.append(node)
        参数 = [self.visit(arg) for arg in node.参数列表]
        return f"{self.visit(node.函数)}({', '.join(参数)})"
    
    def visit_赋值表达式(self, node: 赋值表达式) -> str:
        self.visited_nodes.append(node)
        return f"{self.visit(node.目标)} = {self.visit(node.值)}"
    
    def visit_表达式语句(self, node: 表达式语句) -> str:
        self.visited_nodes.append(node)
        return f"{self.visit(node.表达式)};"
    
    def visit_变量声明语句(self, node: 变量声明语句) -> str:
        self.visited_nodes.append(node)
        if node.初始值:
            return f"var {node.名称} = {self.visit(node.初始值)};"
        else:
            return f"var {node.名称};"
    
    def visit_函数声明语句(self, node: 函数声明语句) -> str:
        self.visited_nodes.append(node)
        参数 = ", ".join(node.参数列表)
        return f"func {node.名称}({参数}) {self.visit(node.函数体)}"
    
    def visit_返回语句(self, node: 返回语句) -> str:
        self.visited_nodes.append(node)
        if node.返回值:
            return f"return {self.visit(node.返回值)};"
        else:
            return "return;"
    
    def visit_如果语句(self, node: 如果语句) -> str:
        self.visited_nodes.append(node)
        result = f"if ({self.visit(node.条件)}) {self.visit(node.then分支)}"
        if node.else分支:
            result += f" else {self.visit(node.else分支)}"
        return result
    
    def visit_当语句(self, node: 当语句) -> str:
        self.visited_nodes.append(node)
        return f"while ({self.visit(node.条件)}) {self.visit(node.循环体)}"
    
    def visit_代码块语句(self, node: 代码块语句) -> str:
        self.visited_nodes.append(node)
        statements = [self.visit(stmt) for stmt in node.语句列表]
        return "{" + " ".join(statements) + "}"
    
    def visit_程序(self, node: 程序) -> str:
        self.visited_nodes.append(node)
        statements = [self.visit(stmt) for stmt in node.语句列表]
        return "\n".join(statements)


class TestASTVisitor:
    """访问者模式测试"""
    
    def test_visitor_pattern(self):
        """测试访问者模式"""
        # 创建AST: 1 + 2
        left = 字面量表达式(Token(TokenType.整数, 1, 1, 1))
        right = 字面量表达式(Token(TokenType.整数, 2, 1, 5))
        op = Token(TokenType.加, "+", 1, 3)
        expr = 二元运算表达式(left, op, right)
        
        visitor = 测试访问者()
        result = visitor.visit(expr)
        
        assert result == "(1 + 2)"
        assert len(visitor.visited_nodes) == 3  # 二元运算表达式 + 两个字面量
    
    def test_complex_expression_visitor(self):
        """测试复杂表达式的访问者"""
        # 创建AST: add(1, 2 * 3)
        func = 标识符表达式(Token(TokenType.标识符, "add", 1, 1))
        arg1 = 字面量表达式(Token(TokenType.整数, 1, 1, 5))
        
        # 2 * 3
        left = 字面量表达式(Token(TokenType.整数, 2, 1, 8))
        right = 字面量表达式(Token(TokenType.整数, 3, 1, 12))
        mul_op = Token(TokenType.乘, "*", 1, 10)
        arg2 = 二元运算表达式(left, mul_op, right)
        
        call = 函数调用表达式(func, [arg1, arg2], 1, 1)
        
        visitor = 测试访问者()
        result = visitor.visit(call)
        
        assert result == "add(1, (2 * 3))"
        assert len(visitor.visited_nodes) == 6  # 函数调用 + 标识符 + 字面量 + 二元运算 + 两个字面量