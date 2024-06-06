number1 = int(input("Please enter your first number: "))
number2 = int(input("Please enter your second number:"))

if number1 > number2 and number1 > 20:
    print("Option 1")
else:
    if number1 == number2:
        print("Option 2")
    else:
        print("Option 3")
