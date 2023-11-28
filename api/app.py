from config import DEVEL, DevelopmentConfig, ProductionConfig
from flask import Flask

app = Flask(__name__)
conf = DevelopmentConfig if DEVEL else ProductionConfig
app.config.from_object(conf)


import staff_users
staff_users.views.register_views(app)

if DEVEL and __name__ == '__main__':
    app.run(host='0.0.0.0', port=conf.PORT)
