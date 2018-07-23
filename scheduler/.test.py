
def func(a):
    for i,b in enumerate(a):
        b[0] += 1

a = [[1],[2],[3]]

print a
func(a)
print a
