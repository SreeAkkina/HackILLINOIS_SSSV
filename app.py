from flask import Flask,request, Response
from werkzeug.utils import secure_filename

from db import db_init, db
from models import Img

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

@app.route('/')
def hello_world():
    return 'index.html'

@app.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']

    if not pic:
        return 'No pic uploaded', 400
    
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    
    img = Img(img=pic.read(), mimetype=mimetype, name=filename)
    db.session.add(img)
    db.session.commit()

    return 'Img has been uploaded!', 200

@app.route('/<int:id>') 
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'No img with that id', 404
    
    return Response(img.img, mimetype=img.mimetype)
    
