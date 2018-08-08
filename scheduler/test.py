
from solver import create_optimal_schedule
from tasks import Task
from tasks import Active,Inactive,Variable


t1 = Task(timeblocks = [Active(1),Inactive(2),Active(1)])
t2 = Task(timeblocks = [Active(1),Inactive(2),Active(1)])
t3 = Task(timeblocks = [Active(1),Inactive(2),Active(1)])
t4 = Task(timeblocks = [Active(2),Inactive(2),Active(1)])
t5 = Task(timeblocks = [Active(3),Variable(), Active(3)])
t6 = Task(timeblocks = [Active(4),Inactive(1),Active(2)])
t7 = Task(timeblocks = [Active(2),Inactive(2),Active(2)])
t8 = Task(timeblocks = [Active(1),Inactive(3),Active(2)])
t9 = Task(timeblocks = [Active(1),Inactive(1),Active(1)])

tasks = [t1,t2,t3,t4,t5,t6,t7,t8,t9]

# dictionary declaring which tasks need to happen before which
## i.e. t2 needs to happen before t4 & t5

dependencies = {
        t1.name:(t4,),
        t2.name:(t4,t5),
        t3.name:(t5,),
        t4.name:(t6,),
        t5.name:(t6,),
        t5.name:(t6,),
        t6.name:(t7,t8,t9),
        }

options = {
        'worker_count': 2,
        'worker_names': ["Patrick","Patrick's Undergrad"],
        'greedy_solution': False,
        'unique_workers': True,
        }

create_optimal_schedule(tasks,dependencies,**options)

