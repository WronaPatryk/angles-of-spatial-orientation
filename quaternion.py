#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


def qa(THETA, PSI, FI):
    def qa0(THETA, PSI, FI):
        return np.cos(PSI/2) * np.cos(THETA/2) * np.cos(FI/2) + np.sin(PSI/2) * np.sin(THETA/2) * np.sin(FI/2)
    
    def qa1(THETA, PSI, FI):
        return np.cos(PSI/2) * np.cos(THETA/2) * np.sin(FI/2) - np.sin(PSI/2) * np.sin(THETA/2) * np.cos(FI/2)
        
    def qa2(THETA, PSI, FI):
        return np.cos(PSI/2) * np.sin(THETA/2) * np.cos(FI/2) + np.sin(PSI/2) * np.cos(THETA/2) * np.sin(FI/2)
        
    def qa3(THETA, PSI, FI):
        return np.sin(PSI/2) * np.cos(THETA/2) * np.cos(FI/2) - np.cos(PSI/2) * np.sin(THETA/2) * np.sin(FI/2)
    
    return [qa0(THETA,PSI,FI), qa1(THETA,PSI,FI), qa2(THETA,PSI,FI), qa3(THETA,PSI,FI)]       


# In[3]:


def qb(wx, wy, wz, dt = 0.005):
    w = np.sqrt(wx**2 + wy**2 + wz**2)
    
    fi0 = w * dt
    
    qb0 = np.cos(fi0/2)
    
    qb1 = (wx/w) * np.sin(fi0/2)
    
    qb2 = (wy/w) * np.sin(fi0/2)
    
    qb3 = (wz/w) * np.sin(fi0/2)
    
    return [qb0, qb1, qb2, qb3]


# In[4]:


def qq(qa, qb):
    q0 = qa[0] * qb[0] - qa[1] * qb[1] - qa[2] * qb[2] - qa[3] * qb[3] 
    
    q1 = qa[0] * qb[1] + qa[1] * qb[2] + qa[2] * qb[3] - qa[3] * qb[2]
    
    q2 = qa[0] * qb[2] - qa[1] * qb[3] + qa[2] * qb[0] + qa[3] * qb[1]
    
    q3 = qa[0] * qb[3] + qa[1] * qb[2] - qa[2] * qb[1] + qa[3] * qb[0]
    
    return [q0, q1, q2, q3]


# In[5]:


def CGH(q):
    return np.array([[2 * (q[0]**2 + q[1]**2) - 1,       2 * (q[1] * q[2] - q[0]*q[3]),    2 * (q[1] * q[3] + q[0]*q[2])],
                     [2 * (q[1] * q[2] + q[0]*q[3]),   2 * (q[0]**2 + q[2]**2) - 1 ,       2 *(q[2] * q[3] - q[0]*q[1])],
                     [2 * (q[1] * q[3] - q[0]*q[2]),   2 *(q[2] * q[3] + q[0]*q[1]),     2 * (q[0]**2 + q[3]**2) - 1]]) 


# In[6]:


def TFP(CGH):
    def THETA(CGH):
        return np.arcsin(- CGH[0][2])
    
    def FI(CGH):
        return -2 * np.arctan(CGH[1][2]/(CGH[2][2] + np.cos(np.arcsin(- CGH[0][2]))))
    
    def PSI(CGH):
        return -2 * np.arctan(CGH[0][1]/(CGH[0][0] + np.cos(np.arcsin(- CGH[0][2]))))
    
    return [THETA(CGH), PSI(CGH), FI(CGH)]


# In[7]:


def not_ort_err(q):
    return q[0] + q[1] + q[2] + q[3] - 1

def q_length(q):
    return np.sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2)


# In[14]:


def quaternion(q_a, P, Q, R):
    q_b = qb(P, Q, R) 
    q = qq(q_a, q_b)
    tfp = TFP(CGH(q))
    return [q, tfp[0]*(180/np.pi), tfp[1]*180/np.pi, tfp[2]*180/np.pi, not_ort_err(q), q_length(q)]          


# In[13]:


quaternion([0,0,0,1],1,1,0)

