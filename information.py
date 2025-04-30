from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(15), nullable = False)
    age = db.Column(db.String(10), nullable=False)
    button = db.Column(db.String(15), nullable = False)

@app.route("/", methods=['POST','GET'])
def info():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        button = request.form['button']

        new_user = User(name=name, age=age, button=button)
        db.session.add(new_user)
        db.session.commit()

        return render_template("result.html", name=name, age=age, button=button)
    
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
