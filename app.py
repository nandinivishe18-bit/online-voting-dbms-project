from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'voting_key_123'

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'YOUR_MYSQL_PASSWORD'
app.config['MYSQL_DB'] = 'voting_system'

mysql = MySQL(app)


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form.get('name')
        prn = request.form.get('prn')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        age = request.form.get('age')
        password = request.form.get('password')

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM voters WHERE prn = %s",
            (prn,)
        )

        if cur.fetchone():
            cur.close()
            return "<h3>PRN already registered! <a href='/register'>Try again</a></h3>"

        cur.execute(
            """INSERT INTO voters
            (name, prn, email, mobile, age, password)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (name, prn, email, mobile, age, password)
        )

        mysql.connection.commit()
        cur.close()

        return render_template('confirm_register.html')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        prn = request.form['prn']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM voters WHERE prn = %s AND password = %s",
            (prn, password)
        )

        user = cur.fetchone()
        cur.close()

        if user:
            return redirect(url_for('vote'))

        return "<h3>Invalid PRN or Password! <a href='/login'>Try again</a></h3>"

    return render_template('login.html')


@app.route('/vote', methods=['GET', 'POST'])
def vote():

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        candidate_id = request.form.get('candidate_id')

        cur.execute(
            "UPDATE candidates SET votes = votes + 1 WHERE id = %s",
            (candidate_id,)
        )

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('results'))

    cur.execute("SELECT * FROM candidates")
    candidates = cur.fetchall()

    cur.close()

    return render_template(
        'vote.html',
        candidates=candidates
    )


@app.route('/results')
def results():

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT name, party, votes FROM candidates"
    )

    data = cur.fetchall()

    cur.close()

    return render_template(
        'results.html',
        candidates=data
    )


@app.route('/view-diagram')
def view_diagram():
    return render_template('diagram.html')


@app.route('/feedback', methods=['POST'])
def feedback():

    email = request.form.get('email')
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')

    cur = mysql.connection.cursor()

    cur.execute(
        """INSERT INTO feedback
        (email, q1_rating, q2_ease_of_use, q3_recommend)
        VALUES (%s, %s, %s, %s)""",
        (email, q1, q2, q3)
    )

    mysql.connection.commit()
    cur.close()

    return render_template('confirm.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
