class ReflectionNode:

    def __init__(self,reflection_id,data):

        self.id= data[0]
        self.given_prompt= data[1]
        self.reflection_writing= data[2]
        self.date= data[3]
        self.source_author= data[4]
        self.media= data[5]
        self.topic_of_discussion= data[6]
        self.abstract_topic= data[7]
        self.character_referenced= data[8]

    def __repr__(self):
        return f"ReflectionNode({self.id})"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash((type(self).__name__, self.id))