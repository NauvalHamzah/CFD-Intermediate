import math
import numpy as np

from AirfoilEquation import NACA0012
import PlotMethod

def Initialization(chord, gap, flap, rOutflow, rFarfield, wakeChord, thickness, nAirfoil, ngap, nflap, 
                        nAirfoilWake, nOutflow, nWake, iMax, jMax):
    
    # Initialize
    X = np.zeros(shape=(iMax,jMax))
    Y = np.zeros(shape=(iMax,jMax))

    # Initialize coordinates
    # titik 1
    X[0,0] = rOutflow
    Y[0,0] = 0

    # titik 2
    X[nWake-1,0] = chord+gap+flap
    Y[nWake-1,0] = 0

    # titik 3
    X[nWake-1 + nflap-1,0] = chord+gap
    Y[nWake-1 + nflap-1,0] = 0

    # titik 4
    X[nWake-1 + nflap-1 + ngap-1,0] = chord
    Y[nWake-1 + nflap-1 + ngap-1,0] = 0

    # titik 5
    X[nWake-1 + nflap-1 + ngap-1 + nAirfoil-1 ,0] = 0
    Y[nWake-1 + nflap-1 + ngap-1 + nAirfoil-1 ,0] = 0

    # titik 6
    X[iMax-1,0] = rOutflow
    Y[iMax-1,0] = 0

    # titik 7
    X[iMax-1,jMax-1] = rOutflow
    Y[iMax-1,jMax-1] = rFarfield

    # titik 8
    X[(iMax-1)-(nWake-1),jMax-1] = chord+gap+flap
    Y[(iMax-1)-(nWake-1),jMax-1] = rFarfield

    # titik 9
    X[nWake-1,jMax-1] = chord+gap+flap
    Y[nWake-1,jMax-1] = -rFarfield

    # titik 10
    X[0,jMax-1] = rOutflow
    Y[0,jMax-1] = -rFarfield

    # Initialize Boundary coordinates
    # Vertical left and right
    for j in range(1, jMax-1):
        eta = j/(jMax-1)
        m = rFarfield

        # Distribution
        A = 1.2   # exponential

        # Left
        X[0,j] = rOutflow
        #Y[0,j] = -m*eta     # linear
        Y[0,j] = -m*(math.exp(A*eta)-1)/(math.exp(A)-1) #exponential

        # Right
        X[iMax-1,j] = rOutflow
        #Y[iMax-1,j] = m*eta # linear
        Y[iMax-1,j] = m*(math.exp(A*eta)-1)/(math.exp(A)-1) # exponential

    # Top Boundary: Horizontal
    for i in range(1, nWake-1):
        xi = i/(nWake-1)
        m = rOutflow-1

        # Top: Lower
        X[i,jMax-1] = rOutflow - m*xi   # linear
        #X[i,jMax-1] = rOutflow - m*math.sin(0.5*math.pi*xi)    # cosinus
        Y[i,jMax-1] = -rFarfield
        
        # Top: Top
        startIndex = iMax-1 
        X[startIndex-i,jMax-1] = rOutflow - m*xi
        Y[startIndex-i,jMax-1] = rFarfield

    # Top Boundary: C-shaped
    for i in range(1, 2*(nAirfoil+ngap+nflap-2)-2):
        m = rFarfield
        xi = i/(2*(nAirfoil+ngap+nflap-2)-2)   # linear
        #xi = 1-math.cos(0.5*math.pi*xi)     # cosinus

        # linear distribution
        startIndex = nWake-1
        X[startIndex+i,jMax-1] = m*math.sin(-math.pi*xi) + (chord+gap+flap)
        Y[startIndex+i,jMax-1] = -m*math.cos(-math.pi*xi)

    # Bottom Boundary: Outflow
    for i in range(1,nOutflow):
        xi = i/(nOutflow-1)
        m = rOutflow-(chord+gap+flap+wakeChord)

        X[i,0] = rOutflow - m*xi                            # linear
        #X[i,0] = rOutflow - m*math.sin(0.5*math.pi*xi)     # cosinus
        Y[i,0] = 0

        X[(iMax-1)-i,0] = X[i,0]                                    # linear
        #X[iMax-1)-i,0] = rOutflow - m*math.sin(0.5*math.pi*xi)     # cosinus
        Y[(iMax-1)-i,0] = Y[i,0]

    # Bottom Boundary: Airfoil wake
    for i in range(1,nAirfoilWake):
        xi = i/(nAirfoilWake-1)
        m = wakeChord 

        # Bottom: Lower
        startIndex1 = nOutflow-1
        #X[startIndex+i,0] = chord + m*xi   # linear
        X[startIndex1+i,0] = chord + gap + flap + wakeChord - m*math.sin(0.5*math.pi*xi)    # cosinus
        Y[startIndex1+i,0] = 0
        
        # Bottom: Upper
        startIndex2 = (iMax-nOutflow)
        X[startIndex2-i,0] = X[startIndex1+i,0]
        Y[startIndex2-i,0] = 0

    # Bottom Boundary: flap
    for i in range(1,nflap):
        xi = i/(nflap-1)
        m = flap

        # Bottom: Bottom
        startIndex1 = nWake-1
        #X[startIndex+i,0] = chord + m*xi   # linear
        X[startIndex1+i,0] = chord + gap + flap - m*math.sin(0.5*math.pi*xi)    # cosinus
        Xrel = (X[startIndex1+i,0]- (chord + gap))/flap
        Y[startIndex1+i,0] = NACA0012(Xrel, thickness, flap)

        # Bottom: Top
        startIndex2 = (iMax-nWake)
        X[startIndex2-i,0] = X[startIndex1+i,0]
        Y[startIndex2-i,0] = -Y[startIndex1+i,0]

    # Bottom Boundary: gap
    for i in range(1,ngap):
        xi = i/(ngap-1)
        m = gap

        # Bottom: Bottom
        startIndex1 = nWake + nflap - 2
        #X[startIndex+i,0] = chord + m*xi   # linear
        X[startIndex1+i,0] = chord + gap - m*math.sin(0.5*math.pi*xi)    # cosinus
        Y[startIndex1+i,0] = 0

        # Bottom: Top
        startIndex2 = (iMax- (nWake + nflap -1))
        X[startIndex2-i,0] = X[startIndex1+i,0]
        Y[startIndex2-i,0] = 0

    # Bottom Boundary: Airfoil
    for i in range(1,nAirfoil):
        xi = i/(nAirfoil-1)
        m = chord

        # Bottom: Bottom
        startIndex1 = nWake + nflap + ngap - 3
        #X[startIndex+i,0] = chord + m*xi   # linear
        X[startIndex1+i,0] = chord - m*math.sin(0.5*math.pi*xi)    # cosinus
        Xrel = (X[startIndex1+i,0]-0)/chord
        Y[startIndex1+i,0] = NACA0012(Xrel, thickness, chord)

        # Bottom: Top
        startIndex2 = (iMax- (nWake + nflap + ngap -2))
        X[startIndex2-i,0] = X[startIndex1+i,0]
        Y[startIndex2-i,0] = -Y[startIndex1+i,0]

    return (X, Y)

