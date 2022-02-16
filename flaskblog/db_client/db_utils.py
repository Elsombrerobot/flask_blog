from flaskblog import db

def commit(function):
    """Auto commit."""
    def wrap_function(*args, **kwargs):
        obj = function(*args, **kwargs)
        db.session.commit()
        return obj
    return wrap_function
    