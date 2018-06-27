

# standard libraries
import sys

# nonstandard libraries
import matplotlib.pyplot as plt
from graphviz import Digraph

# homegrown libraries
import operations as op

max_iterations = 10

def add_node 

def node_match(n1,n2):
    """ Checks to see if two nodes match """
    for e1,e2 in zip(n1,n2):

        if e1 == None or e2 == None:
            continue

        if e1 != e2:
            return False

    return True

def build_edge(operation,nodes):
    """ Decides whether to add a new node using operation """

    all_edges = []

    for _input in operation.input_template:

        for node in nodes:

            if node_match(node,_input):
                for _output in operation.output_template:
                    all_edges.append((node,_output))
                break 

    if len(all_edges) == len(operation.input_template):
        return all_edges
    else:
        return False

def main():

    current_nodes = [('*','*','*','*')]
    current_edges = []

    f = Digraph('protocol_options', filename='fsm.gv')

    f.attr(rankdir='LR', size='8,5')

    f.attr('node', shape='circle')

    for node in current_nodes:
        f.node(str(node))

    operations = op.get_default_operations()

    for iteration in xrange(max_iterations):

        print 'Current nodes:',current_nodes
        print 'Current edges:',current_edges

        total_additions = 0

        for operation in operations:

            new_edges = build_edge(operation,current_nodes)

            print 'New edge:',new_edges

            if not new_edges:
                continue

            for new_edge in new_edges:
                if not new_edge in current_edges:
                    f.edge(*new_edge,label=operation.name)
                    current_edges.append(new_edge)
                    current_nodes.append(new_edge[1])
                    #f.edge('LR_0', 'LR_2', label='SS(B)')
                    total_additions += 1

        if total_additions == 0:
            break

    f.view()

    plt.show(block=False)
    raw_input('Press enter to close...')
    plt.close()

if __name__ == "__main__":
    main()


