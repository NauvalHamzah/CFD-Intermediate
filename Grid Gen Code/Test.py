import math
import numpy as np
import os

import Core.CGridGen as CGrid
import Core.PlotMethod as PlotMethod

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
jMax = 4
nAirfoil = 7
nGap = 2
nFlap = 5
nAirfoilWake = 2
nOutflow = 5

nWake = nAirfoilWake + nOutflow - 1
iMax = 2*nAirfoil + 2*nGap + 2*nFlap + 2*nWake - 7

# Directory
# Create directory
dirName = "results"

if not os.path.exists(dirName):
    os.mkdir(dirName)
else:
    pass

# ---------------------------------------------------------------------------- #
# 2. INITIALIZATION OF X AND Y
# ---------------------------------------------------------------------------- #
# Initialize X and Y from the following configuration
X, Y = CGrid.Initialization(chord, gap, flap, rOutflow, rFarfield, wakeChord, thickness, nAirfoil, nGap, nFlap, 
                        nAirfoilWake, nOutflow, nWake, iMax, jMax)

# ---------------------------------------------------------------------------- #
# 3. GENERATE XI AND ETA
# ---------------------------------------------------------------------------- #
# Boundary normalization
u, v = CGrid.BoundaryNormalization(X, Y, iMax, jMax)

# Boundary-blended control function
xi, eta = CGrid.BoundaryBlendedControlFunction(u, v, iMax, jMax)

# ---------------------------------------------------------------------------- #
# 3. PERFORM TRANSFINITE INTERPOLATION
# ---------------------------------------------------------------------------- #
# Transfinite interpolation
X, Y = CGrid.TFI(X, Y, xi, eta, iMax, jMax)

# Mesh Quality Check
skewnessBefore = CGrid.MeshQuality(X, Y, iMax, jMax,"Mesh Quality - Before Smoothing")

PlotMethod.plotGrid(X, Y, "Transfinite Interpolation - Before Smoothing")

# ---------------------------------------------------------------------------- #
# 4. PERFORM SMOOTHING WITH LAPLACE
# ---------------------------------------------------------------------------- #
# Laplace smoothing
omega = 1.5
targetError = 1e-3

X, Y, residual = CGrid.LaplaceSmoothing(X, Y, iMax, jMax, nWake + nFlap + nGap - 3, omega, targetError)
PlotMethod.plotResidual(residual)

# Mesh Quality Check
skewnessAfter = CGrid.MeshQuality(X, Y, iMax, jMax,"Mesh Quality - After Smoothing")

# Plot Grid and Residual
PlotMethod.plotGrid(X, Y, "Transfinite Interpolation - After Smoothing")
PlotMethod.plotQualityComparison(skewnessBefore, skewnessAfter)

Nodes = CGrid.NodesCoordinates(X, Y, iMax, jMax, nWake, nFlap, nGap, nAirfoil, thickness)
CellNumber = CGrid.CellNumber(X,Y,iMax,jMax,nAirfoil,nFlap)
CellNeighbor = CGrid.CellNeighbor(X, Y, CellNumber, iMax, jMax, nAirfoil, nFlap, nWake, nGap)
CellNodalNumber = CGrid.CellNodalNumber(X, Y, Nodes, CellNumber, iMax, jMax, nAirfoil, nFlap, nWake, nGap)
CellTypes = CGrid.CellTypes(CellNodalNumber, iMax, jMax, nAirfoil, nFlap)
BoundaryFlags = CGrid.BoundaryFlags(CellNumber, iMax, jMax, nAirfoil, nFlap, nWake, nGap)
CGrid.WriteDataStructures(Nodes, CellNumber, CellNeighbor, CellNodalNumber, CellTypes, BoundaryFlags, iMax, jMax, nAirfoil, nFlap)


