from flask import Flask, request, url_for, redirect, render_template

import db

app = Flask(__name__)


@app.route("/snacks", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        db.add_snack(request.form['name'], request.form['kind'])
        return redirect(url_for('index'))
    return render_template('index.html', snacks=db.get_all_snacks())


@app.route("/snacks/new")
def new():
    return render_template('new.html')


@app.route("/snacks/<int:id>", methods=["GET", "POST"])
def show(id):
    snacks = db.get_all_snacks()

    found_snack = next(snack for snack in snacks if snack[0] == id)

    if request.method == "POST":
        if request.form['method'] == "PATCH":
            db.update_snack(id, request.form['name'], request.form['kind'])
        elif request.form['method'] == "DELETE":
            db.delete_snack(id)
            return redirect(url_for('index'))

    return render_template('show.html', snack=found_snack)


@app.route("/snacks/<int:id>/edit")
def edit(id):
    snacks = db.get_all_snacks()

    found_snack = next(snack for snack in snacks if snack[0] == id)

    return render_template('edit.html', snack=found_snack)


