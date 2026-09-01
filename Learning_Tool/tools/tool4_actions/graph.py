
from platform import node
from Learning_Tool.tools.tool4_actions import edge
from tools.tool4_actions.edge import Edge
from tools.tool4_actions.action_node import action_node
from tools.tool4_actions.belief_node import belief_node
from tools.tool4_actions.reflection_node import reflection_node
from collections import defaultdict

adj_dict=defaultdict(list) #Upon addition of new edges we can append to the existing edge list correctly not replace 

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def node_creation(node_type,node_id,node_info): 
#Consider how function might behave different if a reflection entry is passed in
    if node_type == "action":
        node_object=action_node(node_id,node_info)
        return node_object
    elif node_type == "reflection":
        node_object=reflection_node(node_id,node_info)
        return node_object
    elif node_type == "belief":
        node_object=belief_node(node_id,node_info)
        return node_object
    else:
        return ("Incorrect node name entered, ps Use lowercase")

#Pass in all of that characters reflections and the reflection ID needed then iterate through that to extract which reflection_writing is needed.
def node_extraction(c_reflections,ref_id):
    for reflection in c_reflections:
        if ref_id == reflection.id:
            return reflection.Reflection_Writing

#Creation of a node of each type
musa_reflection= node_creation("reflection",2,"Musa")
friend_situation=node_creation("belief",2,"Scared to speak the truth over holding others accountable")
friend_action=node_creation("action",2,"Acknolodging to friends that i speak the truth in all situations no matter how close someone is to me")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Is hardcoded for now but can be changed after
adj_list=[[musa_reflection,friend_situation], [friend_situation,friend_action]] #used to know direction nodes are connected
node_dict=defaultdict(list) #Upon addition of new edges we can append to the existing edge list correctly not replace 
#Function to add the nodes from the defined edges
def node_dict_create(adj_list_example):
    for edge in adj_list_example:

        node_dict[(type(edge[0]).__name__,edge[0].id)].append(edge[1])
    return node_dict
#Function to create adjacency dictionary
#need combined keys creating
def edge_creation(node1,node2,info):


    new_edge=Edge((type(node1).__name__,node1.id),(type(node2).__name__,node2.id),info)
    adj_dict[type(node1).__name__,node1.id].append(new_edge)
    return new_edge


#Create an edge for musa_reflection to friend_situation
edge_creation(musa_reflection,friend_situation,"surfaced through reflection")

def reflection_workflow(reflection_id,reflections,belief,action):

    chosen_reflection=node_extraction(reflection_id,reflections)
    reflection_node=node_creation("Reflection",reflection_id,chosen_reflection)
    reflection_key=(reflection_id,"Reflection")
    node_dict[reflection_key].append(reflection_node)

    belief_node=node_creation("Belief",reflection_id,belief)
    belief_key=(reflection_id,"Belief")
    node_dict=[belief_key].append(reflection_node)
    Reflection_Belief_Edge=edge_creation(reflection_node,belief_node)

    action_node=node_creation("Action",reflection_id,action)
    node_key=(reflection_id,"Action")
    node_dict[node_key].append(belief_node)
    Belief_Action_Edge=edge_creation(belief_node,action_node)










