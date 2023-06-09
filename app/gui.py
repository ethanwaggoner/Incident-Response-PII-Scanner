from flaskwebgui import FlaskUI
from app import create_app

app = create_app()

if __name__ == "__main__":
    FlaskUI(app=app, port=5001, server="flask", fullscreen=True).run()


