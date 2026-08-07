import time
class Reflection_Timer:

  


    def __init__(self,duration): #initialisation methods

        self.duration=duration
        self.start_time=time.monotonic()
    


        
        
    #seconds_remaining() — returns the whole seconds left in the countdown, computed fresh from duration,
    # the recorded start point, and the current time each time it's called. Never returns a negative number.

    def seconds_remaining(self): #2 variables needed by the seconds remaining is the duration and the start time

        remainder=self.duration - (time.monotonic()-self.start_time) #how we calculate the remaining time

        if remainder <=0: #never have a negative number
            remainder =0

        return int(remainder)

#`is_timer_finished()` — returns `True` once the countdown has reached zero, `False` otherwise. 
#False otherwise. This must be derived from seconds_remaining(), not tracked as its own separate flag.

    def is_timer_finished(self):

        remainder=self.seconds_remaining()

        if remainder == 0:
            status= True

        else:
            status=False
        
        return status



