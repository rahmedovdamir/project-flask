import secrets
import os.path
from flask import current_app
from PIL import Image
import urllib.parse

def save_picture(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['SERVER_PATH'], picture_fn)
    output_size = (125,125)
    i = Image.open(picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def generate_group_schedule_url(group_name):
    encoded_group_name = urllib.parse.quote(group_name)
    
    base_url = "https://schedule-of.mirea.ru/schedule/api/search"
    url = f"{base_url}?limit=15&match={encoded_group_name}"
    
    return url