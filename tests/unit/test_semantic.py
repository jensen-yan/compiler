"""
语义分析器的单元测试
"""

import pytest
from src.semantic.analyzer import 语义分析器, 语义错误
from src.semantic.types import 类型系统, 基本类型, 函数类型, 基本类型枚举
from src.semantic.symbols import 符号表, 变量符号, 函数符号, 作用域管理器
from src.parser.parser import parse_source


class TestTypeSystem:
    """类型系统测试"""
    
    def test_basic_types(self):
        """测试基本类型"""
        type_system = 类型系统()
        
        assert str(type_system.整数类型) == "整数"
        assert str(type_system.浮点数类型) == "浮点数"
        assert str(type_system.字符串类型) == "字符串"
        assert str(type_system.布尔值类型) == "布尔值"
        assert str(type_system.空值类型) == "空值"
    
    def test_type_compatibility(self):
        """测试类型兼容性"""
        type_system = 类型系统()
        
        # 相同类型兼容
        assert type_system.整数类型.is_compatible_with(type_system.整数类型)
        
        # 数值类型兼容
        assert type_system.整数类型.is_compatible_with(type_system.浮点数类型)
        assert type_system.浮点数类型.is_compatible_with(type_system.整数类型)
        
        # 不兼容类型
        assert not type_system.整数类型.is_compatible_with(type_system.字符串类型)
    
    def test_type_assignment(self):
        """测试类型赋值"""
        type_system = 类型系统()
        
        # 相同类型可以赋值
        assert type_system.整数类型.is_assignable_from(type_system.整数类型)
        
        # 整数可以赋值给浮点数
        assert type_system.浮点数类型.is_assignable_from(type_system.整数类型)
        
        # 浮点数不能赋值给整数
        assert not type_system.整数类型.is_assignable_from(type_system.浮点数类型)
    
    def test_binary_operations(self):
        """测试二元运算类型检查"""
        type_system = 类型系统()
        from src.lexer.token import TokenType
        
        # 整数 + 整数 = 整数
        result = type_system.check_binary_operation(
            type_system.整数类型, TokenType.加, type_system.整数类型
        )
        assert result == type_system.整数类型
        
        # 整数 + 浮点数 = 浮点数
        result = type_system.check_binary_operation(
            type_system.整数类型, TokenType.加, type_system.浮点数类型
        )
        assert result == type_system.浮点数类型
        
        # 整数 > 整数 = 布尔值
        result = type_system.check_binary_operation(
            type_system.整数类型, TokenType.大于, type_system.整数类型
        )
        assert result == type_system.布尔值类型
        
        # 字符串 + 布尔值 = None（不支持）
        result = type_system.check_binary_operation(
            type_system.字符串类型, TokenType.加, type_system.布尔值类型
        )
        assert result is None
    
    def test_unary_operations(self):
        """测试一元运算类型检查"""
        type_system = 类型系统()
        from src.lexer.token import TokenType
        
        # -整数 = 整数
        result = type_system.check_unary_operation(TokenType.减, type_system.整数类型)
        assert result == type_system.整数类型
        
        # !布尔值 = 布尔值
        result = type_system.check_unary_operation(TokenType.非, type_system.布尔值类型)
        assert result == type_system.布尔值类型
        
        # -字符串 = None（不支持）
        result = type_system.check_unary_operation(TokenType.减, type_system.字符串类型)
        assert result is None
    
    def test_function_types(self):
        """测试函数类型"""
        type_system = 类型系统()
        
        # 创建函数类型：(整数, 浮点数) -> 字符串
        func_type = 函数类型(
            [type_system.整数类型, type_system.浮点数类型],
            type_system.字符串类型
        )
        
        assert str(func_type) == "函数(整数, 浮点数) -> 字符串"
        
        # 测试函数调用类型检查
        result = type_system.check_function_call(
            func_type, 
            [type_system.整数类型, type_system.浮点数类型]
        )
        assert result == type_system.字符串类型
        
        # 参数数量不匹配
        result = type_system.check_function_call(
            func_type, 
            [type_system.整数类型]
        )
        assert result is None
        
        # 参数类型不匹配
        result = type_system.check_function_call(
            func_type, 
            [type_system.字符串类型, type_system.浮点数类型]
        )
        assert result is None


class TestSymbolTable:
    """符号表测试"""
    
    def test_symbol_table_basic(self):
        """测试符号表基本功能"""
        type_system = 类型系统()
        symbol_table = 符号表("测试作用域")
        
        # 定义变量符号
        var_symbol = 变量符号("x", type_system.整数类型, 1, 1)
        assert symbol_table.define(var_symbol) is True
        
        # 查找符号
        found_symbol = symbol_table.lookup("x")
        assert found_symbol is not None
        assert found_symbol.名称 == "x"
        assert found_symbol.类型 == type_system.整数类型
        
        # 重复定义
        var_symbol2 = 变量符号("x", type_system.字符串类型, 2, 1)
        assert symbol_table.define(var_symbol2) is False
        
        # 查找不存在的符号
        assert symbol_table.lookup("y") is None
    
    def test_scope_manager(self):
        """测试作用域管理器"""
        type_system = 类型系统()
        scope_manager = 作用域管理器()
        
        # 进入全局作用域
        scope_manager.enter_scope("全局")
        assert scope_manager.get_scope_depth() == 1
        assert scope_manager.is_global_scope() is True
        
        # 定义全局变量
        global_var = 变量符号("global_var", type_system.整数类型, 1, 1)
        assert scope_manager.define_symbol(global_var) is True
        
        # 进入局部作用域
        scope_manager.enter_scope("局部")
        assert scope_manager.get_scope_depth() == 2
        assert scope_manager.is_global_scope() is False
        
        # 定义局部变量
        local_var = 变量符号("local_var", type_system.字符串类型, 2, 1)
        assert scope_manager.define_symbol(local_var) is True
        
        # 查找变量（应该能找到全局和局部变量）
        assert scope_manager.lookup_symbol("global_var") is not None
        assert scope_manager.lookup_symbol("local_var") is not None
        
        # 仅在当前作用域查找
        assert scope_manager.lookup_symbol_current_scope("global_var") is None
        assert scope_manager.lookup_symbol_current_scope("local_var") is not None
        
        # 退出局部作用域
        scope_manager.exit_scope()
        assert scope_manager.get_scope_depth() == 1
        
        # 局部变量应该不可见
        assert scope_manager.lookup_symbol("local_var") is None
        assert scope_manager.lookup_symbol("global_var") is not None


