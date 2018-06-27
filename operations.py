
"""

Testing to see if we can construct intelligent pipeline

Say we have a vector we want to transform to:
    <A,A,A,A> -> <B,B,B,B>

Let's imagine each of these elements as a certain characteristic of a sample:

1: Biologic,Cell
2: Sequence Content
3: Linear,Circular
4: Concentration

"""



def dist(v1,v2):
    """ Determine distance """
    return sum((e1 == e2) for e1,e2 in zip(v1,v2))



class Operation(object):

    def __init__(self):
        self.cost = 0
        self.time = 0

    def input(self): 
        NotImplementedError('Function needs forward')

    def output(self): 
        NotImplementedError('Function needs reverse')

    def input_template(self):
        NotImplementedError('Function needs output check')

    def output_template(self):
        NotImplementedError('Function needs output check')

    def check_input(self): # should define from template
        pass

    def check_output(self): # should define from template
        pass


class OligoSynthesis(Operation):

    name = 'Oligo Synthesis'
    input_template = (('*','*','*','*'),)
    output_template = (('Sequence',None,'Linear',None),)

class GBlockSynthesis(Operation):

    name = 'Oligo Synthesis'
    input_template = (('*','*','*','*'),)
    output_template = (('Sequence',None,'Linear',None),)

class Ligate(Operation):

    name = 'Ligate'
    input_template = (('Sequence',None,'Linear',None),('Sequence',None,'Linear',None))
    output_template = (('Sequence',None,'Circular',None),)

class Transform(Operation):

    name = 'Transform'
    input_template = (('Sequence',None,'Circular',None),)
    output_template = (('Cell',None,'Circular','low'),)

class Outgrowth(Operation):

    name = 'Outgrowth'
    input_template = (('Cell',None,None,'low'),)
    output_template = (('Cell',None,None,'high'),)


def gibson(v1,v2):
    pass

def grow(v1):
    pass  


def get_default_operations():
    return [OligoSynthesis,GBlockSynthesis,Ligate,Transform,Outgrowth]

start_samples = [
    ('CUT----------CUT','linear','soluble','low'),
    ('CUT*****CUT','linear','soluble','low'),
    ]

target = ('-----CUT*****CUT-----','E.Coli','high')




