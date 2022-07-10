from flask import Flask

app = Flask(__name__)


@app.route("/add/<int:num1>/<int:num2>")
def addition(num1, num2):
    return f"{num1 + num2}"


@app.route("/sub/<int:num1>/<int:num2>")
def subtraction(num1, num2):
    return f"{num1 - num2}"


@app.route("/mul/<int:num1>/<int:num2>")
def multiplication(num1, num2):
    return f"{num1 * num2}"


@app.route("/div/<int:num1>/<int:num2>")
def division(num1, num2):
    result = (num1 / num2)
    return f"{result}"


@app.route("/math/<int:num1>/<int:num2>")
def math(num1, num2):
    add = addition(num1, num2)
    sub = subtraction(num1, num2)
    mul = multiplication(num1, num2)
    div = division(num1, num2)
    return f"{add}\n{sub}\n{mul}\n{div}"
