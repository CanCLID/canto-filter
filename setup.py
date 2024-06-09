from setuptools import setup, find_packages
# Read the version from cantofilter/version.py
version = {}
with open("cantofilter/version.py") as fp:
    exec(fp.read(), version)

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

    setup(
        name="canto-filter",
        version=version['__version__'],
        author="CanCLID (Cantonese Computational Linguistics Infrastructure Development Workgroup)",
        author_email="support@jyutping.org",
        description="粵文分類篩選器 Cantonese text filter",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "License :: OSI Approved :: MIT License",
            "Intended Audience :: Developers",
            "Topic :: Text Processing :: Linguistic",
            "Natural Language :: Cantonese",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.11",
        entry_points={
            "console_scripts": [
                "cantofilter=cantofilter.cli:main",  # 'command=package.module:function'
            ],
        },
    )
