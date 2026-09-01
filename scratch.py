from collections import defaultdict
class Solution(object):
    def firstUniqChar(self, s):
        """
        :type s: str
        :rtype: int
        """
        character_dict=defaultdict(int)
        for character in s:
            if character_dict[character] >0:
                character_dict[character]+=1
            elif character_dict[character]==0:
                character_dict[character]=1

        for char in character_dict:
            if character_dict[char] ==1:
                return s.index(char)
               
            
        return -1


   