class TestSemanticAnalyzer:
    """语义分析器测试"""
    
    def test_simple_expression(self):
        """测试简单表达式"""
        source = "x = 123;"
        ast = parse_source(source)
        
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        assert len(errors) == 0
        
        # 检查变量是否被定义
        symbol = analyzer.作用域管理器.lookup_symbol("x")
        assert symbol is not None
        assert symbol.名称 == "x"
        assert str(symbol.类型) == "整数"
    
    def test_type_mismatch_error(self):
        """测试类型不匹配错误"""
        source = """
        x = 123;
        y = "hello";
        x = y;
        """
        ast = parse_source(source)
        
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        assert len(errors) == 1
        assert "类型不兼容" in errors[0].message
    
    def test_undefined_variable_error(self):
        """测试未定义变量错误"""
        source = "x = y;"
        ast = parse_source(source)
        
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        assert len(errors) == 1
        assert "未定义的标识符" in errors[0].message
    
    def test_function_declaration(self):
        """测试函数声明"""
        source = """
        func add(a, b) {
            return a + b;
        }
        """
        ast = parse_source(source)
        
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        assert len(errors) == 0
        
        # 检查函数是否被定义
        symbol = analyzer.作用域管理器.lookup_symbol("add")
        assert symbol is not None
        assert symbol.名称 == "add"
        assert isinstance(symbol, 函数符号)
        assert symbol.参数列表 == ["a", "b"]
    
    def test_function_call(self):
        """测试函数调用"""
        source = """
        func add(a, b) {
            return a + b;
        }
        result = add(1, 2);
        """
        ast = parse_source(source)
        
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        assert len(errors) == 0
    
    def test_function_call_error(self):
        """测试函数调用错误"""
        source = """
        func add(a, b) {
            return a + b;
        }
        result = add(1);  // 参数数量不匹配
        """
        ast = parse_source(source)
        
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        assert len(errors) == 1
        assert "参数不匹配" in errors[0].message
    
    def test_if_statement(self):
        """测试if语句"""
        source = """
        x = 10;
        if (x > 5) {
            y = 1;
        } else {
            y = 2;
        }
        """
        ast = parse_source(source)
        
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        assert len(errors) == 0
    
    def test_if_condition_error(self):
        """测试if条件错误"""
        source = """
        x = 10;
        if (x) {  // 条件不是布尔类型
            y = 1;
        }
        """
        ast = parse_source(source)
        
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        assert len(errors) == 1
        assert "条件必须是布尔类型" in errors[0].message
    
    def test_while_statement(self):
        """测试while语句"""
        source = """
        x = 0;
        while (x < 10) {
            x = x + 1;
        }
        """
        ast = parse_source(source)
        
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        assert len(errors) == 0
    
    def test_builtin_functions(self):
        """测试内置函数"""
        source = """
        print("Hello World");
        x = len("test");
        """
        ast = parse_source(source)
        
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        assert len(errors) == 0
    
    def test_variable_initialization(self):
        """测试变量初始化"""
        source = """
        x = y;  // y未定义
        z = 10;
        w = z;  // z已定义
        """
        ast = parse_source(source)
        
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        assert len(errors) == 1
        assert "未定义的标识符" in errors[0].message
    
    def test_scope_visibility(self):
        """测试作用域可见性"""
        source = """
        x = 10;
        {
            y = 20;
            z = x + y;  // x在外层作用域，y在当前作用域
        }
        w = y;  // y在内层作用域，此处不可见
        """
        ast = parse_source(source)
        
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        assert len(errors) == 1
        assert "未定义的标识符" in errors[0].message
    
    def test_complex_program(self):
        """测试复杂程序"""
        source = """
        func factorial(n) {
            if (n <= 1) {
                return 1;
            } else {
                return n * factorial(n - 1);
            }
        }
        
        result = factorial(5);
        print(str(result));
        """
        ast = parse_source(source)
        
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        assert len(errors) == 0
    
    def test_error_summary(self):
        """测试错误摘要"""
        source = """
        x = y;  // 错误1：y未定义
        z = 10;
        if (z) {  // 错误2：条件不是布尔类型
            w = 1;
        }
        """
        ast = parse_source(source)
        
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        assert len(errors) == 2
        assert analyzer.has_errors() is True
        
        summary = analyzer.get_error_summary()
        assert "发现 2 个语义错误" in summary
        assert "未定义的标识符" in summary
        assert "条件必须是布尔类型" in summary