import re

file = open('a.txt', 'r')
txt = file.read()
file.close()
print(re.findall('Tomi', txt))

file = open ('a.txt', 'a')
txt = file.write(', how are u')
file.close()