

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

class QuickScheduler(object):

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

        timelines_equal = all(len(x) == len(tl0)
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
        for new_task in new_tasks: self.add_task(new_task)

    def add_dependencies(self,graph):
        """ Add dependencies between tasks """
        self._dependency_map = {}
        
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
        
        print 'Task states',task_states
        print 'Max states',max_task_states
        print 'Req',task_requirements
        print 'Max req',max_task_requirements

        print 'Timer:',task_requirement_timer

        for i,task in enumerate(self.tasks):
            print '\nTask {}'.format(i)
            
            if task_states[i] == max_task_states[i]: 
                print 'case 1'
                continue # if a task is complete
            if task_requirement_timer[i] > 0: 
                print 'case 2'
                continue # if there are remaining requirements that are pending
            if task_requirements[i] != max_task_requirements[i]: 
                print 'case 3'
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















