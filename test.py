date = '8/3/2020'

d, m, y = date.split('/')
d = '0' + d if len(d) < 2 else d
m = '0' + m if len(m) < 2 else m
date = "/".join((d, m, y))
print(date)