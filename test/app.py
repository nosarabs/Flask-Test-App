from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r' % self.id

@app.route('/')
def index():
    title = "Index"
    return render_template("index.html", title=title)

@app.route('/test', methods=['POST', 'GET'])
def test():
    title = "Test Database"

    if request.method == "POST":
        testName = request.form['name']
        testObj = Test(name=testName)

        try:
            db.session.add(testObj)
            db.session.commit()
            return redirect('/test')
        except:
            return "Error adding object"
    else:
        objs = Test.query.order_by(Test.date_created)
        return render_template("test.html", objs=objs, title=title)
    