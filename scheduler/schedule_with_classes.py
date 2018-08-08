
# standard libraries
import copy

# nonstandard libraries
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# homegrown libraries
from tasks import Task
from tasks import Active,Inactive,Variable

# library mods
#plt.rcParams["font.family"] = "Times New Roman"
plt.style.use('ggplot')


"""
SCHEDULE Classes
"""

class Scheduler(object):

    def __init__(self,worker_count = 2,worker_names = None):

        if worker_names == None: 
            worker_names = ['worker_{}'.format(i+1) for i in xrange(worker_count)] 
        
        # worker properties
        self.worker_count = worker_count
        self.worker_names = worker_names
        self.worker_map = dict([(name,i) for i,name in enumerate(self.worker_names)])

        # task variables
        self.tasks = [] # contains 
        self.max_task_states = []
        self.max_task_requirements = []
        self.task_map = {}

        # init dependencies between task completions
        self._dependency_map = {}

        self._nullblock = Task(name = 'null',timeblocks = [Active(1)])

    def display_traits(self):
        """ Get info regarding scheduler object """
        print 'Worker count: {}'.format(self.worker_count)
        print 'Worker names : {}'.format(self.worker_names)
        print 'Tasks : {}'.format(self.tasks)
        print 'Max task states: {}'.format(self.max_task_states)
        print 'Max task requirements: {}'.format(self.max_task_requirements)


    def get_starting_state(self):
        """ """
        return {
                'task_states': [0 for _ in self.tasks],
                'cost': 0,
                'timeline_header': [[0] for _ in self.worker_names],
                'task_requirement_timer': [0 for _ in self.tasks],
                }

    def _is_schedule_complete(self,state):

        tl0 = state['timeline_header'][0]

        tasks_complete = (state['task_states'] == self.max_task_states) and \
                all((s == 0 for s in state['task_requirement_timer']))

        timelines_equal = all(len(x) == 1
                for x in state['timeline_header'])

        return all((tasks_complete,timelines_equal))

    def tag(self,state):
        """ """
        return '{} {} {}'.format(
                state['task_states'],   
                state['timeline_header'],   
                state['task_requirement_timer'],   
                )

    def add_task(self,new_task):

        # check for name uniqueness
        if new_task in self.task_map:
            print 'New task needs unique name!'
            return None

        self.tasks += [new_task]
        self.max_task_states = [len(task.timesections) for task in self.tasks]
        self.max_task_requirements.append(0)
        self.task_map[new_task.name] = len(self.tasks) - 1

    def add_tasks(self,*new_tasks):
        """ Add multiple tasks simultaneously """
        for new_task in new_tasks: 
            self.add_task(new_task)

    def add_dependencies(self,graph):
        """ Add dependencies between tasks """
        self._dependency_map = dict([(i,[]) for i in xrange(len(self.tasks))])
        
        for name,tasks in graph.items():
            source_id = self.task_map[name] # get index for source task
            # iterate through sink tasks
            self._dependency_map[source_id] = [self.task_map[task.name] 
                    if isinstance(task,Task) 
                    else task_map[task] 
                    for task in tasks]
            
            # add requirement count to task_requirements
            for sink_id in self._dependency_map[source_id]:
                self.max_task_requirements[sink_id] += 1

    def get_next_states(self,state):

        """ Returns a list of next states, from input state """ 

        # initialize next states
        next_states = []

        # transfer state variables to local
        task_states = state['task_states']
        cost = state['cost']
        timeline_header = state['timeline_header']
        task_requirement_timer = state['task_requirement_timer']

        # transfer class variables to local
        max_task_states = self.max_task_states
        max_task_requirements = self.max_task_requirements

        # see which tasks have met their requirements
        # note: by requirements, it is listing the # of tasks that have been ATLEAST started
        task_requirements = [0 for _ in self.tasks]

        for i,(task_state,max_task_state) in enumerate(zip(task_states,max_task_states)):

            if task_state != max_task_state: continue

            for sink_id in self._dependency_map[i]:
                task_requirements[sink_id] += 1

        # get worker with lowest timepoint
        worker_index = _get_available_worker_from_header(timeline_header) 

        merged_header = _merge_header_with_timeblocks(timeline_header,[1])
        merged_header,merged_requirement_timer = _reduce_header_with_timer(
                merged_header,task_requirement_timer)

        next_states.append(('null',{
                'task_states': task_states, 
                'cost': cost + 1,
                'timeline_header': merged_header,
                'task_requirement_timer': merged_requirement_timer,
            }))

        for i,task in enumerate(self.tasks):
            
            if task_states[i] == max_task_states[i]: 
                continue # if a task is complete
            if task_requirement_timer[i] > 0: 
                continue # if there are remaining requirements that are pending
            if task_requirements[i] != max_task_requirements[i]: 
                continue # if there are remaining requirements 
            
            dependencies = [i] + self._dependency_map[i]

            binary_timeblocks = task.binary_timesections[task_states[i]]
            new_task_requirement_timer = [req if not i_req in dependencies else max(req,len(binary_timeblocks))
                    for i_req,req in enumerate(task_requirement_timer)]


            merged_header = _merge_header_with_timeblocks(timeline_header,binary_timeblocks)

            if merged_header == False: 
                continue

            merged_header,merged_requirement_timer = _reduce_header_with_timer(
                    merged_header,new_task_requirement_timer)
            

            next_states.append((i,{
                    'task_states': [ts if i_ts != i else ts+1 for i_ts,ts in enumerate(task_states)],
                    'cost': cost,
                    'timeline_header': merged_header,
                    'task_requirement_timer': merged_requirement_timer,
                }))

        return next_states

    def _set_available_worker_name(self):

        names = self.timelines.keys()
        timepoints = [tl.index(None) for tl in self.timelines.values()]
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

        self.timelines[name] = timeline
        self.timepoints[name] = timepoint

        # adjust state variable
        if task_index == 'null':
            self.nullblocks[name] += 1
        else:
            self.task_states[task_index] += 1
            # if task is completed, update requirements
            if self.task_states[task_index] == self.max_task_states[task_index] \
                    and task_index in self._dependency_map:
                self.task_start_time[task_index] = -1 
                # decrease task requirements if task is complete
                for sink_id in self._dependency_map[task_index]: 
                    self.task_requirements[sink_id] += -1
                    self.task_start_time[sink_id] = completion_time 

        
    def view(self,progression):
        """ View a choice progression """

        # initialize some variables
        self.timelines  = dict([(name,[None]) for name in self.worker_names])
        task_states = [0 for _ in self.tasks]  

        # iterate through move choices
        for move in progression:

            name,current_time = self._set_available_worker_name() # get worker with lowest timepoint

            # decide what the next timeblocks are going to be
            if move == 'null':
                timeblocks = self._nullblock.timeblocks
            else:
                task = self.tasks[move]
                timeblocks = task.timesections[task_states[move]]
            
            add_timer = 0

            for tb in timeblocks:
                # skip if inactive time
                if tb.type == 'inactive': continue
                # otherwise, replace None with activity
                for _ in xrange(tb.duration):
                    try:
                        self.timelines[name][current_time + add_timer] = tb
                    except IndexError:
                        self.timelines[name] += [tb]
                    add_timer += 1

                if self.timelines[name][-1] != None:
                    self.timelines[name] += [None]

        for name,tl in self.timelines.items():
            self.timelines[name] = tl[:-1]

        self._plot()

    def _plot(self):


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

            ax.set_xlim((0,max([len(tl) for tl in self.timelines.values()])))
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

