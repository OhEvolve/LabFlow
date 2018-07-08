
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

from template import Template

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
    input_template = Template(no_input = True)
    output_template = Template(type = 'DNA', shape = 'linear', length = 'short')

class GBlockSynthesis(Operation):

    name = 'GBlock Synthesis'
    input_template = Template(no_input = True)
    output_template = Template(type = 'DNA', shape = 'linear', length = 'long')

class Ligate(Operation):

    name = 'Ligate'
    input_template = Template(type = 'DNA', shape = 'linear')
    output_template = Template(type = 'DNA', shape = 'circular', concentration = 'low')

class Gibson(Operation):

    name = 'Gibson Assembly'
    input_template = Template(type = 'DNA', shape = 'linear')
    output_template = Template(type = 'DNA', shape = 'circular', concentration = 'low')

class Transform(Operation):

    name = 'Transform'
    input_template = Template(type = 'DNA', shape = 'circular')
    output_template = Template(type = 'E.Coli', concentration = 'low')

class BacterialOutgrowth(Operation):

    name = 'Bacterial Outgrowth'
    input_template = Template(type = 'E.Coli', concentration = 'low')
    output_template = Template(type = 'E.Coli', concentration = 'high')

class YeastOutgrowth(Operation):

    name = 'Yeast Outgrowth'
    input_template = Template(type = 'Yeast', concentration = 'low')
    output_template = Template(type = 'Yeast', concentration = 'high')

class Miniprep(Operation):

    name = 'Miniprep'
    input_template = Template(type = 'E.Coli', concentration = 'high')
    output_template = Template(type = 'DNA', shape = 'circular', concentration = 'high')

class Quikchange(Operation):

    name = 'Quikchange'
    input_template = Template(type = 'DNA', shape = 'circular')
    output_template = Template(type = 'DNA', shape = 'circular', concentration = 'low')

class SangerSequence(Operation):

    name = 'Sanger Sequencing'
    input_template = (Template(type = 'DNA', shape = 'circular'),Template(type = 'DNA', shape = 'linear', length = 'short'))
    output_template = Template(type = 'Data')

class Electroporation(Operation):

    name = 'Electroporation'
    input_template = Template(type = 'DNA', shape = 'circular', concentration = 'high')
    output_template = Template(type = 'Yeast', concentration = 'low')

class AffinityMaturation(Operation):

    name = 'Affinity Maturation'
    input_template = Template(type = 'Yeast', concentration = 'high')
    output_template = Template(type = 'Yeast', concentration = 'low')

class Zymoprep(Operation):

    name = 'Zymoprep'
    input_template = Template(type = 'Yeast', concentration = 'high')
    output_template = Template(type = 'DNA', shape = 'circular', concentration = 'low')

def get_default_operations():
    return [
            OligoSynthesis,
            GBlockSynthesis,
            Ligate,
            Gibson,
            Transform,
            BacterialOutgrowth,
            YeastOutgrowth,
            Miniprep,
            Quikchange,
            SangerSequence,
            Electroporation,
            Zymoprep,
            AffinityMaturation,
           ]


start_samples = [
    ('CUT----------CUT','linear','soluble','low'),
    ('CUT*****CUT','linear','soluble','low'),
    ]

target = ('-----CUT*****CUT-----','E.Coli','high')