def BoundaryNormalization(X, Y, iMax, jMax):
    # Normalization at boundary
    meshLength = np.zeros(shape=(iMax-1, jMax-1))
    u = np.zeros(shape=(iMax, jMax))
    v = np.zeros(shape=(iMax, jMax))

    # Bottom
    totalLength = 0
    for i in range(iMax-1):
        dx = X[i+1,0] - X[i,0]
        dy = Y[i+1,0] - Y[i,0]
        dLength = math.sqrt(dx**2 + dy**2)
        totalLength = totalLength + dLength
        meshLength[i,0] = totalLength

    for i in range(iMax-1):
        u[i+1,0] = meshLength[i,0]/totalLength
        v[i+1,0] = 0

    # Top
    totalLength = 0
    for i in range(iMax-1):
        dx = X[i+1,jMax-1] - X[i,jMax-1]
        dy = Y[i+1,jMax-1] - Y[i,jMax-1]
        dLength = math.sqrt(dx**2 + dy**2)
        totalLength = totalLength + dLength
        meshLength[i,jMax-2] = totalLength
        
    for i in range(iMax-1):
        u[i+1,jMax-1] = meshLength[i,jMax-2]/totalLength
        v[i+1,jMax-1] = 1

    # reset
    meshLength = np.zeros(shape=(iMax-1, jMax-1))

    # Left
    totalLength = 0
    for i in range(jMax-1):
        dx = X[0,i+1] - X[0,i]
        dy = Y[0,i+1] - Y[0,i]
        dLength = math.sqrt(dx**2 + dy**2)
        totalLength = totalLength + dLength
        meshLength[0,i] = totalLength

    for i in range(jMax-1):
        u[0,i+1] = 0
        v[0,i+1] = meshLength[0,i]/totalLength
        
    # Right
    totalLength = 0
    for i in range(jMax-1):
        dx = X[iMax-1,i+1] - X[iMax-1,i]
        dy = Y[iMax-1,i+1] - Y[iMax-1,i]
        dLength = math.sqrt(dx**2 + dy**2)
        totalLength = totalLength + dLength
        meshLength[iMax-2,i] = totalLength

    for i in range(jMax-1):
        u[iMax-1,i+1] = 1
        v[iMax-1,i+1] = meshLength[iMax-2,i]/totalLength

    return (u, v)

