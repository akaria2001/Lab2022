import re

N = int(input())

# search for 10 digit string beginning with 7,8 or 9
pattern = r"(7|8|9)(\d){9}"

for _ in range(5):
    if re.fullmatch(pattern, input()):
        print("YES")
    else:
        print("NO")
