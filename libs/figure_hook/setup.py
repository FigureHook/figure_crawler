from setuptools import find_packages, setup

setup(
    name="figure_hook",
    version="0.0.1",
    author="Elton H.Y. Chou",
    author_email="plscd748@gmail.com",
    description="figure_hook",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
        "discord.py>=1.7.2",
        "Babel>=2.9.1",
        "sqlalchemy_mixins>=1.3",
        "psycopg2-binary>=2.8.6",
        "SQLAlchemy>=1.4.15"
    ]
)
