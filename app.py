from flask import Flask, render_template, request

app = Flask(__name__)

# convert decimal to ieee754
def decimal_to_ieee754(decimal, bits):

    #return value
    return f"Converted {decimal} to IEEE 754 format with {bits} bits"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # retrieve data from form
        decimal = request.form['decimal']
        bits = request.form['bits']
        
         # set result to function
        result = decimal_to_ieee754(decimal, bits)
    
    return render_template('index.html', result=result)