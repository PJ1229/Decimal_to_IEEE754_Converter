from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # Retrieve form data
        decimal = request.form['decimal']
        bits = request.form['bits']
        
        # Example conversion logic (you can replace it with actual IEEE 754 conversion logic)
        result = f"Convert {decimal} to IEEE 754 number with {bits} bits"
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
