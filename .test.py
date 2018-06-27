
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        return 'Point(x=%s, y=%s)' % (self.x, self.y)
    def __eq__(self,x):
        return True

print Point(1,2)
print Point(2,3)




