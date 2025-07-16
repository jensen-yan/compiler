#!/usr/bin/env python3
"""
语法分析器演示程序
展示从源代码到AST的完整过程
"""

from src.lexer import Lexer
from src.parser import Parser
from src.ast import *


class AST打印器(ASTVisitor):
    """AST打印访问者，用于可视化AST结构"""
    
    def __init__(self):
        self.indent_level = 0
    
    def _indent(self) -> str:
        return "  " * self.indent_level
    
    def _print_with_indent(self, text: str) -> str:
        return self._indent() + text
    
    def visit_程序(self, node: 程序) -> str:
        result = [self._print_with_indent("程序:")]
        self.indent_level += 1
        for stmt in node.语句列表:
            result.append(self.visit(stmt))
        self.indent_level -= 1
        return "\n".join(result)
    
    def visit_二元运算表达式(self, node: 二元运算表达式) -> str:
        result = [self._print_with_indent(f"二元运算表达式 ({node.运算符.值}):")]
        self.indent_level += 1
        result.append(self._print_with_indent("左操作数:"))
        self.indent_level += 1
        result.append(self.visit(node.左操作数))
        self.indent_level -= 1
        result.append(self._print_with_indent("右操作数:"))
        self.indent_level += 1
        result.append(self.visit(node.右操作数))
        self.indent_level -= 2
        return "\n".join(result)
    
    def visit_一元运算表达式(self, node: 一元运算表达式) -> str:
        result = [self._print_with_indent(f"一元运算表达式 ({node.运算符.值}):")]
        self.indent_level += 1
        result.append(self.visit(node.操作数))
        self.indent_level -= 1
        return "\n".join(result)
    
    def visit_字面量表达式(self, node: 字面量表达式) -> str:
        return self._print_with_indent(f"字面量: {node.值!r}")
    
    def visit_标识符表达式(self, node: 标识符表达式) -> str:
        return self._print_with_indent(f"标识符: {node.名称}")
    
    def visit_函数调用表达式(self, node: 函数调用表达式) -> str:
        result = [self._print_with_indent("函数调用:")]
        self.indent_level += 1
        result.append(self._print_with_indent("函数:"))
        self.indent_level += 1
        result.append(self.visit(node.函数))
        self.indent_level -= 1
        if node.参数列表:
            result.append(self._print_with_indent("参数:"))
            self.indent_level += 1
            for i, arg in enumerate(node.参数列表):
                result.append(self._print_with_indent(f"参数 {i + 1}:"))
                self.indent_level += 1
                result.append(self.visit(arg))
                self.indent_level -= 1
            self.indent_level -= 1
        self.indent_level -= 1
        return "\n".join(result)
    
    def visit_赋值表达式(self, node: 赋值表达式) -> str:
        result = [self._print_with_indent("赋值表达式:")]
        self.indent_level += 1
        result.append(self._print_with_indent("目标:"))
        self.indent_level += 1
        result.append(self.visit(node.目标))
        self.indent_level -= 1
        result.append(self._print_with_indent("值:"))
        self.indent_level += 1
        result.append(self.visit(node.值))
        self.indent_level -= 2
        return "\n".join(result)
    
    def visit_表达式语句(self, node: 表达式语句) -> str:
        result = [self._print_with_indent("表达式语句:")]
        self.indent_level += 1
        result.append(self.visit(node.表达式))
        self.indent_level -= 1
        return "\n".join(result)
    
    def visit_变量声明语句(self, node: 变量声明语句) -> str:
        result = [self._print_with_indent(f"变量声明: {node.名称}")]
        if node.初始值:
            self.indent_level += 1
            result.append(self._print_with_indent("初始值:"))
            self.indent_level += 1
            result.append(self.visit(node.初始值))
            self.indent_level -= 2
        return "\n".join(result)
    
    def visit_函数声明语句(self, node: 函数声明语句) -> str:
        参数_str = ", ".join(node.参数列表) if node.参数列表 else "无参数"
        result = [self._print_with_indent(f"函数声明: {node.名称}({参数_str})")]
        self.indent_level += 1
        result.append(self._print_with_indent("函数体:"))
        self.indent_level += 1
        result.append(self.visit(node.函数体))
        self.indent_level -= 2
        return "\n".join(result)
    
    def visit_返回语句(self, node: 返回语句) -> str:
        result = [self._print_with_indent("返回语句:")]
        if node.返回值:
            self.indent_level += 1
            result.append(self.visit(node.返回值))
            self.indent_level -= 1
        return "\n".join(result)
    
    def visit_如果语句(self, node: 如果语句) -> str:
        result = [self._print_with_indent("如果语句:")]
        self.indent_level += 1
        result.append(self._print_with_indent("条件:"))
        self.indent_level += 1
        result.append(self.visit(node.条件))
        self.indent_level -= 1
        result.append(self._print_with_indent("Then分支:"))
        self.indent_level += 1
        result.append(self.visit(node.then分支))
        self.indent_level -= 1
        if node.else分支:
            result.append(self._print_with_indent("Else分支:"))
            self.indent_level += 1
            result.append(self.visit(node.else分支))
            self.indent_level -= 1
        self.indent_level -= 1
        return "\n".join(result)
    
    def visit_当语句(self, node: 当语句) -> str:
        result = [self._print_with_indent("当语句(while):")]
        self.indent_level += 1
        result.append(self._print_with_indent("条件:"))
        self.indent_level += 1
        result.append(self.visit(node.条件))
        self.indent_level -= 1
        result.append(self._print_with_indent("循环体:"))
        self.indent_level += 1
        result.append(self.visit(node.循环体))
        self.indent_level -= 2
        return "\n".join(result)
    
    def visit_代码块语句(self, node: 代码块语句) -> str:
        result = [self._print_with_indent("代码块:")]
        self.indent_level += 1
        for stmt in node.语句列表:
            result.append(self.visit(stmt))
        self.indent_level -= 1
        return "\n".join(result)


def main():
    print("=== 语法分析器演示 ===\n")
    
    # 读取示例程序
    with open("examples/simple_program.txt", "r", encoding="utf-8") as f:
        source_code = f.read()
    
    print("源代码:")
    print("-" * 40)
    print(source_code)
    print("-" * 40)
    
    try:
        # 词法分析
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        print(f"\n词法分析完成，共生成 {len(tokens)} 个tokens")
        
        # 语法分析
        parser = Parser(tokens)
        ast = parser.parse()
        
        print("语法分析完成！")
        
        # 打印AST结构
        print("\nAST结构:")
        print("=" * 40)
        printer = AST打印器()
        ast_str = printer.visit(ast)
        print(ast_str)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()