
class action_node:

    def __init__(self,id,action):

        self.id=id
        self.action=action

    def edit_action(self,new_action):
        self.action= new_action

    def return_action(self):
        return self.action

    def __repr__(self):
        return f"action_node({self.id})"