from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Secret key
app.secret_key = 'voting_key_123'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'YOUR_MYSQL_PASSWORD'
app.config['MYSQL_DB'] = 'voting_system'

mysql = MySQL(app)


# Home Page
@app.route('/')
def index():
    return render_template('index.html')


# Voter Registration
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        prn = request.form['prn']
        email = request.form['email']
        mobile = request.form['mobile']
        age = request.form['age']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO voters
            (name, prn, email, mobile, age, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, prn, email, mobile, age, password))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('confirm_register'))

    return render_template('register.html')


# Registration Confirmation
@app.route('/confirm-register')
def confirm_register():
    return render_template('confirm_register.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        prn = request.form['prn']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT * FROM voters
            WHERE prn = %s AND password = %s
        """, (prn, password))

        voter = cur.fetchone()

        cur.close()

        if voter:
            return redirect(url_for('vote'))

        return "Invalid PRN or Password"

    return render_template('login.html')


# Voting Page
@app.route('/vote', methods=['GET', 'POST'])
def vote():

    cur = mysql.connection.cursor()

    # Get all candidates
    cur.execute("SELECT * FROM candidates")
    candidates = cur.fetchall()

    if request.method == 'POST':

        candidate_id = request.form['candidate']

        cur.execute("""
            UPDATE candidates
            SET votes = votes + 1
            WHERE id = %s
        """, (candidate_id,))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('confirm'))

    cur.close()

    return render_template(
        'vote.html',
        candidates=candidates
    )


# Vote Confirmation
@app.route('/confirm')
def confirm():
    return render_template('confirm.html')


# Election Results
@app.route('/results')
def results():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT name, party, votes
        FROM candidates
        ORDER BY votes DESC
    """)

    results = cur.fetchall()

    cur.close()

    return render_template(
        'results.html',
        results=results
    )


# ER Diagram
@app.route('/view-diagram')
def view_diagram():
    return render_template('diagram.html')


# Feedback
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():

    if request.method == 'POST':

        email = request.form['email']
        q1_rating = request.form['q1_rating']
        q2_ease_of_use = request.form['q2_ease_of_use']
        q3_recommend = request.form['q3_recommend']

        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO feedback
            (email, q1_rating, q2_ease_of_use, q3_recommend)
            VALUES (%s, %s, %s, %s)
        """, (
            email,
            q1_rating,
            q2_ease_of_use,
            q3_recommend
        ))

        mysql.connection.commit()
        cur.close()

        return "Thank you for your feedback!"

    return render_template('index.html')


# Run Application
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
