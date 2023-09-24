import math

def square(number):
    output = number**2
    return output


def cubed(number):
    output = number**3
    return output


def square_root(number):
    return math.sqrt(number)


def floor_division(number):
    return number // 2


def modulus(number):
    return number % 2


def main():
    upperbound = 25
    print("Running Square Number function")
    for num in range(1, upperbound+1):
        print(f"{num} -> Squared {square(num)}")
    print("Running Cubed Number function")
    for num in range(1, upperbound+1):
        print(f"{num} -> Cubed {cubed(num)}")
    print("Running Floor Division Number function")
    for num in range(1, upperbound+1):
        print(f"{num} -> Floor Division (return whole number after division by 2) {floor_division(num)}")
    print("Running Modulus Number function")
    for num in range(1, upperbound+1):
        print(f"{num} ->  Modulus (/2 and remainder) {modulus(num)}")
    print("Running Square Root Number function, will only print whole numbers")
    for num in range(1, upperbound+1):
        val = round(square_root(num),3)
        print(f"{num} -> Square Root {val}") if val.is_integer() else None


if __name__ == '__main__':
    main()
