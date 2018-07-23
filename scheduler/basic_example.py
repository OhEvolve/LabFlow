
# standard libraries
import copy

# nonstandard libraries
import matplotlib.pyplot as plt
from graphviz import Digraph
import networkx as nx


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

    def __init__(self,timeblocks = [],name = 'my_task'):
        
        # check that all passed timeblocks are right
        if not all((isinstance(tb,TimeBlock) for tb in timeblocks)):
            raise TypeError('Not all elements in timeblock list are timeblocks!')

        # associate each timeblock with task name
        for tb in timeblocks:
            tb.task = name

        # assign basic properties
        self.timeblocks = timeblocks
        self.timesections = _make_timesections(timeblocks)
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

        if worker_names == None: 
            worker_names = ['worker_{}'.format(i+1) for i in xrange(worker_count)] 
        
        # worker properties
        self.worker_count = worker_count
        self.worker_names = worker_names

        # worker tasks
        self.tasks = []

        # state characteristics
        self.timelines  = dict([(name,[]) for name in worker_names])
        self.nullblocks = dict([(name,0)    for name in worker_names])
        self.timepoints = dict([(name,0)    for name in worker_names])
        self.task_states = []
        self.history = ''

        # build a default nulltask
        self._nullblock = Task(name = 'null',timeblocks = [Active(1)])
        
        # 
        #self.create_new_schedule()

    def __repr__(self):
        return '\n'.join(('{} - {}'.format(name,','.join((str(tb) for tb in self.timelines[name]))) for name in self.worker_names))

    def add_task(self,new_task):

        self.tasks += [new_task]
        self.task_states = [0 for _ in self.tasks]
        self.max_task_states = [len(task.timesections) for task in self.tasks]

    def get_cost(self):
        return sum(self.nullblocks.values())

    def get_state(self): 
        """ Get current schedule configuration """
        return {
                'nullblocks':   self.nullblocks,
                'timepoints':   self.timepoints,
                'task_states': self.task_states,
                'timelines':     self.timelines,
                'history':         self.history,
                }

    def load_state(self,state):
        """ Load schedule with a particular configuration """
        self.nullblocks  =  state['nullblocks']
        self.timepoints  =  state['timepoints']
        self.task_states = state['task_states']
        self.timelines   =   state['timelines']
        self.history     =     state['history']

    def _set_available_worker_name(self):

        names = self.timepoints.keys()
        timepoints = self.timepoints.values()
        min_timepoint = min(timepoints)

        self.available_worker_name = names[timepoints.index(min_timepoint)]
        
    def _merge_worker_timeblocks(self,task_index,*timeblocks):
        """ """

        name = self.available_worker_name

        timeline = list(self.timelines[name])
        timepoint = self.timepoints[name]
        task_timeline = [tb for tb in timeblocks for _ in xrange(tb.duration)]
        duration = len(task_timeline)

        if len(timeline) < timepoint + duration:
            timeline += [None for _ in xrange(timepoint + duration - len(timeline))]

        # create merged timeline object (if possible)
        for i,(moment,task_moment) in enumerate(zip(timeline[timepoint:],task_timeline)):
            if moment != None and task_moment.type == 'active': # if there is a conflict for activity times
                return False # return a failure
            elif task_moment.type == 'active':
                timeline[i + timepoint] = task_moment 

        # find the first available timeblock
        for added_moments,moment in enumerate(timeline[timepoint:]):
            if moment == None:
                break 
            else:
                timepoint += 1 

        state = copy.deepcopy(self.get_state())      # create nullblock addition for next state

        state['timelines'][name] = timeline
        state['timepoints'][name] = timepoint

        # adjust state variable
        if task_index == 'null':
            state['nullblocks'][name] += 1
            state['history'] += '-> null'
        else:
            state['task_states'][task_index] += 1
            state['history'] += '-> {}'.format(task_index)

        '''
        print 'Previous state:', state
        for k,v in self.get_state().items():
            print '>',k,v
        print 'Merged state:', state
        for k,v in state.items():
            print '>',k,v
        print '\n'
        '''

        return state

    def get_next_states(self):
        """ Returns a list of next states, from current """ 
        starting_state = self.get_state()             # create nullblock addition for next state
        next_states = []                              # initialize storage variable

        self._set_available_worker_name() # get worker with lowest timepoint

        new_state = self._merge_worker_timeblocks('null',*self._nullblock.timeblocks)
        next_states.append(new_state)

        for i,task in enumerate(self.tasks):
            
            if self.task_states[i] == self.max_task_states[i]: continue # if a task is complete

            timeblocks = task.timesections[self.task_states[i]] # get active timesection of task
            new_state = self._merge_worker_timeblocks(i,*timeblocks)
            
            if new_state == False: continue
            
            next_states.append(new_state)

        return next_states



    '''
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
    '''



if __name__ == "__main__":

    task1 = Task(name = 'task_1',timeblocks = [Active(1),Inactive(2),Active(1)])
    task2 = Task(name = 'task_2',timeblocks = [Active(1),Inactive(2),Active(2)])
    task3 = Task(name = 'task_3',timeblocks = [Active(1),Inactive(2),Active(1)])

    schedule = Schedule(workers = 1)

    schedule.add_task(task1)
    schedule.add_task(task2)
    schedule.add_task(task3)


    for i in xrange(5):
        states = schedule.get_next_states()
        schedule.load_state(states[-1])
        print schedule.history

    print schedule














