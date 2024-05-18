from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask(__name__)
app.secret_key = 'bancawebudla'  


db_connection = pymysql.connect(
    host='localhost',
    user='root',
    database='bancoweb',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']

        cursor = db_connection.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (usuario,))
        user = cursor.fetchone()

        if user:
            session['usuario'] = usuario
            return redirect(url_for('operaciones'))
        else:
            return 'Usuario incorrecto'
    return render_template('login.html')

@app.route('/operaciones')
def operaciones():
    if 'usuario' in session:
        return render_template('operaciones.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
