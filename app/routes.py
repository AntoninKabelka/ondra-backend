import os
from app import app, db
from flask import request, jsonify, redirect, url_for, send_from_directory, render_template, send_file
from werkzeug.utils import secure_filename
import datetime

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    technical_skill = db.Column(db.Integer)
    version = db.Column(db.String(10))
    age = db.Column(db.String(10))
    gender = db.Column(db.String(10))

@app.route('/info')
@app.route('/')
@app.route('/index')
def info():
    return jsonify({'message': 'Backend for testing app'})

@app.route('/api/v1/test/create', methods=["POST"])
def create_test():
    name = request.form['name']
    folder_name = name

    path = os.getcwd()
    print ("The current working directory is %s" % path)

    path = os.path.join(path, 'data', folder_name)
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    return redirect(url_for('index'))

@app.route('/api/v1/file/upload/<test_id>', methods=['POST'])
def upload_file(test_id):
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], str(test_id), filename))
    return jsonify({'message': 'file saved'})

@app.route('/api/v1/test', methods=["POST"])
def create_test_db():
    data = request.get_json()

    # create test in db
    new_test = Test(
	    name = data['name'],
		technical_skill = data['skill'],
        version = data['version'],
        age = data['age'],
        gender = data['gender']
    )

    db.session.add(new_test)
    db.session.commit()
    path = os.getcwd()

    print ("The current working directory is %s" % path)

    path = os.path.join(path, 'data', str(new_test.id))
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    
    return jsonify({ 'test_id' : new_test.id })

@app.route("/api/v1/get_file")
def get_file():
    path = os.getcwd()
    print(path)
    return send_from_directory(os.path.join(path, app.config['UPLOAD_PATH'], '16'), '10-1.wav')

@app.route("/api/v1/test/<id>")
def get_test(id):
    test = Test.query.get_or_404(id)
    data = {}
    data['id'] = test.id
    data['name'] = test.name
    data['age'] = test.age
    data['technical_skill'] = test.technical_skill
    data['version'] = test.version
    data['gender'] = test.gender
    return jsonify({ "test" : data })
