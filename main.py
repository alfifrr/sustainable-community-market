from app import create_app
from app.apis import blueprints

app = create_app()
for blueprint, url_prefix in blueprints:
    app.register_blueprint(blueprint, url_prefix=url_prefix)

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/')
def hello():
    return {'message': 'Hello from Sustainable Community Market'}
