"""
语法分析器的单元测试
"""

import pytest
from src.parser.parser import Parser, ParserError, parse_source
from src.parser.precedence import 运算符优先级, 结合性
from src.lexer.lexer import Lexer
from src.lexer.token import TokenType
from src.ast import *


class TestParserPrecedence:
    """运算符优先级测试"""
    
    def test_运算符优先级(self):
        """测试运算符优先级"""
        assert 运算符优先级.get_优先级(TokenType.乘) > 运算符优先级.get_优先级(TokenType.加)
        assert 运算符优先级.get_优先级(TokenType.加) > 运算符优先级.get_优先级(TokenType.大于)
        assert 运算符优先级.get_优先级(TokenType.大于) > 运算符优先级.get_优先级(TokenType.与)
        assert 运算符优先级.get_优先级(TokenType.与) > 运算符优先级.get_优先级(TokenType.或)
        assert 运算符优先级.get_优先级(TokenType.或) > 运算符优先级.get_优先级(TokenType.赋值)
    
    def test_结合性(self):
        """测试运算符结合性"""
        assert 运算符优先级.get_结合性(TokenType.加) == 结合性.左结合
        assert 运算符优先级.get_结合性(TokenType.赋值) == 结合性.右结合
        assert 运算符优先级.get_结合性(TokenType.非) == 结合性.右结合
    
    def test_运算符检查(self):
        """测试运算符类型检查"""
        assert 运算符优先级.is_二元运算符(TokenType.加) is True
        assert 运算符优先级.is_二元运算符(TokenType.标识符) is False
        
        assert 运算符优先级.is_一元运算符(TokenType.非) is True
        assert 运算符优先级.is_一元运算符(TokenType.减) is True
        assert 运算符优先级.is_一元运算符(TokenType.加) is False


class TestParserBasic:
    """基础语法分析器测试"""
    
    def test_parse_整数字面量(self):
        """测试整数字面量解析"""
        source = "123;"
        program = parse_source(source)
        
        assert len(program.语句列表) == 1
        stmt = program.语句列表[0]
        assert isinstance(stmt, 表达式语句)
        assert isinstance(stmt.表达式, 字面量表达式)
        assert stmt.表达式.值 == 123
    
    def test_parse_字符串字面量(self):
        """测试字符串字面量解析"""
        source = '"hello world";'
        program = parse_source(source)
        
        assert len(program.语句列表) == 1
        stmt = program.语句列表[0]
        assert isinstance(stmt, 表达式语句)
        assert isinstance(stmt.表达式, 字面量表达式)
        assert stmt.表达式.值 == "hello world"
    
    def test_parse_布尔字面量(self):
        """测试布尔字面量解析"""
        source = "true; false;"
        program = parse_source(source)
        
        assert len(program.语句列表) == 2
        
        # true
        stmt1 = program.语句列表[0]
        assert isinstance(stmt1, 表达式语句)
        assert isinstance(stmt1.表达式, 字面量表达式)
        assert stmt1.表达式.值 is True
        
        # false
        stmt2 = program.语句列表[1]
        assert isinstance(stmt2, 表达式语句)
        assert isinstance(stmt2.表达式, 字面量表达式)
        assert stmt2.表达式.值 is False
    
    def test_parse_标识符(self):
        """测试标识符解析"""
        source = "variable_name;"
        program = parse_source(source)
        
        assert len(program.语句列表) == 1
        stmt = program.语句列表[0]
        assert isinstance(stmt, 表达式语句)
        assert isinstance(stmt.表达式, 标识符表达式)
        assert stmt.表达式.名称 == "variable_name"
    
    def test_parse_二元运算表达式(self):
        """测试二元运算表达式解析"""
        source = "1 + 2;"
        program = parse_source(source)
        
        assert len(program.语句列表) == 1
        stmt = program.语句列表[0]
        assert isinstance(stmt, 表达式语句)
        assert isinstance(stmt.表达式, 二元运算表达式)
        
        expr = stmt.表达式
        assert isinstance(expr.左操作数, 字面量表达式)
        assert expr.左操作数.值 == 1
        assert expr.运算符.类型 == TokenType.加
        assert isinstance(expr.右操作数, 字面量表达式)
        assert expr.右操作数.值 == 2
    
    def test_parse_一元运算表达式(self):
        """测试一元运算表达式解析"""
        source = "-42;"
        program = parse_source(source)
        
        assert len(program.语句列表) == 1
        stmt = program.语句列表[0]
        assert isinstance(stmt, 表达式语句)
        assert isinstance(stmt.表达式, 一元运算表达式)
        
        expr = stmt.表达式
        assert expr.运算符.类型 == TokenType.减
        assert isinstance(expr.操作数, 字面量表达式)
        assert expr.操作数.值 == 42
    
    def test_parse_函数调用(self):
        """测试函数调用解析"""
        source = "add(1, 2);"
        program = parse_source(source)
        
        assert len(program.语句列表) == 1
        stmt = program.语句列表[0]
        assert isinstance(stmt, 表达式语句)
        assert isinstance(stmt.表达式, 函数调用表达式)
        
        call = stmt.表达式
        assert isinstance(call.函数, 标识符表达式)
        assert call.函数.名称 == "add"
        assert len(call.参数列表) == 2
        assert isinstance(call.参数列表[0], 字面量表达式)
        assert call.参数列表[0].值 == 1
        assert isinstance(call.参数列表[1], 字面量表达式)
        assert call.参数列表[1].值 == 2
    
    def test_parse_赋值表达式(self):
        """测试赋值表达式解析"""
        source = "x = 42;"
        program = parse_source(source)
        
        assert len(program.语句列表) == 1
        stmt = program.语句列表[0]
        assert isinstance(stmt, 表达式语句)
        assert isinstance(stmt.表达式, 赋值表达式)
        
        assign = stmt.表达式
        assert isinstance(assign.目标, 标识符表达式)
        assert assign.目标.名称 == "x"
        assert isinstance(assign.值, 字面量表达式)
        assert assign.值.值 == 42


