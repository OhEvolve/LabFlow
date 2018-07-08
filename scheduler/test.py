
from Queue import PriorityQueue

"""
PRIORITY QUEUE Classes 
"""

class MyPriorityQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item, ))
        self.counter += 1

    def get(self, *args, **kwargs):
        dist,_, item, _ = PriorityQueue.get(self, *args, **kwargs)
        return item,dist

"""
TIMEBLOCK Classes
"""

class TimeBlock(object):

    type = 'unknown'

    def __init__(self,duration = 5):
        self.duration = duration 

    def __repr__(self):
        return '{} timeblock - {} units'.format(self.type.capitalize(),self.duration)

class Active(TimeBlock):
    type = 'active'

class Inactive(TimeBlock):
    type = 'inactive'

class Variable(TimeBlock):
    type = 'variable'

"""
TESTING Script
"""

task1 = [Active(2),Inactive(3),Active(2)]
task2 = [Active(2),Inactive(2),Active(2)]
task3 = [Active(1),Variable(),Active(1)]

tasks = [task1,task2,task3]

current_node = tuple(0 for _ in tasks)
current_distance = tuple(0 for _ in tasks)

final_node = tuple(1 + sum(isinstance(x,Variable) for x in task) for task in tasks)

queue = MyPriorityQueue()

finished_nodes = {current_node: 0}

def next_nodes(state):
    return [tuple(s2 if i != j else s2 + 1 for j,s2 in enumerate(state)) for i,s1 in enumerate(state) if s1 < final_node[i]]

def distance(current_node,next_node):
    dist = 2 
    return finished_nodes[current_node] + dist 
    


while current_node != final_node:

    print 'Current node:', current_node
    print 'Current distance:', current_distance
    
    for next_node in next_nodes(current_node):
       
        node_distance = distance(current_node,next_node)
        queue.put(next_node,node_distance)
        
    # pull next node based on priority
    current_node,current_distance = queue.get()
    finished_nodes[current_node] = current_distance

    


















