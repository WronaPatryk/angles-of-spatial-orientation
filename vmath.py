import numpy as np

def CNB (yaw, pitch, roll):
    return np.array([[np.cos(yaw) * np.cos(pitch),  np.sin(yaw) * np.cos(pitch) ,   - np.sin(pitch)] ,
                    [np.cos(yaw) * np.sin(pitch) * np.sin(roll) - np.sin(yaw) * np.cos(roll), np.sin(yaw) * np.sin(pitch) * np.sin(roll) + np.cos(yaw) * np.cos(roll) , np.cos(pitch) * np.sin(roll)  ],
                    [np.cos(yaw) * np.sin(pitch) * np.cos(roll) + np.sin(yaw) * np.sin(roll), np.sin(yaw) * np.sin(pitch) * np.cos(roll) - np.cos(yaw) * np.sin(roll), np.cos(pitch) * np.cos(roll) ]])


def nvec(angles):
    return np.matmul(CNB(angles[0] * np.pi/180 ,angles[1] * np.pi/180 ,angles[2] * np.pi/180), [0,0,-1])

import quaternion as quat
import EKF as ekf


# def S_omega(omega):
#     return np.array([   [0, -omega[0], -omega[1], -omega[2]],
#                         [omega[0], 0 , omega[2], -omega[1]],
#                         [omega[1], -omega[2], 0 , omega[0]],
#                         [omega[2], omega[1], -omega[0], 0]])

# def S_quat(q):
#     return np.array([   [-q[1], -q[2], -q[3]],
#                         [q[0], -q[3], q[2]],
#                         [q[3], q[0], -q[1]],
#                         [-q[2], q[1], q[0]]])

# def normalize_quat(q):
#         mag = (q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2)**0.5
#         return q / mag


# def A_matrix():
#     return np.identity(4)
                                

# def B_matrix(dt, q):
#     return dt / 2 * S_quat(q[0:4])

bquat = [1,0,0,0]

dt = 1

omega = [0,-10*np.pi/180, 0]

ans = quat.quaternion(bquat, omega)

angs = ekf.getEulerAngles(ans[0])

print(angs)

vec = nvec(angs)

print(vec)

# qx =  bquat + np.matmul(B_matrix(dt, bquat), np.array(omega).transpose())
# qy = normalize_quat(qx)

# print(ekf.getEulerAngles(qy))