

# standard libraries
import copy

# nonstandard libraries
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# homegrown libraries
from tasks import Task,Active
from schedule_with_classes import Scheduler as Schedule

# library mods
#plt.rcParams["font.family"] = "Times New Roman"
plt.style.use('ggplot')


"""
SCHEDULE Classes
"""

class ScheduleViewer(Schedule):

    def __init__(self,schedule):

        if not isinstance(schedule,Schedule):
            raise TypeError('Need to import schedule object')

        # load attributes
        self.worker_count = schedule.worker_count
        self.worker_names = schedule.worker_names
        
        # state characteristics
        self.tasks = []
        self.timelines  = dict([(name,[]) for name in self.worker_names])
        self.nullblocks = dict([(name,0)    for name in self.worker_names])
        self.timepoints = dict([(name,0)    for name in self.worker_names])
        self.task_states = []
        self.task_requirements = []
        self.task_start_time = []
        self.task_map = {}

        # init dependencies between task completions
        self._dependency_map = {}

        # build a default nulltask
        self._nullblock = Task(name = 'null',timeblocks = [Active(1)])
        
        # load existing tasks
        self.add_tasks(*schedule.tasks)

        #self.create_new_schedule()

    def __repr__(self):
        return '\n'.join(('{} - {}'.format(name,','.join((str(tb) for tb in self.timelines[name]))) for name in self.worker_names))

    """ Overwrite existing definition """
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

    #"""





    #"""

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


    def _set_available_worker_name(self):

        names = self.timepoints.keys()
        timepoints = self.timepoints.values()
        min_timepoint = min(timepoints)
        self.available_worker_name = names[timepoints.index(min_timepoint)]

        return (self.available_worker_name,min_timepoint)


    def plot(self,progression):

        for move in progression:

            _,current_time = self._set_available_worker_name() # get worker with lowest timepoint

            if move == 'null':
                new_state = self._merge_worker_timeblocks('null',*self._nullblock.timeblocks)
            else:
                task = self.tasks[move]
                timeblocks = task.timesections[self.task_states[move]]
                new_state = self._merge_worker_timeblocks(move,*timeblocks)

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

        



