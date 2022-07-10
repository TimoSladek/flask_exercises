from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-sql-snacks"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Snack(db.Model):
    __tablename__ = "snacks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    kind = db.Column(db.Text)

    def __init__(self, name, kind):
        self.name = name
        self.kind = kind


@app.route("/snacks", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        db.session.add(Snack(request.form['name'], request.form['kind']))
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', snacks=Snack.query.all())


@app.route("/snacks/new")
def new():
    return render_template('new.html')


@app.route("/snacks/<int:id>", methods=["GET", "POST"])
def show(id):
    found_snack = Snack.query.get_or_404(id)

    if request.method == "POST":
        if request.form['method'] == "PATCH":
            found_snack.name = request.form['name']
            found_snack.kind = request.form['kind']
            db.session.add(found_snack)
            db.session.commit()
        elif request.form['method'] == "DELETE":
            db.session.delete(found_snack)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('show.html', snack=found_snack)


@app.route("/snacks/<int:id>/edit")
def edit(id):
    found_snack = Snack.query.get_or_404(id)

    return render_template('edit.html', snack=found_snack)
