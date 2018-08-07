
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
    schedule = Schedule(worker_count = 2) 
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

        print '\nIteration {}'.format(iterations)
        print 'current state:',current_state

        '''
        print 'Finished nodes:'
        for k,v in finished_nodes.items():
            print k,v
        print 'Finished edges:'
        for k,v in finished_edges.items():
            print k,v
        '''

        #print ''

        if current_tag in finished_nodes and current_cost >= finished_nodes[current_tag]:
            print 'in finished...',finished_nodes[new_tag]
            current_state,current_cost = queue.get()
            current_tag = schedule.tag(current_state)
            

        for move,new_state in schedule.get_next_states(current_state):

            print 'move/state:',move,new_state

            new_tag = schedule.tag(new_state)
            new_cost = new_state['cost']

            if new_tag in finished_nodes:
                print 'in finished...',finished_nodes[new_tag]

                existing_cost = finished_nodes[new_tag]

                if new_cost < existing_cost:
                    print 'Surpised to be here...'
                    # a new, better path to a node
                    finished_nodes[new_tag] = new_cost
                    finished_edges[new_tag] = [(move,current_tag)]
                elif new_cost == existing_cost:
                    # if as good, just add as a potential path
                    finished_edges[new_tag].append((move,current_tag))
                else:
                    # this move was less favorable than existing
                    continue
           
            # if tag hasn't been observed before
            #finished_nodes[new_tag] = new_cost
            #finished_edges[new_tag] = (move,current_tag)
            print 'adding new'
            queue.put(new_state,new_state['cost'])

        # pull next node based on priority
        last_tag = current_tag
        current_state,current_cost = queue.get()
        current_tag = schedule.tag(current_state)

        finished_nodes[current_tag] = new_cost
        finished_edges[current_tag].append((move,last_tag))
        #finished_nodes[current_tag] = current_cost 

        if iterations % 1000 == 0 and iterations != 0:

            pass
            print 'Checkpoint [{}]:'.format(iterations)
            print '>',schedule.task_start_time
            print '>',schedule.tag
            print '>',schedule.history
            print '> Timeline:',schedule.timelines
            print '> Binary timeline:',schedule.binary_timelines_header
            print '>',schedule.nullblocks.values()
            print ''

    print 'Time to completion: {}'.format(time.time() - start)    
    print 'Iterations used: {}'.format(iterations)
    print 'Ending timepoint: {}'.format(schedule.timepoints.values()[0])

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
