import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{base_dir}/lib.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
