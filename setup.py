"""
我的编译器 - 安装脚本
"""

from setuptools import setup, find_packages

setup(
    name="my-compiler",
    version="0.1.0",
    description="一个用于学习编译器原理的简单实现",
    author="学习者",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ],
    extras_require={
        "dev": [
            "black>=22.0.0",
            "flake8>=5.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "my-compiler=src.main:main",
        ],
    },
)