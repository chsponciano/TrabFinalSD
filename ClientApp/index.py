from flask import Flask, render_template, request, redirect, session, flash, url_for
import subprocess

app = Flask(__name__)
contador = 1


@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/add', methods=['POST',])
@app.route('/add')
def add_server():
    global contador
    #id_server = request.form['id_server']
    #cust_server = request.form['cust_server']

    with open("output.log", "a") as output:
        subprocess.call("docker run -d --network graph-network chsponciano/noderabbit python ServerAppInitialize.py q" + str(contador),
                        shell=True, stdout=output, stderr=output)

    contador += 1
    return redirect(url_for('index'))


@app.route('/route')
def calcule_router():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
