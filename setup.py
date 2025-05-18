from setuptools import setup, find_packages

setup(
    name="idp-project",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=5.0",
        "mysqlclient>=2.2.1",
        "Pillow>=10.1.0",
        "pytesseract>=0.3.10",
        "pdf2image>=1.16.3",
        "spacy>=3.7.2",
        "nltk>=3.8.1",
        "python-magic>=0.4.27",
        "python-dotenv>=1.0.0",
    ],
    description="Intelligent Document Processing System",
    author="IDP Team",
    author_email="contact@idp-project.example.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Topic :: Document Processing",
    ],
    python_requires=">=3.10",
) 