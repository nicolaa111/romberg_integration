from flask import Flask, render_template, request
import math

app = Flask(__name__, template_folder='../templates')

allowed_names = {
    k: getattr(math, k)
    for k in dir(math)
    if not k.startswith("__")
}

def f(x, expression):
    allowed_names['x'] = x
    return eval(expression, {"__builtins__": {}}, allowed_names)

def romberg_integration(expression, a, b, n):

    R = [[0 for _ in range(n)] for _ in range(n)]

    h = b - a

    R[0][0] = (h / 2) * (
        f(a, expression) + f(b, expression)
    )

    for i in range(1, n):

        h /= 2

        summation = 0

        for k in range(1, 2**i, 2):
            summation += f(a + k*h, expression)

        R[i][0] = 0.5 * R[i-1][0] + summation * h

        for j in range(1, i + 1):
            R[i][j] = R[i][j-1] + (
                (R[i][j-1] - R[i-1][j-1]) /
                (4**j - 1)
            )

    return R[n-1][n-1], R


@app.route('/', methods=['GET', 'POST'])
def home():

    result = None
    table = None

    if request.method == 'POST':

        func = request.form['function']
        a = float(request.form['a'])
        b = float(request.form['b'])
        n = int(request.form['n'])

        result, table = romberg_integration(func, a, b, n)

    return render_template(
        'index.html',
        result=result,
        table=table
    )


if __name__ == '__main__':
    app.run()