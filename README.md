# 我的编译器

一个简单的编译器实现，用于学习编译器构造原理，包括词法分析、语法分析、AST构建、语义分析和代码生成。

## 项目结构

```
my_compiler/
├── src/
│   ├── __init__.py
│   ├── lexer/          # 词法分析器
│   ├── parser/         # 语法分析器  
│   ├── ast/            # AST节点定义
│   ├── semantic/       # 语义分析
│   ├── codegen/        # 代码生成
│   └── utils/          # 工具函数
├── tests/
│   ├── __init__.py
│   ├── unit/           # 单元测试
│   ├── integration/    # 集成测试
│   └── fixtures/       # 测试用例
├── examples/           # 示例源文件
└── docs/               # 文档
```

## 开发方式

本项目遵循测试驱动开发(TDD)原则：

1. 先写测试
2. 实现最小代码通过测试
3. 重构和改进

## 环境要求

- Python 3.8+
- pytest 用于测试
- coverage 用于测试覆盖率

## 安装

```bash
pip install -e .
```

## 运行测试

```bash
pytest tests/ -v
pytest tests/ --cov=src
```