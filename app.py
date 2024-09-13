from flask import Flask, render_template, request

app = Flask(__name__)

# Convert decimal to binary whole number
def decimal_to_binary(decimal, total_length):
    if decimal == 0:
        return '0.' + '0' * (total_length - 2)
    
    binary = ""
    integral = int(decimal)
    fractional = decimal - integral 

    # Convert integral part
    integral_binary = ""
    while integral:
        integral_binary = str(integral % 2) + integral_binary
        integral //= 2

    if not integral_binary:
        integral_binary = '0'
    
    # Convert fractional part
    fractional_binary = ""
    while len(fractional_binary) < (total_length - len(integral_binary) - 1):
        fractional *= 2
        fractional_bit = int(fractional)
        if fractional_bit == 1:
            fractional -= fractional_bit
            fractional_binary += '1'
        else:
            fractional_binary += '0'

    binary = integral_binary + '.' + fractional_binary
    if len(binary) < total_length:
        binary = binary.ljust(total_length, '0')

    return binary


# Convert binary to IEEE 754
def binary_to_ieee754(sign, binary, precision='double'):
    if precision == 'single':
        exponent_bits = 8
        mantissa_bits = 23
        exponent_bias = 127
    elif precision == 'double':
        exponent_bits = 11
        mantissa_bits = 52
        exponent_bias = 1023
    else:
        raise ValueError("Precision must be 'single' or 'double'")

    # Normalize binary string
    if '.' in binary:
        integral_part, fractional_part = binary.split('.')
    else:
        integral_part, fractional_part = binary, ''

    # Remove leading zeros
    integral_part = integral_part.lstrip('0')
    if not integral_part:
        integral_part = '0'

    # Calculate exponent
    if integral_part == '0':
        exponent = -fractional_part.find('1') - 1
    else:
        exponent = len(integral_part) - 1

    biased_exponent = exponent + exponent_bias
    exponent_binary = format(biased_exponent, f'0{exponent_bits}b')

    # Calculate mantissa
    mantissa = integral_part[1:] + fractional_part
    mantissa = mantissa.ljust(mantissa_bits, '0')[:mantissa_bits]

    # Construct IEEE 754 string
    ieee754 = str(sign) + exponent_binary + mantissa
    return f"{ieee754}"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # Retrieve data from form
        decimal_str = request.form['decimal']
        precision_str = request.form['bits']

        try:
            decimal = float(decimal_str)
        except ValueError:
            result = "Invalid decimal number"
            return render_template('index.html', result=result)
        
        precision = int(precision_str)

        if precision == 32:
            binary = decimal_to_binary(decimal, 24)
            ieee754 = binary_to_ieee754(0, binary, precision='single')
            result = ieee754
        elif precision == 64:
            binary = decimal_to_binary(decimal, 52)
            ieee754 = binary_to_ieee754(0, binary, precision='double')
            result = ieee754
        else:
            result = "Invalid precision value. Use 32 or 64."
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=False)
