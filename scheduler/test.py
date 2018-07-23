
from Queue import PriorityQueue
from basic_example import Active,Inactive,Variable
from basic_example import Task,Schedule

"""
PRIORITY QUEUE Classes 
"""

class MyPriorityQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item,))
        self.counter += 1

    def get(self, *args, **kwargs):
        dist,_, item = PriorityQueue.get(self, *args, **kwargs)
        return item,dist


def _is_schedule_complete(schedule):

    tp0 = schedule.timepoints.values()[0]
    tl0 = schedule.timelines.values()[0]

    tasks_complete   = schedule.task_states == schedule.max_task_states

    timepoints_equal = all(schedule.timepoints[name]  == len(schedule.timelines[name])
            for name in schedule.worker_names)
            
    timelines_equal = all(len(x) == len(tl0)
            for x in schedule.timelines.values())

    return all((tasks_complete,timepoints_equal,timelines_equal))


"""
TESTING Script
"""

task1 = Task(name = 'task_1',timeblocks = [Active(1),Inactive(2),Active(1)])
task2 = Task(name = 'task_2',timeblocks = [Active(1),Inactive(2),Active(2)])
task3 = Task(name = 'task_3',timeblocks = [Active(1),Inactive(2),Active(1)])

schedule = Schedule(worker_count = 2)

schedule.add_task(task1)
schedule.add_task(task2)
schedule.add_task(task3)


queue = MyPriorityQueue()

finished_nodes = {
        schedule.history:   schedule.get_cost()
        }

while not _is_schedule_complete(schedule): 

    for new_state in schedule.get_next_states():
       
        schedule.load_state(new_state)

        #print 'Local history:',schedule.history

    
        queue.put(new_state,schedule.get_cost())
        
    # pull next node based on priority
    current_state,current_cost = queue.get()
    schedule.load_state(current_state)
    finished_nodes[current_state['history']] = current_cost 

    '''
    print 'History:',current_state['history']
    for k,v in current_state.items():
        print ' ->',k,v
    '''

for k,v in schedule.get_state().items():
    print '>',k,':',v


    


















