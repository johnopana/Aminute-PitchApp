from app import create_app, db
# from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Server
from app.models import User, Pitch, Comment
from config import Config
from flask_migrate import Migrate, MigrateCommand
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os   

from app import create_app  

app = create_app('production')

manager = Manager(app, db)
migrate = Migrate(app, db)

manager.add_command('server', Server)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User, Pitch = Pitch, Comment = Comment)

if __name__ == '__main__':
    manager.run()
    db.create_all()