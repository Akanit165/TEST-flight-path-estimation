from sd_time import angle
#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


plt.style.use('dark_background')
fig = plt.figure()
fig.suptitle("\nECEF and ECI Reference Frame")
ax = fig.add_subplot(111, projection='3d')

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

x = 0.3*np.outer(np.cos(u), np.sin(v))
y = 0.3*np.outer(np.sin(u), np.sin(v))
z = 0.3*np.outer(np.ones(np.size(u)), np.cos(v))

# Plot the ECI reference frame
start = [0,0,0]
ax.set_xlim(-1,1,0.5)
ax.set_ylim(-1,1,0.5)
ax.set_zlim(-1,1,0.5)
ax.set_xticks(np.arange(-1, 1.2,0.5))
ax.set_yticks(np.arange(-1, 1.2,0.5))
ax.set_zticks(np.arange(-1, 1.2,0.5))
ax.quiver(start[0],start[1],start[2], 1,0,0, label = '$X_{ECI}$', colors = 'r')
ax.quiver(start[0],start[1],start[2], 0,1,0, label = '$Y_{ECI}$', colors = 'yellow')
ax.quiver(start[0],start[1],start[2], 0,0,1, label = '$Z_{ECI}$', colors = 'yellow')
ax.view_init(35,45)
ax.set_xlabel('$x\ (Vernal\ Equinox)$')
ax.set_ylabel('$y$')
ax.set_zlabel('$z\ (North\ Pole)$')


# Plot ECEF frame usig GMST, UT1, UTC

dcm = angle()

ub = [dcm[0,0],dcm[0,1],dcm[0,2]]
vb = [dcm[1,0],dcm[1,1],dcm[1,2]]
wb = [dcm[2,0],dcm[2,1],dcm[2,2]]

start = [0,0,0]
ax.quiver(start[0],start[1],start[2], ub[0],ub[1],ub[2], label = '$X_{ECEF}$', colors = 'w')
ax.quiver(start[0],start[1],start[2], vb[0],vb[1],vb[2], label = '$Y_{ECEF}$', colors = 'b')
ax.quiver(start[0],start[1],start[2], wb[0],wb[1],wb[2], label = '$Z_{ECEF}$', colors = 'b')

"""
Case 2 plot ECI in term of ECEF 

Sequence: 
    1. Receive data from GNSS (ECEF)
    2. Calculate potential energy in ECEF frame
    3. Calculate acceleration in ECI (a = dcm * U)
    4. Calculate satellite position at instance time, t
"""

# start = [0,0,0]
# ax.set_xlim(-1,1,0.5)
# ax.set_ylim(-1,1,0.5)
# ax.set_zlim(-1,1,0.5)
# ax.set_xticks(np.arange(-1, 1.2,0.5))
# ax.set_yticks(np.arange(-1, 1.2,0.5))
# ax.set_zticks(np.arange(-1, 1.2,0.5))
# ax.quiver(start[0],start[1],start[2], 1,0,0, label = '$X_{ECEF}$', colors = 'w')
# ax.quiver(start[0],start[1],start[2], 0,1,0, label = '$Y_{ECEF}$', colors = 'b')
# ax.quiver(start[0],start[1],start[2], 0,0,1, label = '$Z_{ECEF}$', colors = 'b')
# ax.view_init(35,45)

# # Plot ECEF frame usig GMST, UT1, UTC

# dcm = angle()

# ub = [dcm[0,0],dcm[0,1],dcm[0,2]]
# vb = [dcm[1,0],dcm[1,1],dcm[1,2]]
# wb = [dcm[2,0],dcm[2,1],dcm[2,2]]


# ax.quiver(start[0],start[1],start[2], ub[0],ub[1],ub[2], label = '$X_{ECI}$', colors = 'r')
# ax.quiver(start[0],start[1],start[2], vb[0],vb[1],vb[2], label = '$Y_{ECI}$', colors = 'yellow')
# ax.quiver(start[0],start[1],start[2], wb[0],wb[1],wb[2], label = '$Z_{ECI}$', colors = 'yellow')



# Use 3x the stride, no scipy zoom
ax.plot_surface(x, y, z, rstride=3, cstride=3, color='w', shade=0)

ax.legend()
plt.show()

