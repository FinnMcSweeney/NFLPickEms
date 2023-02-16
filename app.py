from flask import Flask, request, redirect, render_template, session, url_for
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    username = request.args.get('username')
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username=username)
    else:
        return render_template('home.html', message="Please log in to view the picks.")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the database and check the credentials
        connection = mysql.connector.connect(
            host='localhost',
            user='sa',
            password='YOUR_strong_*pass4w0rd*',
            database='pickems'
        )
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            return redirect(f'/?username={username}')
        else:
            return 'Invalid credentials'

    return render_template('login.html')

@app.route('/submit_picks', methods=['POST'])
def submit_picks():
    # Retrieve the username from the form
    username = request.form['username']
    
    # Connect to the database and retrieve the user_id for the current user
    connection = mysql.connector.connect(
        host='localhost',
        user='sa',
        password='YOUR_strong_*pass4w0rd*',
        database='pickems'
    )
    cursor = connection.cursor()
    cursor.execute(f"SELECT user_id FROM users WHERE username='{username}'")
    user_id = cursor.fetchone()[0]
    cursor.close()
    connection.close()

    # Use the user_id in the insert statement
    connection = mysql.connector.connect(
        host='localhost',
        user='sa',
        password='YOUR_strong_*pass4w0rd*',
        database='pickems'
    )
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO picks (user_id, spread, over_under, coin_toss, score_first, 
            mahomes_passing_yards, hurts_passing_yards, receiving,
            octopus, longest, flag)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, request.form['spread'], request.form['over_under'], request.form['coin_toss'], 
        request.form['score_first'], request.form['mahomes_passing_yards'], 
        request.form['hurts_passing_yards'], request.form['receiving'], 
        request.form['octopus'], request.form['longest'], request.form['flag']))
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect('/')
    
@app.route('/recap')
def recap():
    username = request.args.get('username')
    if username:
        return render_template('recap.html', username=username)
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
