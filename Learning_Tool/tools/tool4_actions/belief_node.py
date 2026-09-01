
class belief_node:

    def __init__(self,id,belief):

        self.id=id
        self.belief=belief

    def edit_belief(self,new_belief):
        self.belief = new_belief

    def return_belief(self):
        return self.belief

    def __repr__(self):
        return f"belief_node({self.id})"