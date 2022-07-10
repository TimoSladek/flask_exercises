from flask import Flask, render_template

app = Flask(__name__)


@app.route("/person/<name>/<int:age>")
def person(name, age):
    return render_template("person.html", name=name, age=age)


