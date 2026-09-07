class Solution:
    def twoSum(self, nums, target):
        nums_set={}

        for i in range(len(nums)):
            needed_value= target - nums[i]
            if needed_value in nums_set: # there is a number which adds with our current number to make target
                smaller_number_index=nums.index(needed_value)
                
                if i>smaller_number_index:
                    return [smaller_number_index,i]
                elif smaller_number_index>i:
                    return[i,smaller_number_index]
            else:
                nums_set[nums[i]]=0



            


        
        