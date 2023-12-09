from setuptools import setup, find_packages

setup(
    name="canto-filter",
    version="1.0.0",
    author="CanCLID (Cantonese Computational Linguistics Infrastructure Development Workgroup)",
    author_email="support@jyutping.org",
    description="粵文分類篩選器 Cantonese text filter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "cantofilter=cantofilter.cli:main",  # 'command=package.module:function'
        ],
    },
)
