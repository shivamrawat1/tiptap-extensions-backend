from app import create_app
from app.cli import init_app

app = create_app()
init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
