import random
import time


STEALTH_MODE = False


def random_delay():

    if STEALTH_MODE:

        delay = random.uniform(
            0.1,
            0.5
        )

        time.sleep(delay)