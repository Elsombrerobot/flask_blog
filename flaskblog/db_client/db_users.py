from flaskblog import db
from flaskblog.db_client.db_utils import commit
from flaskblog.models import Post, User

def get(user_id : str):
    """Get a User."""
    return User.query.get(user_id)

@commit
def create(username : str, email : str, password : str, image_file : str):
    """Create a user."""
    user = User(username=username, email=email, password=password, image_file=image_file)
    db.session.add(user)
    return user

@commit
def update(user : User, username : str=None, email : str=None, password : str=None, image_file : str=None):
    """Update a user."""
    user.username = username or user.username
    user.email = email or user.email
    user.password = password or user.password
    user.image_file = image_file or user.image_file
    return user

@commit
def remove(user : User):
    """Remove a user."""
    db.session.delete(user)