from app import create_app
from app.apis.user_api import api

app = create_app()
app.register_blueprint(api, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def hello():
    return {'message': 'Hello from Sustainable Community Market'}