from utils import env

env.load()

DEVEL=env.get_bool('DEVEL', False)

class BaseConfig:
    DEVEL=DEVEL
    PORT=env.get_int('PORT', 5001)
    SECRET_KEY=env.get('SECRET_KEY')


class DevelopmentConfig(BaseConfig):
    DEVEL = True
    DATABASE_URI = "sqlite://devel.db"


class ProductionConfig(BaseConfig):
    DATABASE_URI = None

