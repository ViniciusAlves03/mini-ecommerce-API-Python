from flask_swagger_ui import get_swaggerui_blueprint
from config import swagger_config

swaggerui_blueprint = get_swaggerui_blueprint(
    swagger_config['SWAGGER_URL'],
    swagger_config['API_URL'],
    config={
        'app_name': "CRUD API"
    }
)
