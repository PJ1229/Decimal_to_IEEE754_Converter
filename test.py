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
    return ieee754

# Test for double precision
decimal = 100
binary_str = decimal_to_binary(decimal, 52)
ieee754_double = binary_to_ieee754(0, binary_str, precision='double')
print("Double Precision:", ieee754_double)

# Test for single precision
binary_str_single = decimal_to_binary(decimal, 23 + 1)  # 23 bits for mantissa + 1 for the implicit leading bit
ieee754_single = binary_to_ieee754(0, binary_str_single, precision='single')
print("Single Precision:", ieee754_single)
