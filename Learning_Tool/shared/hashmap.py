from db.database import get_all_character, get_character_name

class HashMap:

    def __init__(self):
        self.array_length = 9999
        self.array = [None] * self.array_length

    def hash_formula(self, string): # provides array index value for a character referenced
        total = 0 # overall value
        num = len(string)
        mod_number = 10**9 + 7  # 1_000_000_007

        for char in string: # each character
            temp = ord(char) * pow(31, num - 1) # formula for each characters total value
            temp = temp % mod_number # prevents too large number
            total = total + temp
            num -= 1

        return total % self.array_length

    def reflection_storage(self, character_name):
        index = self.hash_formula(character_name)
        self.array[index] = get_character_name(character_name)

    def hash_insertion(self,character_name):

        index=self.hash_formula(character_name) 
        tuple_list=get_character_name(character_name)

        if self.array[index] == None:
            self.array[index]= {

                character_name:tuple_list #tuples
            }
        
        else:

            self.array[index][character_name]=tuple_list

    def read_character(self,character_name):

        index=self.hash_formula(character_name)
        try:
            return self.array[index][character_name]

        except KeyError:

            print("Character doesnt exist")

    def delete_reflection(self,character_name):


        delete_choice=self.read_character(character_name) #provides characters reflections
        print(delete_choice)
        id_choice=input("Enter which Reflection ID you want to delete")#


        for value in delete_choice:

            if value[0]==id_choice:
                value=delete_choice.remove(value)
     

    def hashmap_initialise(self):

        characters=get_all_character()

        for character in characters:

            self.hash_insertion(character[0])


