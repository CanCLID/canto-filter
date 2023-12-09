from setuptools import setup, find_packages
from cantofilter import __version__

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

    setup(
        name="canto-filter",
        version=__version__,
        author="CanCLID (Cantonese Computational Linguistics Infrastructure Development Workgroup)",
        author_email="support@jyutping.org",
        description="粵文分類篩選器 Cantonese text filter",
        long_description=long_description,
        long_description_content_type="text/markdown",
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
            "Natural Language :: Cantonese",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6",
        entry_points={
            "console_scripts": [
                "cantofilter=cantofilter.cli:main",  # 'command=package.module:function'
            ],
        },
    )
