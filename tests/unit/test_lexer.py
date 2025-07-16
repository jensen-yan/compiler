"""
词法分析器的单元测试
"""

import pytest
from src.lexer.lexer import Lexer, LexerError
from src.lexer.token import Token, TokenType


class TestLexer:
    """词法分析器测试"""
    
    def test_empty_source(self):
        """测试空源代码"""
        lexer = Lexer("")
        token = lexer.next_token()
        
        assert token.类型 == TokenType.文件结束
        assert token.值 is None
    
    def test_single_integer(self):
        """测试单个整数"""
        lexer = Lexer("123")
        token = lexer.next_token()
        
        assert token.类型 == TokenType.整数
        assert token.值 == 123
        assert token.行号 == 1
        assert token.列号 == 1
    
    def test_single_float(self):
        """测试单个浮点数"""
        lexer = Lexer("3.14")
        token = lexer.next_token()
        
        assert token.类型 == TokenType.浮点数
        assert token.值 == 3.14
        assert token.行号 == 1
        assert token.列号 == 1
    
    def test_single_string_double_quotes(self):
        """测试双引号字符串"""
        lexer = Lexer('"hello world"')
        token = lexer.next_token()
        
        assert token.类型 == TokenType.字符串
        assert token.值 == "hello world"
    
    def test_single_string_single_quotes(self):
        """测试单引号字符串"""
        lexer = Lexer("'hello world'")
        token = lexer.next_token()
        
        assert token.类型 == TokenType.字符串
        assert token.值 == "hello world"
    
    def test_string_with_escapes(self):
        """测试带转义字符的字符串"""
        lexer = Lexer('"hello\\nworld\\t!"')
        token = lexer.next_token()
        
        assert token.类型 == TokenType.字符串
        assert token.值 == "hello\nworld\t!"
    
    def test_identifier(self):
        """测试标识符"""
        lexer = Lexer("变量名")
        token = lexer.next_token()
        
        assert token.类型 == TokenType.标识符
        assert token.值 == "变量名"
    
    def test_keywords(self):
        """测试关键字识别"""
        keywords_test = [
            ("func", TokenType.函数),
            ("return", TokenType.返回),
            ("if", TokenType.如果),
            ("else", TokenType.否则),
            ("while", TokenType.当),
            ("for", TokenType.对于),
        ]
        
        for keyword, expected_type in keywords_test:
            lexer = Lexer(keyword)
            token = lexer.next_token()
            
            assert token.类型 == expected_type
            assert token.值 == keyword
    
    def test_boolean_literals(self):
        """测试布尔值字面量"""
        # 测试true
        lexer = Lexer("true")
        token = lexer.next_token()
        assert token.类型 == TokenType.布尔值
        assert token.值 is True
        
        # 测试false
        lexer = Lexer("false")
        token = lexer.next_token()
        assert token.类型 == TokenType.布尔值
        assert token.值 is False
        
        # 测试null
        lexer = Lexer("null")
        token = lexer.next_token()
        assert token.类型 == TokenType.布尔值
        assert token.值 is None
    
    def test_single_char_operators(self):
        """测试单字符运算符"""
        operators_test = [
            ("+", TokenType.加),
            ("-", TokenType.减),
            ("*", TokenType.乘),
            ("/", TokenType.除),
            ("%", TokenType.模),
            ("=", TokenType.赋值),
            ("<", TokenType.小于),
            (">", TokenType.大于),
            ("!", TokenType.非),
        ]
        
        for op, expected_type in operators_test:
            lexer = Lexer(op)
            token = lexer.next_token()
            
            assert token.类型 == expected_type
            assert token.值 == op
    
    def test_double_char_operators(self):
        """测试双字符运算符"""
        operators_test = [
            ("==", TokenType.等于),
            ("!=", TokenType.不等于),
            ("<=", TokenType.小于等于),
            (">=", TokenType.大于等于),
            ("&&", TokenType.与),
            ("||", TokenType.或),
        ]
        
        for op, expected_type in operators_test:
            lexer = Lexer(op)
            token = lexer.next_token()
            
            assert token.类型 == expected_type
            assert token.值 == op
    
    def test_punctuation(self):
        """测试标点符号"""
        punctuation_test = [
            ("(", TokenType.左括号),
            (")", TokenType.右括号),
            ("{", TokenType.左大括号),
            ("}", TokenType.右大括号),
            ("[", TokenType.左方括号),
            ("]", TokenType.右方括号),
            (";", TokenType.分号),
            (",", TokenType.逗号),
            (".", TokenType.点),
        ]
        
        for punct, expected_type in punctuation_test:
            lexer = Lexer(punct)
            token = lexer.next_token()
            
            assert token.类型 == expected_type
            assert token.值 == punct
    
    def test_newline(self):
        """测试换行符"""
        lexer = Lexer("\n")
        token = lexer.next_token()
        
        assert token.类型 == TokenType.换行
        assert token.值 == "\n"
    
    def test_whitespace_skipping(self):
        """测试空白字符跳过"""
        lexer = Lexer("   123   ")
        token = lexer.next_token()
        
        assert token.类型 == TokenType.整数
        assert token.值 == 123
    
    def test_line_and_column_tracking(self):
        """测试行号和列号跟踪"""
        source = "123\n456"
        lexer = Lexer(source)
        
        # 第一个token
        token1 = lexer.next_token()
        assert token1.类型 == TokenType.整数
        assert token1.值 == 123
        assert token1.行号 == 1
        assert token1.列号 == 1
        
        # 换行token
        token2 = lexer.next_token()
        assert token2.类型 == TokenType.换行
        assert token2.行号 == 1
        assert token2.列号 == 4
        
        # 第二个token
        token3 = lexer.next_token()
        assert token3.类型 == TokenType.整数
        assert token3.值 == 456
        assert token3.行号 == 2
        assert token3.列号 == 1
    
    def test_tokenize_simple_expression(self):
        """测试简单表达式的完整词法分析"""
        source = "x = 123 + 456"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        expected = [
            (TokenType.标识符, "x"),
            (TokenType.赋值, "="),
            (TokenType.整数, 123),
            (TokenType.加, "+"),
            (TokenType.整数, 456),
            (TokenType.文件结束, None),
        ]
        
        assert len(tokens) == len(expected)
        for i, (expected_type, expected_value) in enumerate(expected):
            assert tokens[i].类型 == expected_type
            assert tokens[i].值 == expected_value
    
    def test_iterator_interface(self):
        """测试迭代器接口"""
        source = "1 + 2"
        lexer = Lexer(source)
        
        tokens = list(lexer)
        
        assert len(tokens) == 3
        assert tokens[0].类型 == TokenType.整数
        assert tokens[1].类型 == TokenType.加
        assert tokens[2].类型 == TokenType.整数
    
    def test_unclosed_string_error(self):
        """测试未闭合字符串错误"""
        lexer = Lexer('"未闭合的字符串')
        
        with pytest.raises(LexerError) as exc_info:
            lexer.next_token()
        
        assert "字符串未闭合" in str(exc_info.value)
    
    def test_invalid_character_error(self):
        """测试无效字符"""
        lexer = Lexer("@")  # @ 不是有效的token
        token = lexer.next_token()
        
        assert token.类型 == TokenType.错误
        assert token.值 == "@"
    
    def test_number_followed_by_dot(self):
        """测试数字后跟点号（属性访问）"""
        lexer = Lexer("123.toString")
        tokens = lexer.tokenize()
        
        # 应该识别为: 123, ., toString, EOF
        assert len(tokens) == 4
        assert tokens[0].类型 == TokenType.整数
        assert tokens[0].值 == 123
        assert tokens[1].类型 == TokenType.点
        assert tokens[1].值 == "."
        assert tokens[2].类型 == TokenType.标识符
        assert tokens[2].值 == "toString"