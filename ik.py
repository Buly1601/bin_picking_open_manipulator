

import numpy as np
import math

def get_ik(x=0, y=0, z=0):
    """
    Function to get the inverse kinematics of a 3DOF planar robot
    using geometric analysis.
    """
    # define metrics
    a2 = 0.128 + 0.077
    a3 = 0.124 + 0.024
    a4 = 0.126
    phi = 1.5708 #? 90 + 0 + 0
    q2 = 1.5708
    q3 = 0
    q4 = 0

    # get z-rotating q1
    q1 = math.atan(y / x)

    # compute q2, q3, q4
    r3 = math.sqrt(x**2 + y**2)
    z3 = z - 0.052

    r2 = r3 - (a4 * math.cos(phi))
    z2 = z3 - (a4 * math.sin(phi))

    q3 = math.acos((r2**2 + z2**2 - (a4**2 + a3**2)) / (2 * a4 * a3))

    r2 = (a2 * math.cos(q2)) + (a3 * math.cos(q2 + q3))
    z2 = (a2 * math.sin(q2)) + (a3 * math.sin(q2 + q3))

    r2 = math.cos(q2) * (a2 + (a3 * math.cos(q3))) - math.sin(q2) * (a3 * math.sin(q3))
    z2 = math.cos(q2) * (a3 * math.sin(q3)) - math.sin(q2) * (a2 + (a3 * math.cos(q3)))

    cos_memo_q2 = ((a2 + (a3 * math.cos(q3)) * r2) + (a3 * math.sin(q3)) * z2) / (r2**2 + z2**2)
    sin_memo_q2 = ((a2 + (a3 * math.cos(q3)) * z2) + (a3 * math.sin(q3)) * r2) / (r2**2 + z2**2)

    q2 = math.atan(sin_memo_q2 / cos_memo_q2)

    q4 = phi - (q2 + q3)

    return q1, q2, q3, q4

print(get_ik(x = 0.207, y = 0, z = 0.205))