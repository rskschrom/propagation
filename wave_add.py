import numpy as np
import matplotlib.pyplot as plt
import os

# add random particles
zmin = 0.
zmax = 2.
xmin = -10.
xmax = 10.
ymin = -10.
ymax = 10.

numpar = 1000
rx = np.random.rand(numpar)*(xmax-xmin)+xmin
ry = np.random.rand(numpar)*(ymax-ymin)+ymin
rz = np.random.rand(numpar)*(zmax-zmin)+zmin

# add observation point
obz = 15.
obx = 0.
oby = 0.

# define wave properties
wavl = 2.
k = np.pi*2./wavl
ki = 0.2
omg = k*1.
t = 0.
s = 0.1

# add waves at observation point
r = np.sqrt(rx**2.+ry**2.+(obz-rz)**2.)

# loop over time
dt = 0.1
nt = 54
time = np.arange(nt)*dt
inwv = np.cos(k*obz-omg*time)
wvsum = 0.
pltind = 0
step = 10
parind = 0
for i in range(numpar):
    wvsum = wvsum+s*np.cos(k*rz[i]-omg*time)*np.cos(k*r[i])*np.exp(-ki*r[i])

    # plot every ten new particles
    if((float(i)/float(step)-i/step)<0.01):
        print pltind
        fig = plt.figure(pltind)

        # plot of particle locations
        fig.add_subplot(2,1,1)
        plt.scatter(rz[:parind], rx[:parind], c='k', s=10.)
        plt.plot([zmin, zmax, zmax, zmin, zmin],
                 [xmin, xmin, xmax, xmax, xmin], 'k--', lw=2.)
        plt.plot(obz, obx, 'bo')
        plt.text(obz-7., obx+0.5, 'Observation point', fontsize=20)
        parind = parind+step

        ax = plt.gca()
        ax.set_xlim([-10., 20.])
        ax.set_ylim([xmin, xmax])
        ax.set_xlabel('z-distance (propagation direction)', fontsize=22)
        ax.set_ylabel('x-distance (slab dimension)', fontsize=22)
        ax.set_aspect(1.)
        ax.grid()

        # waves at observation point
        fig.add_subplot(2,1,2)
        plt.plot(time, wvsum, 'r--', lw=3., label='sum of scattered waves')
        plt.plot(time, (inwv-wvsum)/np.max(inwv-wvsum), 'b--', lw=3., label='wave after propagation')
        plt.plot(time, inwv, 'k--', lw=3., label='incident wave')

        ax = plt.gca()
        ax.set_xlim([0., 5.])
        ax.set_ylim([-1.5, 3.])
        ax.set_xlabel('time', fontsize=22)
        ax.set_ylabel('electric field', fontsize=22)
        ax.grid()

        lg = plt.legend(fontsize=20)
        lg.draw_frame(False)

        imgname = 'wv_sum_{:03d}.png'.format(pltind)
        plt.savefig(imgname, dpi=60)
        plt.close()
        pltind = pltind+1
        os.system('convert -trim {} {}'.format(imgname, imgname))
