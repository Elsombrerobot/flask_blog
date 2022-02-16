from flask import url_for
from flaskblog import mail
from flask_mail import Message
import secrets
from PIL import Image
from pathlib import Path
from flask import current_app
from PIL import Image, ImageColor, ImageDraw, ImageFont
import random

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_ext = Path(form_picture.filename).suffix
    picture_fn = random_hex + f_ext
    picture_path = Path(current_app.root_path) / "static" / "profile_pics" / picture_fn
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(str(picture_path))
    return picture_fn
    
def delete_picture(picture_fn):
    picture_path = Path(current_app.root_path) / "static" / "profile_pics" / picture_fn
    Path(picture_path).unlink()
    return picture_path

def generate_profile_picture(username, size=125):
    initials = (username[0] + username[1]).upper()
    font_size=50
    font = Path(current_app.root_path) / "static" / "JosefinSans-Bold.ttf"
    colors = [name for name, _ in ImageColor.colormap.items()]
    colors.remove("white")
    color = random.choice(colors)
    img = Image.new('RGB', (size, size), color = color)
    font_type = ImageFont.truetype(str(font),font_size)
    fw, fh = font_type.getsize(initials)
    center = (size/2 - fw/2, size/2 - fh/2)
    draw = ImageDraw.Draw(img)
    draw.text(center, initials, font=font_type, fill="white")
    random_hex = secrets.token_hex(8)
    picture_fn = f'{random_hex}.jpeg'
    picture_path = Path(current_app.root_path) / "static" / "profile_pics" / picture_fn
    img.save(str(picture_path), quality=100)
    return picture_fn