def BoundaryBlendedControlFunction(u, v, iMax, jMax):
    # Boundary-Blended Control Functions
    for i in range(iMax-1):
        for j in range(jMax-1):
            part1 = (1-v[0,j])*u[i,0] + v[0,j]*u[i,jMax-1]
            part2 = 1 - (u[i,jMax-1]-u[i,0])*(v[iMax-1,j]-v[0,j])
            u[i,j] = part1/part2

            part1 = (1-u[i,0])*v[0,j] + u[i,0]*v[iMax-1,j]
            part2 = 1 - (v[iMax-1,j]-v[0,j])*(u[i,jMax-1]-u[i,0])
            v[i,j] = part1/part2
            #u[i,j] = u[i,0] + v[0,j]*(u[i,jMax-1]-u[i,0])
            #v[i,j] = v[0,j] + u[i,0]*(v[iMax-1,j]-v[0,j])
    return (u, v)

def TFI(X, Y, xi, eta, iMax, jMax):
    # Transfinite Interpolation
    for i in range(1,iMax-1):
        for j in range(1,jMax-1):
            U = (1-xi[i,j])*X[0,j] + xi[i,j]*X[iMax-1,j]
            V = (1-eta[i,j])*X[i,0] + eta[i,j]*X[i,jMax-1]
            UV = xi[i,j]*eta[i,j]*X[iMax-1,jMax-1] + xi[i,j]*(1-eta[i,j])*X[iMax-1,0] +\
                (1-xi[i,j])*eta[i,j]*X[0,jMax-1] + (1-xi[i,j])*(1-eta[i,j])*X[0,0]
            X[i,j] = U + V - UV

            U = (1-xi[i,j])*Y[0,j] + xi[i,j]*Y[iMax-1,j]
            V = (1-eta[i,j])*Y[i,0] + eta[i,j]*Y[i,jMax-1]
            UV = xi[i,j]*eta[i,j]*Y[iMax-1,jMax-1] + xi[i,j]*(1-eta[i,j])*Y[iMax-1,0] +\
                (1-xi[i,j])*eta[i,j]*Y[0,jMax-1] + (1-xi[i,j])*(1-eta[i,j])*Y[0,0]
            Y[i,j] = U + V - UV

    return (X, Y)

