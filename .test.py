
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        print 'Repr'
        return 'Point(x=%s, y=%s)' % (self.x, self.y)
    def __eq__(self,a):
        print 'Eq'
        return all((self.x == a.x,self.y == a.y))

a = Point(1,2)
b = Point(3,4)