class TestParserOperatorPrecedence:
    """运算符优先级解析测试"""
    
    def test_加法乘法优先级(self):
        """测试加法和乘法的优先级：1 + 2 * 3 应该解析为 1 + (2 * 3)"""
        source = "1 + 2 * 3;"
        program = parse_source(source)
        
        stmt = program.语句列表[0]
        expr = stmt.表达式
        
        # 应该是 1 + (2 * 3) 的结构
        assert isinstance(expr, 二元运算表达式)
        assert expr.运算符.类型 == TokenType.加
        assert isinstance(expr.左操作数, 字面量表达式)
        assert expr.左操作数.值 == 1
        assert isinstance(expr.右操作数, 二元运算表达式)
        assert expr.右操作数.运算符.类型 == TokenType.乘
    
    def test_括号优先级(self):
        """测试括号改变优先级：(1 + 2) * 3"""
        source = "(1 + 2) * 3;"
        program = parse_source(source)
        
        stmt = program.语句列表[0]
        expr = stmt.表达式
        
        # 应该是 (1 + 2) * 3 的结构
        assert isinstance(expr, 二元运算表达式)
        assert expr.运算符.类型 == TokenType.乘
        assert isinstance(expr.左操作数, 二元运算表达式)
        assert expr.左操作数.运算符.类型 == TokenType.加
        assert isinstance(expr.右操作数, 字面量表达式)
        assert expr.右操作数.值 == 3
    
    def test_赋值右结合(self):
        """测试赋值运算符的右结合性：a = b = c"""
        source = "a = b = 42;"
        program = parse_source(source)
        
        stmt = program.语句列表[0]
        expr = stmt.表达式
        
        # 应该是 a = (b = 42) 的结构
        assert isinstance(expr, 赋值表达式)
        assert expr.目标.名称 == "a"
        assert isinstance(expr.值, 赋值表达式)
        assert expr.值.目标.名称 == "b"
        assert expr.值.值.值 == 42
    
    def test_比较运算符优先级(self):
        """测试比较运算符优先级：a + b > c * d"""
        source = "a + b > c * d;"
        program = parse_source(source)
        
        stmt = program.语句列表[0]
        expr = stmt.表达式
        
        # 应该是 (a + b) > (c * d) 的结构
        assert isinstance(expr, 二元运算表达式)
        assert expr.运算符.类型 == TokenType.大于
        assert isinstance(expr.左操作数, 二元运算表达式)
        assert expr.左操作数.运算符.类型 == TokenType.加
        assert isinstance(expr.右操作数, 二元运算表达式)
        assert expr.右操作数.运算符.类型 == TokenType.乘


