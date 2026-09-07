
class BeliefNode:

    def __init__(self,id,belief):

        self.id=id
        self.belief=belief

    def edit_belief(self,new_belief):
        self.belief = new_belief

    def return_belief(self):
        return self.belief

    def __repr__(self):
        return f"BeliefNode({self.id})"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash((type(self).__name__, self.id))