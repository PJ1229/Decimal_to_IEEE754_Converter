from flask import Flask, render_template, request

app = Flask(__name__)

# decimal to binary conversion
def decimal_to_binary(decimal, total_length):
    # determine if the number is negative
    is_negative = decimal < 0
    decimal = abs(decimal)

    # returns if decimal is 0
    if decimal == 0:
        return '0.' + '0' * (total_length - 2)

    # calculates integral and fractional parts
    binary = ""
    integral = int(decimal)
    fractional = decimal - integral

    # establishes integral_binary
    integral_binary = ""
    while integral:
        integral_binary = str(integral % 2) + integral_binary
        integral //= 2
    if not integral_binary:
        integral_binary = '0'

    # establishes fractional_binary
    fractional_binary = ""
    while len(fractional_binary) < (total_length - len(integral_binary) - 1):
        fractional *= 2
        fractional_bit = int(fractional)
        if fractional_bit == 1:
            fractional -= fractional_bit
            fractional_binary += '1'
        else:
            fractional_binary += '0'

    # combines integral_binary and fractional_binary
    binary = integral_binary + '.' + fractional_binary
    if len(binary) < total_length:
        binary = binary.ljust(total_length, '0')

    # returns binary
    return binary

# binary to ieee 754 conversion
def binary_to_ieee754(sign, binary, precision='double'):
    # checks precision type and allocates bits
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

    # normalize binary string
    if '.' in binary:
        integral_part, fractional_part = binary.split('.')
    else:
        integral_part, fractional_part = binary, ''

    # remove leading zeros
    integral_part = integral_part.lstrip('0')
    if not integral_part:
        integral_part = '0'

    # calculate exponent
    if integral_part == '0':
        exponent = -fractional_part.find('1') - 1
    else:
        exponent = len(integral_part) - 1

    biased_exponent = exponent + exponent_bias
    exponent_binary = format(biased_exponent, f'0{exponent_bits}b')

    # calculate mantissa
    mantissa = integral_part[1:] + fractional_part
    mantissa = mantissa.ljust(mantissa_bits, '0')[:mantissa_bits]

    # construct ieee 754
    ieee754 = str(sign) + exponent_binary + mantissa
    return ieee754

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # request data
        decimal = float(request.form['decimal'])
        precision = int(request.form['bits'])

        # determine sign
        sign = 0
        if decimal < 0:
            sign = 1
            decimal = abs(decimal)

        # returns data based on precision type
        if precision == 32:
            binary = decimal_to_binary(decimal, 24)
            ieee754 = binary_to_ieee754(sign, binary, precision='single')
            result = f"The conversion of {request.form['decimal']} in decimal to IEEE 754 with 32 bits of precision is {ieee754}"
        elif precision == 64:
            binary = decimal_to_binary(decimal, 52)
            ieee754 = binary_to_ieee754(sign, binary, precision='double')
            result = f"The conversion of {request.form['decimal']} in decimal to IEEE 754 with 64 bits of precision is {ieee754}"
        else:
            result = "Invalid precision value. Use 32 or 64."

    # renders the template
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=False)
