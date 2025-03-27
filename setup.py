from setuptools import setup, find_packages

setup(
    name="wechat-automation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0,<0.69.0",
        "uvicorn>=0.15.0,<0.16.0",
        "sqlalchemy>=1.4.0,<1.5.0",
        "alembic>=1.7.0,<1.8.0",
        "psycopg2-binary>=2.9.1,<2.10.0",
        "python-jose[cryptography]>=3.3.0,<3.4.0",
        "passlib[bcrypt]>=1.7.4,<1.8.0",
        "python-multipart>=0.0.5,<0.0.6",
        "python-dotenv>=0.19.0,<0.20.0",
    ],
) 