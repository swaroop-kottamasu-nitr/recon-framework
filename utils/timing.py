import random
import time

PROFILE = "normal"



def random_delay():

    if PROFILE == "aggressive":


        delay = random.uniform(
            0,
            0.05
        )
    elif PROFILE == "normal":
        delay = random.uniform(
            0.1,
            0.5
        )
    else:
        delay = random.uniform(
            0.5,
            2
        )    
    time.sleep(delay)