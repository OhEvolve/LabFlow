
# standard libraries
import time 

# nonstandard libraries

# homegrown libraries
from Queue import PriorityQueue
#from schedule import ScheduleViewer

from tasks import Task
from tasks import Active,Inactive,Variable
from schedule_with_classes import Scheduler as Schedule

"""
NOTES:
    Want to implement step/class solution
        Find equivilence classes of solutions

    Check if tag is already stored Mm...  Tag consists of:
            set(timepoints - min(timepoints))
        Number of timeblocks accepted 'til this point
"""

"""
Main testing
"""

finished_nodes = {}
finished_edges = {}


def _get_progression(current_tag,finished_edges):

    action_order = []

    while current_tag in finished_edges:
        (move,previous_tag) = finished_edges[current_tag][0]
        #action_order.append('{} ({})'.format(move,len(finished_edges[current_tag])))
        action_order.append(move)
        current_tag = previous_tag

    return action_order[::-1]


def main():

    start = time.time()

    schedule = Schedule(worker_count = 1) 

    # this is a declaration of tasks with different blocks of active/inactive time

    """#
    t1 = Task(timeblocks = [Active(2)])
    t2 = Task(timeblocks = [Active(2)])
    t3 = Task(timeblocks = [Active(2)])
    
    graph = {
            t1.name:(t3,),
            t2.name:(t3,),
            }

    schedule.add_tasks(t1,t2,t3) # add tasks to your schedule
    #"""

    #"""#
    t1 = Task(timeblocks = [Active(1),Inactive(2),Active(1)])
    t2 = Task(timeblocks = [Active(1),Inactive(2),Active(1)])
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
    schedule.add_tasks(t1,t2,t3,t4,t5,t6,t7,t8,t9) # add tasks to your schedule

    # create schedule, with any number of workers
    # be aware time scaling is rough as you increase
    schedule.add_dependencies(graph) # add dependencies between tasks

    queue = MyPriorityQueue()
    
    current_state = schedule.get_starting_state()
    current_cost = current_state['cost']
    current_tag = schedule.tag(current_state)
    previous_tag = None

    iterations = 0

    ### Function to check for exisiting tag

    """ Create a function that uses some of the local dictionaries """
    def _is_existing_tag(current_tag,move,new_state):

        new_tag = schedule.tag(new_state)

        if not new_tag in finished_nodes:
            return False

        new_cost = new_state['cost']
        existing_cost = finished_nodes[new_tag]

        if new_cost < existing_cost:
            raw_input('Surpised to be here...')
            # a new, better path to a node
            finished_nodes[new_tag] = new_cost
            finished_edges[new_tag] = [(move,current_tag)]

        elif new_cost == existing_cost:
            # if as good, just add as a potential path
            finished_edges[new_tag].append((move,current_tag))

        else:
            # this move was less favorable than existing
            pass
        return True

    ###
    ###

    # Main loop iterating over the growing graph structure
    
    while not schedule._is_schedule_complete(current_state): 

        iterations += 1 # add to counter
        
        if previous_tag != None and _is_existing_tag(previous_tag,move,current_state):

            last_tag = current_tag
            (previous_state,current_state,move),current_cost = queue.get()
            previous_tag = schedule.tag(previous_state)
            current_tag = schedule.tag(current_state)

            continue # return to next item in queue

        finished_nodes[current_tag] = current_cost # add node that doesn't exist

        if iterations != 1: # if we are not on the first node
            finished_edges[current_tag] = [(move,previous_tag)]

        for move,new_state in schedule.get_next_states(current_state):

            new_tag = schedule.tag(new_state)
            new_cost = new_state['cost']

            if _is_existing_tag(current_tag,move,new_state):
                continue

            # if tag hasn't been observed before
            queue.put((current_state,new_state,move),new_state['cost'])
           
        # pull next node based on priority
        last_tag = current_tag
        (previous_state,current_state,move),current_cost = queue.get()
        previous_tag = schedule.tag(previous_state)
        current_tag  = schedule.tag(current_state)

        if iterations % 1000 == 0 and iterations != 0:

            print 'Checkpoint [{}]:'.format(iterations)
            print '> Cost:',finished_nodes[previous_tag]
            print '> Tag:',previous_tag
            print ''

    # final addition of last node/edge
    finished_nodes[current_tag] = current_cost 
    finished_edges[current_tag] = [(move,previous_tag)]

    progression = _get_progression(current_tag,finished_edges)

    print 'Time to completion: {}'.format(time.time() - start)    
    print 'Iterations used: {}'.format(iterations)

    action_order = []

    print 'Passing checks:', schedule._is_schedule_complete(current_state)
    print 'Final state:'
    for k,v in current_state.items():
        print '> {}: {}'.format(k,v)
    print 'Final tag:',current_tag
    print 'Final progression:',progression
    print 'Number of finished nodes:',len(finished_nodes)
    print 'Number of finished edges:',len(finished_edges)

    schedule.view(progression) 

    #viewer = ScheduleViewer(schedule)
    #viewer.plot(progression)






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
        if self.empty():
            print 'QUEUE DEPLETED!'
            return False
        dist,_, item = PriorityQueue.get(self, *args, **kwargs)
        return item,dist



if __name__ == "__main__":
    main()