def MeshQuality(X, Y, iMax, jMax, title):
    # Mesh Quality
    meshArea = np.zeros(shape=(iMax-1, jMax-1))
    meshSkewness = np.zeros(shape=(iMax-1, jMax-1))

    for i in range(iMax-1):
        for j in range(jMax-1):
            p = np.array([X[i,j+1] - X[i,j], Y[i,j+1] - Y[i,j]])
            q = np.array([X[i+1,j+1] - X[i,j+1], Y[i+1,j+1] - Y[i,j+1]])
            r = np.array([X[i+1,j+1] - X[i+1,j], Y[i+1,j+1] - Y[i+1,j]])
            s = np.array([X[i+1,j] - X[i,j], Y[i+1,j] - Y[i,j]])

            # Mesh Area
            area1 = -np.cross(p,s)
            area2 = np.cross(-q,-r)
            meshArea[i,j] = 0.5*(area1 + area2)

            # Skewness
            teta1 = math.degrees(math.atan2(-np.cross(p,s),np.dot(p,s)))
            teta2 = math.degrees(math.atan2(-np.cross(-s,r),np.dot(-s,r)))
            teta3 = math.degrees(math.atan2(-np.cross(-r,-q),np.dot(-r,-q)))
            teta4 = 360 - (teta1 + teta2 + teta3)
            teta = np.array([teta1, teta2, teta3, teta4])        
            tetaMaxOnMesh = (np.max(teta)-90)/90
            tetaMinOnMesh = (90-np.min(teta))/90
            skewness = max(np.array([tetaMaxOnMesh, tetaMinOnMesh]))
            meshSkewness[i,j] = skewness
    
    # Create bar chart of skewness
    data1 = []      # storing cell skewness < 0.2
    data2 = []      # storing cell skewness < 0.4
    data3 = []      # storing cell skewness < 0.6
    data4 = []      # storing cell skewness < 0.8
    data5 = []      # storing cell skewness > 0.8

    for i in range(iMax-1):
        for j in range(jMax-1):
            if (meshSkewness[i,j] < 0.2):
                data1.append(meshSkewness[i,j])
            elif (meshSkewness[i,j] < 0.4):
                data2.append(meshSkewness[i,j])
            elif (meshSkewness[i,j] < 0.6):
                data3.append(meshSkewness[i,j])
            elif (meshSkewness[i,j] < 0.8):
                data4.append(meshSkewness[i,j])
            else:
                data5.append(meshSkewness[i,j])
    
    skewnessData = [len(data1), len(data2), len(data3), 
                    len(data4), len(data5)]
    #PlotMethod.plotBarQuality(skewnessData, title)

    print("")
    print("# --------------------------------------- #")
    print("             MESH QUALITY CHECK")
    print("# --------------------------------------- #")
    print("minimum mesh area = %.2e" % np.min(meshArea))
    print("maximum mesh area = %.4f" % np.max(meshArea))
    print("ortoghonality scale. 0 = Orthogonal")
    print("minimum value = %.2e" % np.min(meshSkewness))
    print("maximum value = %.4f" % np.max(meshSkewness))
    print("")

    return (skewnessData)

# ---------------------------------------------------------------------------- #
# 1. INPUT 
# ---------------------------------------------------------------------------- #
# Boundary configurations
chord = 1
gap = 0.1*chord
flap = 0.2*chord
rOutflow = 10*chord
rFarfield = 5*chord
wakeChord = 0.2*chord
thickness = 0.12

# Nodal configurations
jMax = 31
nAirfoil = 21
ngap = 7
nflap = 11
nAirfoilWake = 7
nOutflow = 31

nWake = nAirfoilWake + nOutflow - 1
iMax = 2*nAirfoil + 2*ngap + 2*nflap + 2*nWake - 7

X, Y = Initialization(chord, gap, flap, rOutflow, rFarfield, wakeChord, thickness, nAirfoil, ngap, nflap, 
                        nAirfoilWake, nOutflow, nWake, iMax, jMax)
#np.savetxt('X_baru.txt', X, delimiter=',')
#np.savetxt('Y_baru.txt', Y, delimiter=',')
u, v = BoundaryNormalization(X, Y, iMax, jMax)
xi, eta = BoundaryBlendedControlFunction(u, v, iMax, jMax)
# ---------------------------------------------------------------------------- #
# 3. PERFORM TRANSFINITE INTERPOLATION
# ---------------------------------------------------------------------------- #
# Transfinite interpolation
X, Y = TFI(X, Y, xi, eta, iMax, jMax)

# Mesh Quality Check
skewnessBefore = MeshQuality(X, Y, iMax, jMax,"Mesh Quality - Before Smoothing")

PlotMethod.plotGrid(X, Y, "Transfinite Interpolation - Before Smoothing")                                        