class TestParserStatements:
    """语句解析测试"""
    
    def test_parse_代码块(self):
        """测试代码块解析"""
        source = """
        {
            x = 1;
            y = 2;
        }
        """
        program = parse_source(source)
        
        assert len(program.语句列表) == 1
        stmt = program.语句列表[0]
        assert isinstance(stmt, 代码块语句)
        assert len(stmt.语句列表) == 2
        
        # 检查第一个语句
        assert isinstance(stmt.语句列表[0], 表达式语句)
        assert isinstance(stmt.语句列表[0].表达式, 赋值表达式)
        
        # 检查第二个语句
        assert isinstance(stmt.语句列表[1], 表达式语句)
        assert isinstance(stmt.语句列表[1].表达式, 赋值表达式)
    
    def test_parse_if语句(self):
        """测试if语句解析"""
        source = """
        if (x > 0) {
            return 1;
        }
        """
        program = parse_source(source)
        
        assert len(program.语句列表) == 1
        stmt = program.语句列表[0]
        assert isinstance(stmt, 如果语句)
        
        # 检查条件
        assert isinstance(stmt.条件, 二元运算表达式)
        assert stmt.条件.运算符.类型 == TokenType.大于
        
        # 检查then分支
        assert isinstance(stmt.then分支, 代码块语句)
        
        # 检查没有else分支
        assert stmt.else分支 is None
    
    def test_parse_if_else语句(self):
        """测试if-else语句解析"""
        source = """
        if (x > 0) {
            return 1;
        } else {
            return -1;
        }
        """
        program = parse_source(source)
        
        assert len(program.语句列表) == 1
        stmt = program.语句列表[0]
        assert isinstance(stmt, 如果语句)
        
        # 检查条件
        assert isinstance(stmt.条件, 二元运算表达式)
        
        # 检查then分支
        assert isinstance(stmt.then分支, 代码块语句)
        
        # 检查else分支
        assert stmt.else分支 is not None
        assert isinstance(stmt.else分支, 代码块语句)
    
    def test_parse_while语句(self):
        """测试while语句解析"""
        source = """
        while (x < 10) {
            x = x + 1;
        }
        """
        program = parse_source(source)
        
        assert len(program.语句列表) == 1
        stmt = program.语句列表[0]
        assert isinstance(stmt, 当语句)
        
        # 检查条件
        assert isinstance(stmt.条件, 二元运算表达式)
        assert stmt.条件.运算符.类型 == TokenType.小于
        
        # 检查循环体
        assert isinstance(stmt.循环体, 代码块语句)
    
    def test_parse_return语句(self):
        """测试return语句解析"""
        # 带返回值的return
        source1 = "return 42;"
        program1 = parse_source(source1)
        
        stmt1 = program1.语句列表[0]
        assert isinstance(stmt1, 返回语句)
        assert stmt1.返回值 is not None
        assert isinstance(stmt1.返回值, 字面量表达式)
        assert stmt1.返回值.值 == 42
        
        # 不带返回值的return
        source2 = "return;"
        program2 = parse_source(source2)
        
        stmt2 = program2.语句列表[0]
        assert isinstance(stmt2, 返回语句)
        assert stmt2.返回值 is None
    
    def test_parse_函数声明(self):
        """测试函数声明解析"""
        source = """
        func add(a, b) {
            return a + b;
        }
        """
        program = parse_source(source)
        
        assert len(program.语句列表) == 1
        stmt = program.语句列表[0]
        assert isinstance(stmt, 函数声明语句)
        
        # 检查函数名
        assert stmt.名称 == "add"
        
        # 检查参数列表
        assert stmt.参数列表 == ["a", "b"]
        
        # 检查函数体
        assert isinstance(stmt.函数体, 代码块语句)
        assert len(stmt.函数体.语句列表) == 1
        assert isinstance(stmt.函数体.语句列表[0], 返回语句)


