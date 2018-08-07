

# standard libraries
import copy

# nonstandard libraries
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# homegrown libraries
from tasks import Task,Active

# library mods
#plt.rcParams["font.family"] = "Times New Roman"
plt.style.use('ggplot')


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
        self.task_requirements = []
        self.task_start_time = []
        self.task_map = {}
        self.history = ''

        # init dependencies between task completions
        self._dependency_map = {}

        # build a default nulltask
        self._nullblock = Task(name = 'null',timeblocks = [Active(1)])
        
        #self.create_new_schedule()

    @property
    def binary_timelines_header(self): 
        
        return [[0 if tb == None else 1 for tb in self.timelines[name][self.timepoints[name]:]] for name in self.worker_names] 

    @property
    def tag(self):

        return '{} {}'.format(
                self.timepoints.values(),
                self.task_states
                )

        '''
        return '{} {} {}'.format(
                self.timepoints.values(),
                self.task_start_time,
                self.task_states
                )
        return '{} {} {}'.format(
                self.timepoints.values(),
                self.nullblocks.values(),
                self.task_states
                )
        '''

    def __repr__(self):
        return '\n'.join(('{} - {}'.format(name,','.join((str(tb) for tb in self.timelines[name]))) for name in self.worker_names))

    def add_task(self,new_task):

        # check for name uniqueness
        if new_task in self.task_map:
            print 'New task needs unique name!'
            return None

        self.tasks += [new_task]
        self.task_states.append(0)  
        self.max_task_states = [len(task.timesections) for task in self.tasks]
        self.task_requirements.append(0)
        self.task_start_time.append(0)
        self.task_map[new_task.name] = len(self.tasks) - 1

    def add_tasks(self,*new_tasks):
        """ Add multiple tasks simultaneously """
        for new_task in new_tasks: self.add_task(new_task)

    def add_dependencies(self,graph):
        """ Add dependencies between tasks """
        
        for name,tasks in graph.items():
            source_id = self.task_map[name] # get index for source task
            # iterate through sink tasks
            self._dependency_map[source_id] = [self.task_map[task.name] 
                    if isinstance(task,Task) 
                    else task_map[task] 
                    for task in tasks]
            
            # add requirement count to task_requirements
            for sink_id in self._dependency_map[source_id]:
                self.task_requirements[sink_id] += 1


    def get_cost(self):
        return sum(self.nullblocks.values())

    def get_state(self): 
        """ Get current schedule configuration """
        return {
                'nullblocks':   self.nullblocks,
                'timepoints':   self.timepoints,
                'task_states': self.task_states,
                'task_requirements': self.task_requirements,
                'task_start_time': self.task_start_time,
                'timelines':     self.timelines,
                'history':         self.history,
                }

    def load_state(self,state):
        """ Load schedule with a particular configuration """
        self.nullblocks  =  state['nullblocks']
        self.timepoints  =  state['timepoints']
        self.task_states = state['task_states']
        self.task_requirements = state['task_requirements']
        self.task_start_time = state['task_start_time']
        self.timelines   =   state['timelines']
        self.history     =     state['history']

    def _set_available_worker_name(self):

        names = self.timepoints.keys()
        timepoints = self.timepoints.values()
        min_timepoint = min(timepoints)

        self.available_worker_name = names[timepoints.index(min_timepoint)]

        return (self.available_worker_name,min_timepoint)
        
    def _merge_worker_timeblocks(self,task_index,*timeblocks):
        """ """

        name = self.available_worker_name

        timeline = list(self.timelines[name])
        timepoint = self.timepoints[name]
        task_timeline = [tb for tb in timeblocks for _ in xrange(tb.duration)]
        duration = len(task_timeline)

        completion_time = timepoint + duration # when finished, used in dependencies 

        if len(timeline) < completion_time:
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
            # if task is completed, update requirements
            if state['task_states'][task_index] == self.max_task_states[task_index] \
                    and task_index in self._dependency_map:
                state['task_start_time'][task_index] = -1 
                # decrease task requirements if task is complete
                for sink_id in self._dependency_map[task_index]: 
                    state['task_requirements'][sink_id] += -1
                    state['task_start_time'][sink_id] = completion_time 

        return state

    def get_next_states(self):
        """ Returns a list of next states, from current """ 
        starting_state = self.get_state()             # create nullblock addition for next state
        next_states = []                              # initialize storage variable

        _,current_time = self._set_available_worker_name() # get worker with lowest timepoint

        new_state = self._merge_worker_timeblocks('null',*self._nullblock.timeblocks)
        next_states.append(new_state)

        for i,task in enumerate(self.tasks):
            
            if self.task_start_time[i] > current_time: continue # if task requirements not done
            if self.task_states[i] == self.max_task_states[i]: continue # if a task is complete
            if self.task_requirements[i] > 0: continue # if there are remaining requirements 

            timeblocks = task.timesections[self.task_states[i]] # get active timesection of task
            new_state = self._merge_worker_timeblocks(i,*timeblocks)
            
            if new_state == False: continue
            
            next_states.append(new_state)

        return next_states

    def plot(self):

        height = 0.5
        colors = ['blue','green','yellow','red','orange','purple','pink','teal','brown']

        color_map = dict([(task.name,c) for task,c in zip(self.tasks,colors)])
        ypos_map = dict([(task.name,i+1) for i,task in enumerate(self.tasks)])

        color_map['null'] = 'grey'
        ypos_map['null'] = i + 2

        fig,axes = plt.subplots(1,self.worker_count,figsize = (4*self.worker_count,4))


        for index,(name,timeline) in enumerate(self.timelines.items()):

            if self.worker_count == 1: ax = axes
            else: ax = axes[index]

            plt.sca(ax)

            plt.xlabel('Time (a.u.)')
            plt.ylabel('Available tasks')
            plt.yticks(ypos_map.values(),ypos_map.keys())

            ax.set_title('> {} <'.format(name))
            xpos = 0

            ax.set_xlim((0,max(self.timepoints.values())))
            ax.set_ylim((1 - height,i + 2 + height))

            for tb in timeline:

                if tb.type == 'active':

                    rect = Rectangle((xpos,ypos_map[tb.task] - height/2),
                        1,height,color=color_map[tb.task])
                    ax.add_patch(rect)
                    xpos += 1

        plt.show(block=False)
        raw_input('Press enter to close')
        plt.close()

        



