from app import create_app
import os
from app.extensions import db
from flask_migrate import Migrate
from app.models.user import User

env = os.environ.get("FLASK_CONFIG", "default")

app = create_app(env)
Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)