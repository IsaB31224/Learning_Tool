from db.database import get_exact_reflection

class reflection_node:

    def __init__(self,reflection_id,character_name):

        data=get_exact_reflection(character_name,reflection_id)

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
        return f"reflection_node({self.id})"