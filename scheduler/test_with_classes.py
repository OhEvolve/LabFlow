
# standard libraries
import time 

# nonstandard libraries

# homegrown libraries
from Queue import PriorityQueue

from tasks import Task
from tasks import Active,Inactive,Variable
from schedule_with_classes import QuickScheduler as Schedule

"""
NOTES:
    Want to implement step/class solution
        Find equivilence classes of solutions

    Check if tag is already stored
        Mm... 
        Tag consists of:
            set(timepoints - min(timepoints))
        Number of timeblocks accepted 'til this point
"""

"""
Main testing
"""

def _get_progression(current_tag,finished_edges):

    action_order = []

    while current_tag in finished_edges:
        (move,previous_tag) = finished_edges[current_tag][0]
        action_order.append(move)
        current_tag = previous_tag

    return action_order[::-1]


def main():

    start = time.time()

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
    schedule = Schedule(worker_count = 3) 
    schedule.add_tasks(t1,t2,t3,t4,t5,t6,t7,t8,t9) # add tasks to your schedule
    schedule.add_dependencies(graph) # add dependencies between tasks

    queue = MyPriorityQueue()
    
    current_state = schedule.get_starting_state()
    current_cost = current_state['cost']
    current_tag = schedule.tag(current_state)

    finished_nodes = {
            schedule.tag(current_state): 0,
            }

    finished_edges = {}

    iterations = 0

    while not schedule._is_schedule_complete(current_state): 
        #time.sleep(0.5)
        #raw_input('hold')

        iterations += 1 # add to counter

        finished_nodes[current_tag] = current_cost 
        if iterations != 1: # if we are not on the first node
            finished_edges[current_tag] = [(move,previous_tag)]

        #print '\nCurrent state:',current_state

        for move,new_state in schedule.get_next_states(current_state):

            #print 'New state:',move,new_state

            new_tag = schedule.tag(new_state)
            new_cost = new_state['cost']

            #if new_tag in tested_nodes:
            #    continue

            if new_tag in finished_nodes:
                #print 'in finished...',finished_nodes[new_tag]

                existing_cost = finished_nodes[new_tag]

                if new_cost < existing_cost:
                    raw_input('Surpised to be here...')
                    # a new, better path to a node
                    finished_nodes[new_tag] = new_cost
                    finished_edges[new_tag] = [(move,current_tag)]
                    continue
                elif new_cost == existing_cost:
                    # if as good, just add as a potential path
                    finished_edges[new_tag].append((move,current_tag))
                    print 'it exists!'
                    continue
                else:
                    # this move was less favorable than existing
                    print '-------------------------------------------------------------'
                    print 'Current state:',current_state,'\n'
                    print 'Current progression:',_get_progression(current_tag,finished_edges),'\n'
                    print 'State:',new_state,'\n'
                    print 'Move:',move
                    print 'Progression:',_get_progression(new_tag,finished_edges),'\n'
                    print 'Existing vs. new:',existing_cost,'|',new_cost,'\n'
                    print '-------------------------------------------------------------'
                    print ''
                    raw_input()
                    continue
           
            # if tag hasn't been observed before
            #finished_nodes[new_tag] = new_cost
            #finished_edges[new_tag] = (move,current_tag)
            queue.put((current_state,new_state,move),new_state['cost'])

        # pull next node based on priority
        last_tag = current_tag
        (previous_state,current_state,move),current_cost = queue.get()
        previous_tag = schedule.tag(previous_state)
        current_tag = schedule.tag(current_state)

        if iterations % 1000 == 0 and iterations != 0:

            print 'Checkpoint [{}]:'.format(iterations)
            print '> Cost:',finished_nodes[previous_tag]
            print '> Tag:',previous_tag
            print ''

    # final addition of last node/edge
    finished_nodes[current_tag] = current_cost 
    finished_edges[current_tag] = [(move,previous_tag)]

    print 'Time to completion: {}'.format(time.time() - start)    
    print 'Iterations used: {}'.format(iterations)

    action_order = []

    _get_progression(current_tag,finished_edges)



    #schedule.plot()






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
