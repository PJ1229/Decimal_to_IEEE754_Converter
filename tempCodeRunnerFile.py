def decimal_to_binary(decimal, total_length):
    binary = ""
    integral = int(decimal)
    fractional = decimal - integral 
    integral_binary = ""
    if integral == 0:
        integral_binary = "0"
    else:
        while integral:
            remainder = integral % 2
            integral_binary = str(remainder) + integral_binary
            integral //= 2
    binary += integral_binary + '.'
    fractional_length = total_length - len(integral_binary) - 1
    while fractional_length > 0:
        fractional *= 2
        fraction_bit = int(fractional)
        if fraction_bit == 1:
            fractional -= fraction_bit
            binary += '1'
        else:
            binary += '0'
        fractional_length -= 1
    if len(binary) < total_length:
        binary = binary.ljust(total_length, '0')
    
    return binary

def binary_to_ieee754(binary):
    shift = len(int(binary).split('.')[0] - 1)
    print(shift)


decimal = -121482941.1
binary = decimal_to_binary(decimal, 52)
binary_to_ieee754(binary)
print(binary)
