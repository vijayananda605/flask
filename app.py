from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///people.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class People(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    age = db.Column(db.Integer, nullable = False)

@app.route('/', methods=['GET'])
def index():
    name_filter = request.args.get('name', '')
    min_age = request.args.get('min_age' , type = int)
    max_age = request.args.get('max_age', type = int)
    
    query = People.query

    if name_filter:
        query = query.filter(People.name.contains(name_filter))
    if min_age is not None:
        query = query.filter(People.age>= min_age)
    if max_age is not None:
        query = query.filter(People.age<= max_age)

    people = query.all()
    return render_template('tables.html', people=people)
    
@app.route('/add', methods = ['GET'])
def add_form():
    return render_template('add_person.html')

@app.route('/add', methods = ['POST'])
def add_person():
    name = request.form['name']
    age = request.form['age']
    new_person = People(name=name, age=age)
    db.session.add(new_person)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)
