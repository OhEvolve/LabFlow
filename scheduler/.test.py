
class Function:

    def __init__(self):
        self.mystr = 'asdfasdf'

    @property
    def length(self):
        return len(self.mystr)

f = Function()
print f.length
f.mystr = 'ADFSDF'
print f.length

