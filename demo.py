#!/usr/bin/env python3
"""
词法分析器演示程序
"""

from src.lexer import Lexer, TokenType

def main():
    print("=== 词法分析器演示 ===\n")
    
    # 读取示例程序
    with open("examples/simple_program.txt", "r", encoding="utf-8") as f:
        source_code = f.read()
    
    print("源代码:")
    print("-" * 40)
    print(source_code)
    print("-" * 40)
    
    # 创建词法分析器
    lexer = Lexer(source_code)
    
    # 进行词法分析
    print("\n词法分析结果:")
    print("-" * 40)
    
    token_count = 0
    for token in lexer:
        # 跳过换行符以简化输出
        if token.类型 == TokenType.换行:
            continue
        
        token_count += 1
        print(f"{token_count:2d}. {token}")
    
    print(f"\n总共识别了 {token_count} 个token")

if __name__ == "__main__":
    main()