class TestParserComplex:
    """复杂表达式和语句解析测试"""
    
    def test_parse_复杂表达式(self):
        """测试复杂表达式解析"""
        source = "result = add(x * 2, y + 3) > 10 && flag;"
        program = parse_source(source)
        
        stmt = program.语句列表[0]
        assert isinstance(stmt, 表达式语句)
        assert isinstance(stmt.表达式, 赋值表达式)
        
        # 检查赋值的右侧是逻辑与表达式
        right_side = stmt.表达式.值
        assert isinstance(right_side, 二元运算表达式)
        assert right_side.运算符.类型 == TokenType.与
    
    def test_parse_嵌套函数调用(self):
        """测试嵌套函数调用"""
        source = "result = outer(inner(x, y), z);"
        program = parse_source(source)
        
        stmt = program.语句列表[0]
        assign = stmt.表达式
        call = assign.值
        
        assert isinstance(call, 函数调用表达式)
        assert call.函数.名称 == "outer"
        assert len(call.参数列表) == 2
        
        # 第一个参数是函数调用
        assert isinstance(call.参数列表[0], 函数调用表达式)
        assert call.参数列表[0].函数.名称 == "inner"
        
        # 第二个参数是标识符
        assert isinstance(call.参数列表[1], 标识符表达式)
        assert call.参数列表[1].名称 == "z"
    
    def test_parse_完整程序(self):
        """测试完整程序解析"""
        source = """
        func fibonacci(n) {
            if (n <= 1) {
                return n;
            } else {
                return fibonacci(n - 1) + fibonacci(n - 2);
            }
        }
        
        result = fibonacci(10);
        """
        program = parse_source(source)
        
        assert len(program.语句列表) == 2
        
        # 第一个语句是函数声明
        func_decl = program.语句列表[0]
        assert isinstance(func_decl, 函数声明语句)
        assert func_decl.名称 == "fibonacci"
        assert func_decl.参数列表 == ["n"]
        
        # 第二个语句是赋值
        assign_stmt = program.语句列表[1]
        assert isinstance(assign_stmt, 表达式语句)
        assert isinstance(assign_stmt.表达式, 赋值表达式)


class TestParserErrors:
    """语法错误处理测试"""
    
    def test_缺少分号错误(self):
        """测试缺少分号的错误"""
        source = "x = 42"  # 缺少分号
        
        with pytest.raises(ParserError) as exc_info:
            parse_source(source)
        
        assert "期望 ';'" in str(exc_info.value)
    
    def test_缺少括号错误(self):
        """测试缺少括号的错误"""
        source = "func add(a, b {"  # 缺少右括号
        
        with pytest.raises(ParserError) as exc_info:
            parse_source(source)
        
        assert "期望 ')'" in str(exc_info.value)
    
    def test_无效表达式错误(self):
        """测试无效表达式错误"""
        source = "x = ;"  # 无效表达式
        
        with pytest.raises(ParserError) as exc_info:
            parse_source(source)
        
        assert "期望表达式" in str(exc_info.value)
    
    def test_未闭合大括号错误(self):
        """测试未闭合大括号错误"""
        source = "{ x = 42;"  # 缺少右大括号
        
        with pytest.raises(ParserError) as exc_info:
            parse_source(source)
        
        assert "期望 '}'" in str(exc_info.value)