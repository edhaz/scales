from distutils.core import setup

setup(
    name="scales",
    version="1.0",
    description="Scales web app",
    author="Ed Hazledine",
    author_email="ed.hazledine@gmail.com",
    packages=["scales"],
    install_requires=[
        "flask",
        "flask_sqlalchemy",
        "flask_login",
        "flask_wtf",
        "pyjwt",
        "email_validator",
    ],
)
