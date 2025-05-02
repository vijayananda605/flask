from flask import Flask,request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///person.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.String(10), nullable=False)

@app.route('/')
def index():
    return render_template('add_person.html')

@app.route('/add')
def add_form():
    people = Person.query.all()
    return render_template('table.html', people=people)
    

@app.route('/add', methods=['POST'])
def add_person():
    name = request.form['name']
    age = request.form['age']
    new_person = Person(name=name, age=age)
    db.session.add(new_person)
    db.session.commit()
    return redirect(url_for('add_person'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)