"""
HELPER FUNCTIONS
"""

def _get_available_worker_from_header(timeline_header):
    """ Get the index of the available worker """
    for index,header in enumerate(timeline_header):
        if header[0] == 0:
            return index 
    return None


def _merge_header_with_timeblocks(timeline_header,timesection):
    """ Header """

    worker_index = _get_available_worker_from_header(timeline_header) 

    buffer_len = len(timesection) - len(timeline_header[worker_index]) 

    new_timeline_header = [header[:] + [0 for _ in xrange(buffer_len)] 
        if index == worker_index else header[:] 
        for index,header in enumerate(timeline_header)]

    for i,(a,b) in enumerate(zip(timesection,new_timeline_header[worker_index])):
        if a and b: return False
        new_timeline_header[worker_index][i] = a or b

    new_timeline_header[worker_index] += [0]
    
    return new_timeline_header


def _reduce_header_with_timer(timeline_header,reqs):
    # WILL NEED EXCEPTION CATCHING
    for index in xrange(max((len(header) for header in timeline_header))):
        if any([header[index] == 0 for header in timeline_header]): break

    for ind,header in enumerate(timeline_header):
        for i in xrange(1,len(header)+1):
            if header[-i] == 1:
                timeline_header[ind] = header[index:len(header)-i+2]
                break

    return timeline_header,[max(0,r - index) for r in reqs]





if __name__ == "__main__":

    # this is a declaration of tasks with different blocks of active/inactive time
    t1 = Task(timeblocks = [Active(1),Inactive(2),Active(1)])
    t2 = Task(timeblocks = [Active(1),Inactive(2),Active(2)])
    t3 = Task(timeblocks = [Active(1),Inactive(2),Active(1)])
    t4 = Task(timeblocks = [Active(2),Inactive(2),Active(1)])
    t5 = Task(timeblocks = [Active(3),Variable(), Active(3)])
    t6 = Task(timeblocks = [Active(4),Inactive(1),Active(2)])
    t7 = Task(timeblocks = [Active(2),Inactive(2),Active(2)])
    t8 = Task(timeblocks = [Active(1),Inactive(3),Active(2)])
    t9 = Task(timeblocks = [Active(1),Inactive(1),Active(1)])

    # dictionary declaring which tasks need to happen before which
    ## i.e. t2 needs to happen before t4 & t5
    graph = {
            t1.name:(t4,),
            t2.name:(t4,t5),
            t3.name:(t5,),
            t4.name:(t6,),
            t5.name:(t6,),
            t5.name:(t6,),
            t6.name:(t7,t8,t9),
            }

    # create schedule, with any number of workers
    # be aware time scaling is rough as you increase
    scheduler = QuickScheduler(worker_count = 2) 
    scheduler.add_tasks(t1,t2,t3,t4,t5,t6,t7,t8,t9) # add tasks to your schedule
    scheduler.add_dependencies(graph) # add dependencies between tasks

    #scheduler.display_traits()

    state = scheduler.get_starting_state()
    next_states = scheduler.get_next_states(state)















