from setuptools import find_packages, setup

setup(
    name="basic_task",
    version="0.0.1",
    author="Elton H.Y. Chou",
    author_email="plscd748@gmail.com",
    description="celery tasks",
    package_dir={"": "."},
    packages=find_packages("."),
    python_requires=">=3.6",
    install_requires=[
        "celery",
        "discord.py",
        "SQLAlchemy",
    ]
)
