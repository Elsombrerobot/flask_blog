from flaskblog import db
from flaskblog.db_client.db_utils import commit
from flaskblog.models import Post, User

def get(post_id : str):
    """Get a post."""
    return Post.query.get(post_id)

@commit
def create(title : str, content : str, author : User=None):
    """Create a post."""
    post = Post(title=title, content=content, author=author)
    db.session.add(post)
    return post

@commit
def update(post : Post, title : str=None, content : str=None, author : User=None):
    """Update a post."""
    post.title = title or post.title 
    post.content = content or post.title 
    post.author = author or post.author
    return post

@commit
def remove(post : Post):
    """Remove a post."""
    db.session.delete(post)
    return post
