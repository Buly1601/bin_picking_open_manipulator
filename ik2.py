from numpy import *

# Length of links in cm
a1 = 7.7
a2 = 13
a3 = 12.4

# Desired Position of End effector
px = 0
py = 0
pz = 0

# q1
try:
    q1 = arctan(py / px)
except:
    q1 = 0

phi = 90
phi = deg2rad(phi)

# Equations for Inverse kinematics
wx = px - a3*cos(phi)
wy = py - a3*sin(phi)

delta = wx**2 + wy**2
c2 = ( delta -a1**2 -a2**2)/(2*a1*a2)
s2 = sqrt(1-c2**2)  # elbow down
theta_2 = arctan2(s2, c2)

s1 = ((a1+a2*c2)*wy - a2*s2*wx)/delta
c1 = ((a1+a2*c2)*wx + a2*s2*wy)/delta
theta_1 = arctan2(s1,c1)
theta_3 = phi-theta_1-theta_2

print('theta_1: ', q1)
print('theta_2: ', theta_1)
print('theta_3: ', theta_2)
print('theta_4: ', theta_3)