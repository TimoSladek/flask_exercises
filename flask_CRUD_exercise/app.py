from flask import Flask, request, url_for, redirect, render_template
from snack import Snack

app = Flask(__name__)

potato_chips = Snack("Lays", "Salt")
tortilla_chips = Snack("Doritos", "Cheese")

snacks = [potato_chips, tortilla_chips]
invalid_ids = []


@app.route("/snacks", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        snacks.append(Snack(request.form['name'], request.form['kind']))
        return redirect(url_for('index'))
    return render_template('index.html', snacks=snacks)


@app.route("/snacks/new")
def new():
    return render_template('new.html')


@app.route("/snacks/<int:id>", methods=["GET", "POST"])
def show(id):
    if id in invalid_ids or id > Snack.count:
        return redirect(url_for('invalid_id'))

    found_snack = next(snack for snack in snacks if snack.id == id)

    if request.method == "POST":
        if request.form['method'] == "PATCH":
            found_snack.name = request.form['name']
            found_snack.kind = request.form['kind']
        elif request.form['method'] == "DELETE":
            invalid_ids.append(found_snack.id)
            snacks.remove(found_snack)
            return redirect(url_for('index'))

    return render_template('show.html', snack=found_snack)


@app.route("/snacks/<int:id>/edit")
def edit(id):
    if id in invalid_ids or id > Snack.count:
        return redirect(url_for('invalid_id'))

    found_snack = next(snack for snack in snacks if snack.id == id)

    return render_template('edit.html', snack=found_snack)


@app.route("/404page")
def invalid_id():
    return render_template('404page.html')
