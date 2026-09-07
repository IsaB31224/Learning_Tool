
class ActionNode:

    def __init__(self,id,action):

        self.id=id
        self.action=action

    def edit_action(self,new_action):
        self.action= new_action

    def return_action(self):
        return self.action

    def __repr__(self):
        return f"ActionNode({self.id})"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash((type(self).__name__, self.id))