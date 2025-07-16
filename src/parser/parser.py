"""
语法分析器实现
使用递归下降法解析token流，构建AST
"""

from typing import List, Optional, Callable, Dict
from ..lexer.token import Token, TokenType
from ..lexer.lexer import Lexer
from ..ast import *
from .precedence import 运算符优先级, 结合性


class ParserError(Exception):
    """语法分析器异常"""
    
    def __init__(self, message: str, token: Token):
        super().__init__(f"语法错误在 {token.行号}:{token.列号} - {message}")
        self.token = token
        self.line = token.行号
        self.column = token.列号


class Parser:
    """
    语法分析器类
    使用递归下降法解析token流，构建AST
    """
    
    def __init__(self, tokens: List[Token]):
        """
        初始化语法分析器
        
        Args:
            tokens: 词法分析器产生的token列表
        """
        self.tokens = tokens
        self.current = 0  # 当前token索引
        self.length = len(tokens)
    
    def error(self, message: str) -> None:
        """抛出语法分析错误"""
        current_token = self.peek()
        raise ParserError(message, current_token)
    
    def peek(self, offset: int = 0) -> Token:
        """
        查看当前token或向前查看
        
        Args:
            offset: 向前查看的偏移量
            
        Returns:
            查看到的token
        """
        pos = self.current + offset
        if pos >= self.length:
            return self.tokens[-1]  # 返回EOF token
        return self.tokens[pos]
    
    def advance(self) -> Token:
        """
        消费当前token并前进到下一个
        
        Returns:
            被消费的token
        """
        if self.current < self.length:
            token = self.tokens[self.current]
            self.current += 1
            return token
        return self.tokens[-1]  # 返回EOF token
    
    def match(self, *token_types: TokenType) -> bool:
        """
        检查当前token是否匹配指定类型之一
        
        Args:
            token_types: 要匹配的token类型
            
        Returns:
            如果匹配返回True
        """
        current_token = self.peek()
        return current_token.类型 in token_types
    
    def consume(self, token_type: TokenType, message: str) -> Token:
        """
        消费指定类型的token
        
        Args:
            token_type: 期望的token类型
            message: 错误消息
            
        Returns:
            被消费的token
            
        Raises:
            ParserError: 如果token类型不匹配
        """
        if self.match(token_type):
            return self.advance()
        else:
            self.error(message)
            return self.peek()  # 这行不会执行，但满足类型检查
    
    def skip_newlines(self) -> None:
        """跳过换行符"""
        while self.match(TokenType.换行):
            self.advance()
    
    def at_end(self) -> bool:
        """检查是否到达token流末尾"""
        return self.peek().类型 == TokenType.文件结束
    
    def parse(self) -> 程序:
        """
        解析整个程序
        
        Returns:
            程序AST节点
        """
        statements = []
        
        self.skip_newlines()
        
        while not self.at_end():
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return 程序(statements)
    
    def parse_statement(self) -> Optional[语句]:
        """
        解析语句
        
        Returns:
            语句AST节点
        """
        try:
            if self.match(TokenType.函数):
                return self.parse_function_declaration()
            elif self.match(TokenType.如果):
                return self.parse_if_statement()
            elif self.match(TokenType.当):
                return self.parse_while_statement()
            elif self.match(TokenType.返回):
                return self.parse_return_statement()
            elif self.match(TokenType.左大括号):
                return self.parse_block_statement()
            else:
                return self.parse_expression_statement()
        except ParserError:
            # 错误恢复：跳到下一个语句
            self.synchronize()
            return None
    
    def parse_function_declaration(self) -> 函数声明语句:
        """
        解析函数声明
        func name(param1, param2) { body }
        
        Returns:
            函数声明语句AST节点
        """
        func_token = self.consume(TokenType.函数, "期望 'func'")
        
        name_token = self.consume(TokenType.标识符, "期望函数名")
        name = name_token.值
        
        self.consume(TokenType.左括号, "期望 '('")
        
        # 解析参数列表
        parameters = []
        if not self.match(TokenType.右括号):
            parameters.append(self.consume(TokenType.标识符, "期望参数名").值)
            
            while self.match(TokenType.逗号):
                self.advance()
                parameters.append(self.consume(TokenType.标识符, "期望参数名").值)
        
        self.consume(TokenType.右括号, "期望 ')'")
        
        # 解析函数体
        body = self.parse_block_statement()
        
        return 函数声明语句(name, parameters, body, func_token.行号, func_token.列号)
    
    def parse_if_statement(self) -> 如果语句:
        """
        解析if语句
        if (condition) statement [else statement]
        
        Returns:
            如果语句AST节点
        """
        if_token = self.consume(TokenType.如果, "期望 'if'")
        
        self.consume(TokenType.左括号, "期望 '('")
        condition = self.parse_expression()
        self.consume(TokenType.右括号, "期望 ')'")
        
        then_branch = self.parse_statement()
        if then_branch is None:
            self.error("期望语句")
        
        else_branch = None
        if self.match(TokenType.否则):
            self.advance()
            else_branch = self.parse_statement()
        
        return 如果语句(condition, then_branch, else_branch, if_token.行号, if_token.列号)
    
    def parse_while_statement(self) -> 当语句:
        """
        解析while语句
        while (condition) statement
        
        Returns:
            当语句AST节点
        """
        while_token = self.consume(TokenType.当, "期望 'while'")
        
        self.consume(TokenType.左括号, "期望 '('")
        condition = self.parse_expression()
        self.consume(TokenType.右括号, "期望 ')'")
        
        body = self.parse_statement()
        if body is None:
            self.error("期望语句")
        
        return 当语句(condition, body, while_token.行号, while_token.列号)
    
    def parse_return_statement(self) -> 返回语句:
        """
        解析return语句
        return [expression];
        
        Returns:
            返回语句AST节点
        """
        return_token = self.consume(TokenType.返回, "期望 'return'")
        
        value = None
        if not self.match(TokenType.分号, TokenType.换行, TokenType.文件结束):
            value = self.parse_expression()
        
        self.consume(TokenType.分号, "期望 ';'")
        
        return 返回语句(value, return_token.行号, return_token.列号)
    
    def parse_block_statement(self) -> 代码块语句:
        """
        解析代码块语句
        { statement1; statement2; ... }
        
        Returns:
            代码块语句AST节点
        """
        left_brace = self.consume(TokenType.左大括号, "期望 '{'")
        
        statements = []
        self.skip_newlines()
        
        while not self.match(TokenType.右大括号) and not self.at_end():
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        self.consume(TokenType.右大括号, "期望 '}'")
        
        return 代码块语句(statements, left_brace.行号, left_brace.列号)
    
    def parse_expression_statement(self) -> 表达式语句:
        """
        解析表达式语句
        expression;
        
        Returns:
            表达式语句AST节点
        """
        expr = self.parse_expression()
        self.consume(TokenType.分号, "期望 ';'")
        return 表达式语句(expr)
    
    def parse_expression(self) -> 表达式:
        """
        解析表达式
        
        Returns:
            表达式AST节点
        """
        return self.parse_assignment()
    
    def parse_assignment(self) -> 表达式:
        """
        解析赋值表达式
        
        Returns:
            表达式AST节点
        """
        expr = self.parse_logical_or()
        
        if self.match(TokenType.赋值):
            equals = self.advance()
            value = self.parse_assignment()
            return 赋值表达式(expr, value, equals.行号, equals.列号)
        
        return expr
    
    def parse_logical_or(self) -> 表达式:
        """解析逻辑或表达式"""
        return self.parse_binary_left(self.parse_logical_and, TokenType.或)
    
    def parse_logical_and(self) -> 表达式:
        """解析逻辑与表达式"""
        return self.parse_binary_left(self.parse_equality, TokenType.与)
    
    def parse_equality(self) -> 表达式:
        """解析相等性表达式"""
        return self.parse_binary_left(self.parse_comparison, TokenType.等于, TokenType.不等于)
    
    def parse_comparison(self) -> 表达式:
        """解析比较表达式"""
        return self.parse_binary_left(
            self.parse_addition,
            TokenType.大于, TokenType.大于等于, TokenType.小于, TokenType.小于等于
        )
    
    def parse_addition(self) -> 表达式:
        """解析加减表达式"""
        return self.parse_binary_left(self.parse_multiplication, TokenType.加, TokenType.减)
    
    def parse_multiplication(self) -> 表达式:
        """解析乘除模表达式"""
        return self.parse_binary_left(self.parse_unary, TokenType.乘, TokenType.除, TokenType.模)
    
    def parse_binary_left(self, next_precedence: Callable, *operators: TokenType) -> 表达式:
        """
        解析左结合的二元表达式
        
        Args:
            next_precedence: 下一个优先级的解析函数
            operators: 当前优先级的运算符
            
        Returns:
            表达式AST节点
        """
        expr = next_precedence()
        
        while self.match(*operators):
            operator = self.advance()
            right = next_precedence()
            expr = 二元运算表达式(expr, operator, right)
        
        return expr
    
    def parse_unary(self) -> 表达式:
        """
        解析一元表达式
        
        Returns:
            表达式AST节点
        """
        if self.match(TokenType.非, TokenType.减):
            operator = self.advance()
            right = self.parse_unary()
            return 一元运算表达式(operator, right)
        
        return self.parse_call()
    
    def parse_call(self) -> 表达式:
        """
        解析函数调用表达式
        
        Returns:
            表达式AST节点
        """
        expr = self.parse_primary()
        
        while True:
            if self.match(TokenType.左括号):
                expr = self.finish_call(expr)
            else:
                break
        
        return expr
    
    def finish_call(self, callee: 表达式) -> 表达式:
        """
        完成函数调用解析
        
        Args:
            callee: 被调用的表达式
            
        Returns:
            函数调用表达式AST节点
        """
        paren = self.consume(TokenType.左括号, "期望 '('")
        
        arguments = []
        if not self.match(TokenType.右括号):
            arguments.append(self.parse_expression())
            
            while self.match(TokenType.逗号):
                self.advance()
                arguments.append(self.parse_expression())
        
        self.consume(TokenType.右括号, "期望 ')'")
        
        return 函数调用表达式(callee, arguments, paren.行号, paren.列号)
    
    def parse_primary(self) -> 表达式:
        """
        解析基本表达式
        
        Returns:
            表达式AST节点
        """
        if self.match(TokenType.真, TokenType.假, TokenType.空):
            return 字面量表达式(self.advance())
        
        if self.match(TokenType.整数, TokenType.浮点数, TokenType.字符串, TokenType.布尔值):
            return 字面量表达式(self.advance())
        
        if self.match(TokenType.标识符):
            return 标识符表达式(self.advance())
        
        if self.match(TokenType.左括号):
            self.advance()
            expr = self.parse_expression()
            self.consume(TokenType.右括号, "期望 ')'")
            return expr
        
        self.error("期望表达式")
        return 字面量表达式(self.peek())  # 这行不会执行，但满足类型检查
    
    def synchronize(self) -> None:
        """
        错误恢复：跳到下一个语句的开始
        """
        self.advance()
        
        while not self.at_end():
            if self.tokens[self.current - 1].类型 == TokenType.分号:
                return
            
            if self.peek().类型 in {
                TokenType.函数, TokenType.如果, TokenType.当, TokenType.返回
            }:
                return
            
            self.advance()


def parse_source(source: str) -> 程序:
    """
    解析源代码字符串
    
    Args:
        source: 源代码字符串
        
    Returns:
        程序AST节点
    """
    from ..lexer import Lexer
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    return parser.parse()