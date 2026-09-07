
from tools.tool4_actions.edge import Edge
from tools.tool4_actions.action_node import ActionNode
from tools.tool4_actions.belief_node import BeliefNode
from tools.tool4_actions.reflection_node import ReflectionNode
from collections import defaultdict

adj_dict=defaultdict(list) #Upon addition of new edges we can append to the existing edge list correctly not replace 

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def node_creation(node_type,node_id,node_info): 
#Consider how function might behave different if a reflection entry is passed in
    if node_type == "Action":
        node_object=ActionNode(node_id,node_info)
        return node_object
    elif node_type == "Reflection":
        node_object=ReflectionNode(node_id,node_info)
        return node_object
    elif node_type == "Belief":
        node_object=BeliefNode(node_id,node_info)
        return node_object
    else:
        return ("Incorrect node name entered")

#Pass in all of that characters reflections and the reflection ID needed then iterate through that to extract which reflection_writing is needed.
def node_extraction(c_reflections,ref_id):
    for reflection in c_reflections:
        if ref_id == reflection[0]:
            return reflection

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# node_dict: registry of every node, keyed by its identity (type name, id) -> the node object.
# Lets an Edge's (type, id) tuple be resolved back to a live node. One entry per node, not a list.
node_dict={}

# adj_dict: adjacency list. Key is the node object itself, value is the list of Edges going out of it.
def edge_creation(node1,node2,info=None):
    # Registers both endpoints in node_dict before connecting them, so an edge can
    # never exist without its nodes being resolvable — the caller no longer has to
    # remember a separate registration step.
    for node in (node1,node2):
        node_dict[(type(node).__name__,node.id)]=node

    new_edge=Edge((type(node1).__name__,node1.id),(type(node2).__name__,node2.id),info)
    adj_dict[node1].append(new_edge)
    return new_edge


def reflection_workflow(reflection_id,reflections,belief,action):

    chosen_reflection=node_extraction(reflections,reflection_id)
    if chosen_reflection is None:
        # No reflection with that id in this character's list — build nothing.
        return None

    reflection_node=node_creation("Reflection",reflection_id,chosen_reflection)
    belief_node=node_creation("Belief",reflection_id,belief)
    action_node=node_creation("Action",reflection_id,action)

    # Directed chain: reflection -> belief -> action. edge_creation registers both
    # endpoints in node_dict itself, so no separate registration loop is needed here.
    edge_creation(reflection_node,belief_node)
    edge_creation(belief_node,action_node)











