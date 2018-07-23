
from Queue import PriorityQueue

from tasks import Task
from tasks import Active,Inactive,Variable

from schedule import Schedule


"""
Main testing
"""
def main():

    # this is a declaration of tasks with different blocks of active/inactive time
    t1 = Task(timeblocks = [Active(1),Inactive(2),Active(1)])
    t2 = Task(timeblocks = [Active(1),Inactive(2),Active(2)])
    t3 = Task(timeblocks = [Active(1),Inactive(2),Active(1)])
    t4 = Task(timeblocks = [Active(2),Inactive(2),Active(1)])
    t5 = Task(timeblocks = [Active(3),Variable(),Active(3)])
    t6 = Task(timeblocks = [Active(4),Inactive(1),Active(2)])

    # dictionary declaring which tasks need to happen before which
    ## i.e. t2 needs to happen before t4 & t5
    graph = {
            t1.name:(t4,),
            t2.name:(t4,t5),
            t3.name:(t5,),
            t4.name:(t6,),
            t5.name:(t6,),
            }

    # create schedule, with any number of workers
    # be aware time scaling is rough as you increase
    schedule = Schedule(worker_count = 1) 

    schedule.add_tasks(t1,t2,t3,t4,t5,t6) # add tasks to your schedule

    schedule.add_dependencies(graph) # add dependencies between tasks


    ### BORING ALGORITHMIC CODE ###
    ### DON'T LOOK HERE IF YOU WANT TO THINK ABOUT THIS PROBLEM WITHOUT BIAS ###
    ### THAT MEANS YOU JOSEPH ###

    queue = MyPriorityQueue()

    finished_nodes = {
            schedule.history:   schedule.get_cost()
            }

    while not _is_schedule_complete(schedule): 

        for new_state in schedule.get_next_states():
           
            schedule.load_state(new_state)
            queue.put(new_state,schedule.get_cost())
            
        # pull next node based on priority
        current_state,current_cost = queue.get()
        schedule.load_state(current_state)
        finished_nodes[current_state['history']] = current_cost 

    schedule.plot()

        





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

if __name__ == "__main__":
    main()
