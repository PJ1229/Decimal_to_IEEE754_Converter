from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']  # Access 'name' input field
    email = request.form['email']  # Access 'email' input field

    # You can use the received data here (e.g., save to a database, perform logic)
    return f"Hello, {name}! Your email is {email}."