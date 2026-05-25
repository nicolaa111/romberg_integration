from flask import Flask, render_template, request
import math
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "../templates"))

allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}

def f(x, expression):
    allowed_names["x"] = x
    return eval(expression, {"__builtins__": {}}, allowed_names)

def romberg(expr, a, b, n):
    R = [[0]*n for _ in range(n)]
    h = b - a

    R[0][0] = (h/2)*(f(a, expr)+f(b, expr))

    for i in range(1, n):
        h /= 2
        total = 0

        for k in range(1, 2**i, 2):
            total += f(a + k*h, expr)

        R[i][0] = 0.5*R[i-1][0] + total*h

        for j in range(1, i+1):
            R[i][j] = R[i][j-1] + (R[i][j-1]-R[i-1][j-1])/(4**j - 1)

    return R[n-1][n-1], R


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/discussion")
def discussion():
    return render_template("discussion.html")


@app.route("/calculator", methods=["GET","POST"])
def calculator():
    result = None
    table = None

    if request.method == "POST":
        expr = request.form["function"]
        a = float(request.form["a"])
        b = float(request.form["b"])
        n = int(request.form["n"])

        result, table = romberg(expr, a, b, n)

    return render_template("calculator.html", result=result, table=table)


if __name__ == "__main__":
    app.run()
