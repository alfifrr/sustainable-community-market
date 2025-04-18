from app import create_app
from app.apis import blueprints
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sustainable Community Market API"
    }
)

app = create_app()
app.register_blueprint(swagger_ui_blueprint)
for blueprint, url_prefix in blueprints:
    app.register_blueprint(blueprint, url_prefix=url_prefix)

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/')
def hello():
    return {'message': 'Hello from Sustainable Community Market'}
