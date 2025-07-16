"""
Token类的单元测试
"""

import pytest
from src.lexer.token import Token, TokenType


class TestToken:
    """Token类测试"""
    
    def test_token_creation(self):
        """测试token创建"""
        token = Token(TokenType.整数, 123, 1, 1)
        
        assert token.类型 == TokenType.整数
        assert token.值 == 123
        assert token.行号 == 1
        assert token.列号 == 1
    
    def test_token_str_representation(self):
        """测试token字符串表示"""
        token = Token(TokenType.标识符, "变量名", 2, 5)
        expected = "Token(标识符, '变量名', 2:5)"
        
        assert str(token) == expected
        assert repr(token) == expected
    
    def test_is_type(self):
        """测试类型检查"""
        token = Token(TokenType.整数, 42)
        
        assert token.is_type(TokenType.整数) is True
        assert token.is_type(TokenType.字符串) is False
    
    def test_is_literal(self):
        """测试字面量检查"""
        # 测试各种字面量
        assert Token(TokenType.整数, 123).is_literal() is True
        assert Token(TokenType.浮点数, 3.14).is_literal() is True
        assert Token(TokenType.字符串, "hello").is_literal() is True
        assert Token(TokenType.布尔值, True).is_literal() is True
        
        # 测试非字面量
        assert Token(TokenType.标识符, "变量").is_literal() is False
        assert Token(TokenType.加, "+").is_literal() is False
    
    def test_is_operator(self):
        """测试运算符检查"""
        # 测试各种运算符
        assert Token(TokenType.加, "+").is_operator() is True
        assert Token(TokenType.减, "-").is_operator() is True
        assert Token(TokenType.等于, "==").is_operator() is True
        assert Token(TokenType.与, "&&").is_operator() is True
        
        # 测试非运算符
        assert Token(TokenType.整数, 123).is_operator() is False
        assert Token(TokenType.标识符, "变量").is_operator() is False
    
    def test_is_keyword(self):
        """测试关键字检查"""
        # 测试各种关键字
        assert Token(TokenType.函数, "func").is_keyword() is True
        assert Token(TokenType.如果, "if").is_keyword() is True
        assert Token(TokenType.返回, "return").is_keyword() is True
        
        # 测试非关键字
        assert Token(TokenType.标识符, "变量").is_keyword() is False
        assert Token(TokenType.整数, 123).is_keyword() is False


class TestTokenType:
    """TokenType枚举测试"""
    
    def test_token_type_values(self):
        """测试token类型值的存在性"""
        # 确保所有重要的token类型都存在
        assert hasattr(TokenType, '整数')
        assert hasattr(TokenType, '浮点数')
        assert hasattr(TokenType, '字符串')
        assert hasattr(TokenType, '标识符')
        assert hasattr(TokenType, '函数')
        assert hasattr(TokenType, '加')
        assert hasattr(TokenType, '等于')
        assert hasattr(TokenType, '左括号')
        assert hasattr(TokenType, '分号')
        assert hasattr(TokenType, '文件结束')
    
    def test_token_type_uniqueness(self):
        """测试token类型的唯一性"""
        # 获取所有token类型值
        values = [token_type.value for token_type in TokenType]
        
        # 确保没有重复值
        assert len(values) == len(set(values))