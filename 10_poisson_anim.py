import numpy
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

##variable declarations
nx = 50
ny = 50
nt  = 20
xmin = 0
xmax = 2
ymin = 0
ymax = 1
target = 0.001

dx = (xmax - xmin) / (nx - 1)
dy = (ymax - ymin) / (ny - 1)

##initial conditions
p = numpy.zeros((ny, nx, 1200))  # create a XxY vector of 0's
delta = numpy.zeros((ny, nx, 1200))
b  = numpy.zeros((ny, nx))

##plotting aids
x = numpy.linspace(0, 2, nx)
y = numpy.linspace(0, 1, ny)

# Source
b[int(ny / 4), int(nx / 4)]  = 100
b[int(3 * ny / 4), int(3 * nx / 4)] = -100

##iteration
n = 0
run = True

while run is True:
    error = 0
    p[1:-1, 1:-1, n+1] = ((dy**2 * (p[1:-1, 2:, n] + p[1:-1, 0:-2, n]) +dx**2 * (p[2:, 1:-1, n] + p[0:-2, 1:-1, n])\
                             - b[1:-1,1:-1]*dx**2*dy**2) /(2 * (dx**2 + dy**2)))
         
    p[:, 0, n+1] = 0  
    p[:, -1, n+1] = 0  
    p[0, :, n+1] = 0
    p[-1, :, n+1] = 0  
    
    for j in range (ny):
        for i in range (nx):
            delta[j,i,n+1]=abs(p[j,i,n+1]-p[j,i,n])
    
    for j in range (ny):
        for i in range (nx):
            error=error+delta[j,i,n+1]
    if error<target:
        run = False
    n=n+1

print(n)
X, Y = numpy.meshgrid(x, y) 

zarray=p.copy()

def update_plot(frame_number, zarray, plot):
    plot[0].remove()
    plot[0] = ax.plot_surface(X, Y, zarray[:,:,frame_number], cmap='jet', edgecolors='k')

fig = pyplot.figure()
ax = fig.add_subplot(111, projection='3d')
plot = [ax.plot_surface(X, Y, zarray[:,:,0], cmap='jet', color='0.75', rstride=1, cstride=1)]
anim = animation.FuncAnimation(fig, update_plot, n, fargs=(zarray, plot), interval=20)
ax.set_xlim(0, 2)
ax.set_ylim(0, 1)
ax.view_init(30, 225)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('p')
pyplot.show()

f = r"g:/Kuliah/Python/Python CFD/Animation/10. Poisson.mp4" 
writervideo = animation.FFMpegWriter(fps=30) 
anim.save(f, writer=writervideo)