

# nonstandard libraries
import matplotlib.pyplot as plt
from graphviz import Digraph
import networkx as nx

def node_converter(t):
    """ Converts node tuple to string """
    return tuple_to_string(t)

def edge_converter(ts):
    """ Converts edge tuple of tuples to tuple of strings """
    return tuple((tuple_to_string(t) for t in ts))

def tuple_to_string(t):
    return ', '.join((e if e != None else 'Any' for e in t))

class Network(object):

    def __init__(self):

        self.Graph = nx.MultiDiGraph()
        self.Flowchart = Digraph('protocol_options', filename='protocol_options.gv')

        self.Flowchart.attr(rankdir='LR', size='8,5')
        self.Flowchart.attr('node', shape='circle')

        self.all_nodes  = []
        self.all_edges  = []

        self.silent = True

    def _add_graph_edge(self,new_edge,**kwargs):
        self.Graph.add_edge(*new_edge)

    def _add_flowchart_edge(self,new_edge,**kwargs):
        self.Flowchart.edge(str(new_edge[0]),str(new_edge[1]),**kwargs)

    def add_node(self,new_node):

        if new_node in self.all_nodes:
            return False

        self.all_nodes.append(new_node)
        #self.Graph.add_node(str(new_node))
        #self.Flowchart.node(str(new_node))

        return True

    def add_nodes(self,new_nodes):

        count = 0
       
        for new_node in new_nodes:
            if self.add_node(new_node):
                count += 1

        if not self.silent: print 'Added {} nodes!'.format(count)

        return bool(count)

    def add_edge(self,new_edge,label=None):
    
        if new_edge in self.all_edges:
            return False

        self.all_edges.append((new_edge,label))
        self.add_nodes(new_edge)
        self._add_graph_edge(new_edge)
        self._add_flowchart_edge(new_edge,label=label)

        return True

    def add_edges(self,new_edges,label=None):

        count = 0
       
        for new_edge in new_edges:
            if self.add_edge(new_edge,label=label):
                count += 1

        if not self.silent: print 'Added {} edges!'.format(count)

        return bool(count)

    def display_flowchart(self):
        self.Flowchart.view()

    def display_graph(self):
        print self.Graph.nodes()
        print self.Graph.edges()
        nx.draw(self.Graph)
        plt.show(block=False)
        raw_input('Press enter to close...')
        plt.close()


