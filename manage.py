__author__ = 'jinming'

from app import create_app
from flask.ext.script import Server, Manager, Shell


app = create_app()
manager = Manager(app)


def make_shell_context():
    return dict(app=app)


manager.add_command("runserver", Server('0.0.0.0', port=5000))
manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == "__main__":
    manager.run()