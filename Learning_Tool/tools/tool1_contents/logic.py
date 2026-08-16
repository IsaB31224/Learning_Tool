
"""
Tool 1 Window Split in to 2 windows. View Domains and Search themes

    View Domains- Consists of a tree which has a root node consisting of a domain this domain has child nodes which are the themes of the domain an eg: Financial Domain: Worries Sucess Integrity
    Search Themes- User inputs the theme they want to acess the seerah content from. The search algorithim searches for this theme in the tree of the relevant domain and then they can acess a JSON file which has the info

    How Data is stored?

    Tree Data structure can exist with root node as Domains. Its next layer can be the different domains. The following layer can be the different themes within that domain.

    How data is searched?
    Im not aware of the relevant algorithim to search through the tree will need to be learnt.

    How Seerah content is stored?
    All the seerah content for the theme is stored in a JSON file which contains the Categories to the theme, URL,Author.
    Seerah Content is stored as references to Dr Yasir Qadhis Seerah Series
    The Title of the different categories he talks about is shown with the relevant time stamps.This is sourced by using Gemini Ai youtube pulling 
    

    I need to think through the points of comparison between the user and exmplar and how i am structuring this in the tool 1 system
"""
from shared.DSA.tree import TreeNode


domain_list=["Finance","Social","Mental"]
Finance_theme_list=["Integrity","Responsobility","Provision"]
Mental_theme_list=["Contenment","Anxiety","Relief"]
Social_theme_list=["Friendship","Brotherhood"]

domain_theme_map={
    "Finance":Finance_theme_list,
    "Social":Social_theme_list,
    "Mental":Mental_theme_list,
}

parent_nodes_dict={}


# How to initialise parent and child nodes from a static data structure of lists and dictionary placing them in a dictionary which can be referenced outside the function

def add_nodes_dictionary(dictionary):

    for item in dictionary.items():

        parent=item[0]
        Parent_node=TreeNode(parent)
        parent_nodes_dict[parent]=Parent_node

        for value in item[1]:
            child_node=TreeNode(value)
            Parent_node.add_child(child_node)
    
def add_theme_to_domain(domain,theme):
    

    domain.add_child(theme)

def dfs_traversal(root):

    nodes_list=[]
    

    if root.child==[]:
        nodes_list.append(root)
    
    else:
        nodes_list.append(root)
        for node in root.child:
            caller_list=dfs_traversal(node)
            nodes_list.extend(caller_list)

    return nodes_list

def node_search(n_list,index_node): #Functions calls all traversed nodes and intended object where index_node is a string containing the node name

    for node in n_list:
        if node.theme==index_node:
            return node.text


add_nodes_dictionary(domain_theme_map)
Root_node=TreeNode("Domains")
for parent in parent_nodes_dict.values():

    Root_node.add_child(parent)


    





