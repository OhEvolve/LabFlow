
from itertools import combinations
from template import Template
from network import Network
import operations as op

def main():

    max_iterations = 10
    operations = op.get_default_operations()

    network = Network()
    network.add_node(Template(no_input = True))


    for iteration in xrange(max_iterations):

        #print 'Current nodes:',network.all_nodes
        #print 'Current edges:',network.all_edges
        #print 'Iteration {}'.format(iteration)

        additions = 0 # determines if nothing is growing

        for operation in operations:

            new_edges = build_edge(operation,network.all_nodes,network.all_edges)

            if not new_edges:
                continue

            if network.add_edges(new_edges,operation.name):
                additions = 1

        if additions == 0:
            break

    network.display_flowchart()
    #network.display_graph()

def build_edge(operation,existing_nodes,existing_edges):

    """ Decides whether to add a new node using operation """

    all_edges = []

    # get operation's input/output nodes
    input_nodes  = iterate_template(operation.input_template)
    output_nodes = iterate_template(operation.output_template)

    # get possible input/output nodes
    potential_input_nodes = [
            node for node in existing_nodes if node in input_nodes]
    potential_output_nodes = [
            node for node in existing_nodes if node in output_nodes] + list(output_nodes)

    # create all possible subsets of nodes
    potential_input_node_combos = list(combinations(potential_input_nodes, len(input_nodes)))
    potential_output_node_combos = list(combinations(potential_output_nodes, len(output_nodes)))

    for input_node_combo in potential_input_node_combos:

        if not all((input_node in input_node_combo for input_node in input_nodes)):
            continue
            
        for output_node_combo in potential_output_node_combos:
            
            if not all((output_node in output_node_combo for output_node in output_nodes)):
                continue

            potential_edges = list((i,o) for i in input_node_combo for o in output_node_combo)

            if all(((potential_edge,operation.name) in existing_edges 
                                for potential_edge in potential_edges)):
                continue

            return [potential_edge for potential_edge in potential_edges 
                    if not (potential_edge,operation.name) in existing_edges]
            


def iterate_template(obj):
    """ Get inputs as iterable """
    if isinstance(obj,Template):
        return (obj,)
    else:
        return obj


def node_match(n1,n2):
    """ Checks to see if two nodes match """
    for e1,e2 in zip(n1,n2):

        if e1 == None or e2 == None:
            continue

        if e1 != e2:
            return False

    return True

if __name__ == "__main__":
    main()
