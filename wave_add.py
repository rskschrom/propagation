import numpy as np
import matplotlib as mpl
mpl.use('Agg')
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
hv_rat = 2.
sh = 0.3
sv = sh/hv_rat

# add waves at observation point
r = np.sqrt(rx**2.+ry**2.+(obz-rz)**2.)
rho = np.sqrt(rx**2.+ry**2.)
rdif = r-rho-obz

# loop over time
tend = np.pi
nt = 201
time = np.arange(nt)/float(nt)*tend
inwv = np.cos(k*obz-omg*time)
wvsumh = 0.
wvsumv = 0.
pltind = 0
step = 20
pltcnt = -1
parind = 0

# change fonts
mpl.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],'size': 30})
mpl.rc('text', usetex=True)
mpl.rc('xtick.major', pad=10)
mpl.rc('ytick.major', pad=10)

fmtx = mpl.ticker.StrMethodFormatter("{x:.1f}")
fmty = mpl.ticker.StrMethodFormatter("{x:.1f}")

for i in range(numpar):
    wvsumh = wvsumh+sh*np.cos(k*rz[i]-omg*time)*np.cos(k*r[i])*np.exp(-ki*r[i])
    wvsumv = wvsumv+sv*np.cos(k*rz[i]-omg*time)*np.cos(k*r[i])*np.exp(-ki*r[i])
    pltcnt = pltcnt+1

    # plot every ten new particles
    if(pltcnt==(step*pltind)):
        print pltind
        fig = plt.figure(pltind)

        # plot of particle locations
        fig.add_subplot(2,1,1)
        plt.scatter(rz[:parind], rx[:parind], c='gray', s=10.)
        plt.plot([zmin, zmax, zmax, zmin, zmin],
                 [xmin, xmin, xmax, xmax, xmin], 'k--', lw=2.)
        plt.plot(obz, obx, 'ko', markersize=16.)
        plt.text(obz, obx+0.7, 'Observation point', horizontalalignment='center')
        parind = parind+step

        ax = plt.gca()
        ax.set_xlim([-10., 25.])
        ax.set_ylim([xmin, xmax])
        ax.set_xlabel('X-position')
        ax.set_ylabel('Z-position')
        ax.set_aspect(1.)
        ax.xaxis.set_major_formatter(fmtx)
        ax.yaxis.set_major_formatter(fmty)
        ax.grid()

        # waves at observation point
        fig.add_subplot(2,1,2)
        plt.plot(time, wvsumh, 'm--', lw=3., label='H-pol. scattered wave')
        plt.plot(time, wvsumv, 'c--', lw=3., label='V-pol. scattered wave')
        plt.plot(time, (inwv-wvsumh)/np.max(inwv-wvsumh), 'm-', lw=3., label='H-pol. propagation')
        plt.plot(time, (inwv-wvsumv)/np.max(inwv-wvsumv), 'c-', lw=3., label='V-pol. propagation')
        plt.plot(time, inwv, 'k-', lw=3., label='Incident wave')

        ax = plt.gca()
        ax.set_xlim([0., tend])
        ax.set_ylim([-1.5, 3.])
        ax.set_xlabel('Time')
        ax.set_ylabel('Electric field')
        ax.xaxis.set_major_formatter(fmtx)
        ax.yaxis.set_major_formatter(fmty)
        ax.grid()

        lg = plt.legend(ncol=3)
        lg.draw_frame(False)

        imgname = 'wv_sum_{:03d}.png'.format(pltind)
        plt.savefig(imgname, dpi=45)
        plt.close()
        pltind = pltind+1
        os.system('convert -trim {} {}'.format(imgname, imgname))
