"""
词法分析器实现
将源代码文本转换为token流
"""

from typing import List, Optional, Iterator
from .token import Token, TokenType, KEYWORDS


class LexerError(Exception):
    """词法分析器异常"""
    
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"词法错误在 {line}:{column} - {message}")
        self.line = line
        self.column = column


class Lexer:
    """
    词法分析器类
    负责将源代码转换为token流
    """
    
    def __init__(self, source_code: str):
        """
        初始化词法分析器
        
        Args:
            source_code: 要分析的源代码字符串
        """
        self.source = source_code
        self.length = len(source_code)
        self.position = 0        # 当前字符位置
        self.line = 1           # 当前行号
        self.column = 1         # 当前列号
        self.current_char = self.source[0] if self.source else None
    
    def error(self, message: str) -> None:
        """抛出词法分析错误"""
        raise LexerError(message, self.line, self.column)
    
    def advance(self) -> None:
        """前进到下一个字符"""
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        self.position += 1
        if self.position >= self.length:
            self.current_char = None
        else:
            self.current_char = self.source[self.position]
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """
        向前查看字符，不改变当前位置
        
        Args:
            offset: 向前查看的偏移量
        
        Returns:
            查看到的字符，如果超出范围返回None
        """
        peek_pos = self.position + offset
        if peek_pos >= self.length:
            return None
        return self.source[peek_pos]
    
    def skip_whitespace(self) -> None:
        """跳过空白字符（除了换行符）"""
        while (self.current_char is not None and 
               self.current_char.isspace() and 
               self.current_char != '\n'):
            self.advance()
    
    def skip_line_comment(self) -> None:
        """跳过单行注释"""
        # 跳过 '//'
        self.advance()
        self.advance()
        
        # 读取到行尾
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
    
    def read_number(self) -> Token:
        """
        读取数字（整数或浮点数）
        
        Returns:
            数字token
        """
        start_line, start_column = self.line, self.column
        number_str = ''
        has_dot = False
        
        while (self.current_char is not None and 
               (self.current_char.isdigit() or self.current_char == '.')):
            
            if self.current_char == '.':
                if has_dot:
                    # 遇到第二个小数点，停止读取
                    break
                has_dot = True
            
            number_str += self.current_char
            self.advance()
        
        # 检查是否以小数点结尾
        if number_str.endswith('.'):
            # 回退一个字符，小数点不属于这个数字
            self.position -= 1
            self.column -= 1
            self.current_char = '.'
            number_str = number_str[:-1]
            has_dot = False
        
        # 转换为合适的数值类型
        if has_dot:
            value = float(number_str)
            token_type = TokenType.浮点数
        else:
            value = int(number_str)
            token_type = TokenType.整数
        
        return Token(token_type, value, start_line, start_column)
    
    def read_string(self) -> Token:
        """
        读取字符串字面量
        
        Returns:
            字符串token
        """
        start_line, start_column = self.line, self.column
        quote_char = self.current_char  # 记录引号类型
        self.advance()  # 跳过开始引号
        
        string_value = ''
        
        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\\':
                # 处理转义字符
                self.advance()
                if self.current_char is None:
                    self.error("字符串未闭合")
                
                escape_chars = {
                    'n': '\n',
                    't': '\t',
                    'r': '\r',
                    '\\': '\\',
                    '"': '"',
                    "'": "'",
                }
                
                if self.current_char in escape_chars:
                    string_value += escape_chars[self.current_char]
                else:
                    string_value += self.current_char
            else:
                string_value += self.current_char
            
            self.advance()
        
        if self.current_char != quote_char:
            self.error("字符串未闭合")
        
        self.advance()  # 跳过结束引号
        
        return Token(TokenType.字符串, string_value, start_line, start_column)
    
    def read_identifier(self) -> Token:
        """
        读取标识符或关键字
        
        Returns:
            标识符或关键字token
        """
        start_line, start_column = self.line, self.column
        identifier = ''
        
        while (self.current_char is not None and 
               (self.current_char.isalnum() or self.current_char == '_')):
            identifier += self.current_char
            self.advance()
        
        # 检查是否为关键字
        token_type = KEYWORDS.get(identifier, TokenType.标识符)
        
        # 处理布尔值
        if token_type == TokenType.真:
            return Token(TokenType.布尔值, True, start_line, start_column)
        elif token_type == TokenType.假:
            return Token(TokenType.布尔值, False, start_line, start_column)
        elif token_type == TokenType.空:
            return Token(TokenType.布尔值, None, start_line, start_column)
        
        return Token(token_type, identifier, start_line, start_column)
    
    def next_token(self) -> Token:
        """
        获取下一个token
        
        Returns:
            下一个token
        """
        while self.current_char is not None:
            start_line, start_column = self.line, self.column
            
            # 跳过空白字符（除了换行符）
            if self.current_char.isspace() and self.current_char != '\n':
                self.skip_whitespace()
                continue
            
            # 换行符
            if self.current_char == '\n':
                self.advance()
                return Token(TokenType.换行, '\n', start_line, start_column)
            
            # 数字
            if self.current_char.isdigit():
                return self.read_number()
            
            # 字符串
            if self.current_char in ('"', "'"):
                return self.read_string()
            
            # 标识符和关键字
            if self.current_char.isalpha() or self.current_char == '_':
                return self.read_identifier()
            
            # 注释处理
            if self.current_char == '/' and self.peek() == '/':
                self.skip_line_comment()
                continue
            
            # 双字符运算符
            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.等于, '==', start_line, start_column)
            
            if self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.不等于, '!=', start_line, start_column)
            
            if self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.小于等于, '<=', start_line, start_column)
            
            if self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.大于等于, '>=', start_line, start_column)
            
            if self.current_char == '&' and self.peek() == '&':
                self.advance()
                self.advance()
                return Token(TokenType.与, '&&', start_line, start_column)
            
            if self.current_char == '|' and self.peek() == '|':
                self.advance()
                self.advance()
                return Token(TokenType.或, '||', start_line, start_column)
            
            # 单字符token
            single_char_tokens = {
                '+': TokenType.加,
                '-': TokenType.减,
                '*': TokenType.乘,
                '/': TokenType.除,
                '%': TokenType.模,
                '=': TokenType.赋值,
                '<': TokenType.小于,
                '>': TokenType.大于,
                '!': TokenType.非,
                '(': TokenType.左括号,
                ')': TokenType.右括号,
                '{': TokenType.左大括号,
                '}': TokenType.右大括号,
                '[': TokenType.左方括号,
                ']': TokenType.右方括号,
                ';': TokenType.分号,
                ',': TokenType.逗号,
                '.': TokenType.点,
            }
            
            if self.current_char in single_char_tokens:
                char = self.current_char
                token_type = single_char_tokens[char]
                self.advance()
                return Token(token_type, char, start_line, start_column)
            
            # 未知字符
            char = self.current_char
            self.advance()
            return Token(TokenType.错误, char, start_line, start_column)
        
        # 文件结束
        return Token(TokenType.文件结束, None, self.line, self.column)
    
    def tokenize(self) -> List[Token]:
        """
        对整个源代码进行词法分析
        
        Returns:
            token列表
        """
        tokens = []
        
        while True:
            token = self.next_token()
            tokens.append(token)
            
            if token.类型 == TokenType.文件结束:
                break
        
        return tokens
    
    def __iter__(self) -> Iterator[Token]:
        """使词法分析器可迭代"""
        return self
    
    def __next__(self) -> Token:
        """迭代器的下一个方法"""
        token = self.next_token()
        if token.类型 == TokenType.文件结束:
            raise StopIteration
        return token