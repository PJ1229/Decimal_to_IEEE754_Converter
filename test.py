def decimal_to_binary(decimal):
    binary = ''
    while decimal != 0:
        if decimal % 2 == 1:
            binary = '1' + binary
        else:
            binary = '0' + binary
        decimal = decimal // 2

    return binary

decimal = 1243515
binary = decimal_to_binary(decimal)
print(binary)
