from flask import Flask
from flask_admin import Admin

app = Flask(__name__)
app.secret_key = "[\xdd\xa5\xfb\x85\x1c\x1d\xf2\x8d\x196ms\x02-\x17"

admin = Admin(app=app)