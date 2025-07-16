#!/usr/bin/env python3
"""
语义分析器演示程序
展示从源代码到语义分析的完整过程
"""

from src.lexer import Lexer
from src.parser import Parser
from src.semantic import 语义分析器
from src.ast import *


def main():
    print("=== 语义分析器演示 ===\n")
    
    # 示例程序1：正确的程序
    print("1. 正确的程序:")
    print("-" * 40)
    
    correct_source = """
    func add(a, b) {
        return a + b;
    }
    
    func factorial(n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    
    x = 10;
    y = 20;
    sum = add(x, y);
    
    if (sum > 25) {
        print("和很大");
        result = factorial(5);
        print(str(result));
    } else {
        print("和较小");
    }
    """
    
    print(correct_source)
    print("-" * 40)
    
    try:
        # 词法分析
        lexer = Lexer(correct_source)
        tokens = lexer.tokenize()
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        
        # 语义分析
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        if errors:
            print("❌ 语义分析失败:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✅ 语义分析通过！")
            print(f"符号表信息:")
            print(analyzer.get_symbol_table_info())
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
    
    print("\n" + "=" * 50 + "\n")
    
    # 示例程序2：有错误的程序
    print("2. 有错误的程序:")
    print("-" * 40)
    
    error_source = """
    func test(x) {
        y = z;  // 错误：z未定义
        return x + y;
    }
    
    a = 10;
    b = "hello";
    c = a + b;  // 错误：类型不兼容
    
    if (a) {  // 错误：条件不是布尔类型
        print("test");
    }
    
    result = test(1, 2);  // 错误：参数数量不匹配
    
    undefined_func();  // 错误：函数未定义
    """
    
    print(error_source)
    print("-" * 40)
    
    try:
        # 词法分析
        lexer = Lexer(error_source)
        tokens = lexer.tokenize()
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        
        # 语义分析
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        if errors:
            print("❌ 发现语义错误:")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error}")
        else:
            print("✅ 语义分析通过！")
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
    
    print("\n" + "=" * 50 + "\n")
    
    # 示例程序3：类型推导演示
    print("3. 类型推导演示:")
    print("-" * 40)
    
    type_source = """
    // 基本类型推导
    int_var = 42;
    float_var = 3.14;
    string_var = "hello";
    bool_var = true;
    
    // 表达式类型推导
    result1 = int_var + float_var;  // 整数 + 浮点数 = 浮点数
    result2 = int_var > 10;         // 比较运算 = 布尔值
    result3 = string_var + " world"; // 字符串 + 字符串 = 字符串
    
    // 函数类型推导
    func square(x) {
        return x * x;
    }
    
    squared = square(5);
    """
    
    print(type_source)
    print("-" * 40)
    
    try:
        # 词法分析
        lexer = Lexer(type_source)
        tokens = lexer.tokenize()
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        
        # 语义分析
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        if errors:
            print("❌ 发现语义错误:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✅ 语义分析通过！")
            print("\n变量类型推导结果:")
            
            # 显示变量类型
            scope = analyzer.作用域管理器.全局作用域
            if scope:
                for symbol in scope.get_all_symbols():
                    if symbol.get_种类().name == "变量":
                        print(f"  {symbol.名称}: {symbol.类型}")
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
    
    print("\n" + "=" * 50 + "\n")
    
    # 示例程序4：作用域演示
    print("4. 作用域演示:")
    print("-" * 40)
    
    scope_source = """
    global_var = 100;
    
    func outer() {
        outer_var = 200;
        
        func inner() {
            inner_var = 300;
            return global_var + outer_var + inner_var;
        }
        
        return inner();
    }
    
    result = outer();
    """
    
    print(scope_source)
    print("-" * 40)
    
    try:
        # 词法分析
        lexer = Lexer(scope_source)
        tokens = lexer.tokenize()
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        
        # 语义分析
        analyzer = 语义分析器()
        errors = analyzer.analyze(ast)
        
        if errors:
            print("❌ 发现语义错误:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✅ 语义分析通过！")
            print("\n作用域和符号表信息:")
            print(analyzer.get_symbol_table_info())
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")


if __name__ == "__main__":
    main()