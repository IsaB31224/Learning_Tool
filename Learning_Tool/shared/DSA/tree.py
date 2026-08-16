
class TreeNode: #themes in a domain


    def __init__(self,theme) -> None:

        self.theme= theme
        self.child=[]
        self.parent=None
        self.text=""

        pass

    def add_child(self,child):

        self.child.append(child)
        child.parent=self

    def is_leaf(self):

        if self.child == []:
            return ("{self} has no themes attached")
    def is_root(self):

        if self.parent == None:
            return (f"{self} has no Domain")

        



       