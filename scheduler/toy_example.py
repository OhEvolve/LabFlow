

# nonstandard libraries
import matplotlib.pyplot as plt
from graphviz import Digraph
import networkx as nx


"""
TASK Class
"""

class Task(object):

    def __init__(self,timeblocks = [],name = 'my_task'):
        
        # check that all passed timeblocks are right
        if not all((isinstance(tb,TimeBlock) for tb in timeblocks)):
            raise TypeError('Not all elements in timeblock list are timeblocks!')

        # associate each timeblock with task name
        for tb in timeblocks:
            tb.task = name

        self.timeblocks = timeblocks
        self.name = name

    def __repr__(self):
        return 'Task {} - {}'.format(self.name,','.join([str(tb) for tb in self.timeblocks]))


"""
TIMEBLOCK Classes
"""

class TimeBlock(object):

    task = 'unknown'
    type = 'unknown'

    def __init__(self,duration = 5):
        self.duration = duration 

    def __repr__(self):
        return '{}_{}'.format(self.type[0].capitalize(),self.duration)

class Active(TimeBlock):
    type = 'active'

class Inactive(TimeBlock):
    type = 'inactive'

class Variable(TimeBlock):
    type = 'variable'


"""
SCHEDULE Classes
"""

class Schedule(object):

    def __init__(self,worker_count = 2,worker_names = None):
        
        self.worker_count = worker_count
        self.worker_names = worker_names

        self.nulltask = Task(name = 'null',timeblocks = [Inactive(1)])
        
        self.create_new_schedule()

    def __repr__(self):
        return '\n'.join(('{} - {}'.format(name,','.join((str(tb) for tb in self.worker_schedule[name]))) for name in self.worker_names))

    def create_new_schedule(self):

        if self.worker_names == None:
            self.worker_names = ['worker_{}'.format(i+1) for i in xrange(self.worker_count)]

        self.worker_schedule = dict([(n,[]) for n in self.worker_names])
        self.worker_duration = dict([(n,0) for n in self.worker_names])
        self._is_worker_duration_current = dict([(n,True) for n in self.worker_names])
        self._task_names = []

    def _update_worker_durations(self):

        # iterate through workers 
        for name in self.worker_names:

            # ignore update if already current
            if self._is_worker_duration_current[name] == True:
                continue

            # calculate time for worker
            else:
                self.worker_duration[name] = sum(tb.duration for tb in self.worker_schedule[name])
                self._is_worker_duration_current[name] = True

    def get_duration(self):

        self._update_worker_durations()
        return max(self.worker_duration.values())

    def add_new_timeblock(self,new_tb):
        
        self._update_worker_durations()

        lowest_duration = float('inf')
        best_worker = None

        # add task name to list
        if not new_tb.task in self._task_names:
            self._task_names.append(new_tb.task)
        
        for name in self.worker_names:
            duration = self.worker_duration[name]
            if duration < lowest_duration: 
                best_worker,lowest_duration = name,duration

        if isinstance(new_tb,TimeBlock):
            self.worker_schedule[best_worker] += [new_tb]
        elif all((isinstance(tb,TimeBlock) for tb in new_tb)):
            self.worker_schedule[best_worker] += new_tb
        else:
            raise TypeError('Uncertain type for timeblock')

        self._is_worker_duration_current[best_worker] = False

    def plot(self):

        height = 0.5

        #color_map = dict([(n,c) for n,c in zip(self._task_names,colors)])
        xpos_map = dict([(n,i+1) for i,n in enumerate(self._task_names)])

        fig,axes = plt.subplots(len(self.worker_names),1)

        for worker_index,name in enumerate(self.worker_names):

            for tb in self.worker_schedule[name]:
                if tb.type == 'active':
                    Rectange((xpos_map[tb.task],ypos + 1 - height/2),tb.duration,height,color=color_map[tb.task])
                if tb.type == 'inactive':
                    plt.plot((xpos[tb.task]) 



task1 = Task(name = 'task_1',timeblocks = [Active(2),Inactive(3),Active(2)])
task2 = Task(name = 'task_2',timeblocks = [Active(1),Variable(), Active(1)])
nulltask = Task(name = 'null',timeblocks = [Inactive(1)])

schedule = Schedule()

schedule.add_task(nulltask.timeblocks)
schedule.add_task(task1)
schedule.add_task(task2)














