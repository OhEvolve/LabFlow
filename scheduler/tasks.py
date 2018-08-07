

"""
TASK Class
"""

def _make_timesections(tbs):
    """ Breaks list of timeblocks into sections (divided by variable) """
    sections,sub = [],[]

    for tb in tbs:
        if tb.type == 'variable':
            sections.append(sub) 
            sub = []
        else:
            sub.append(tb)

    sections.append(sub) 
    return sections 

class Task(object):

    counter = 1

    def __init__(self,timeblocks = [],name = None):
        
        # check that all passed timeblocks are right
        if not all((isinstance(tb,TimeBlock) for tb in timeblocks)):
            raise TypeError('Not all elements in timeblock list are timeblocks!')

        if name == None:
            name = 'task_{}'.format(self.counter)

        # associate each timeblock with task name
        for tb in timeblocks:
            tb.task = name

        # assign basic properties
        self.timeblocks = timeblocks
        self.timesections = _make_timesections(timeblocks)
        self.binary_timesections = [[1 if tb.type == 'active' else 0 for tb in ts for _ in xrange(tb.duration)] for ts in self.timesections]
        self.name = name

        Task.counter += 1

    def __repr__(self):
        return 'Task {} - {}'.format(self.name,','.join([str(tb) for tb in self.timeblocks]))


"""
TIMEBLOCK Classes
"""

class TimeBlock(object):

    task = 'unknown'
    type = 'unknown'

    def __init__(self,duration = 1):
        self.duration = duration 

    def __repr__(self):
        return '{}_{}'.format(self.task[0] + self.task[-1].capitalize(),self.duration)

class Active(TimeBlock):
    type = 'active'

class Inactive(TimeBlock):
    type = 'inactive'

class Variable(TimeBlock):
    type = 'variable'










