import re

s = 'Venstre.Deres Ninja?Hurh'
# s = re.split('\./TEGN|\?/TEGN|[a-z]\?[A-Z]|[a-z]\.[A-Z]',  s)
s = re.split('[a-z](\?)\w', s)

print s

s = '(twoplusthree)plusfour'
l = re.split(r"(plus|\(|\))", s)
a = [x for x in l if x != '']
print a