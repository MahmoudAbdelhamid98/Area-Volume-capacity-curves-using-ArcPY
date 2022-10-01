import arcpy
from arcpy import env
from arcpy import mapping as mp
from arcpy import management as man
from arcpy import sa as spa
from arcpy import ddd as TD
import matplotlib.pyplot as plt

#1 Inputs Section

mxd = mp.MapDocument("CURRENT")
Damshp = mp.ListLayers(mxd)[0]
DEM = mp.ListLayers(mxd)[1]
MaxE = 670
MinE= 500
StepE = 10
nsteps = (MaxE-MinE)/StepE

#2 Environment Setting

workfolder = "D:\educational\Masters_spring2022\CEI613_GIS2\Assignment2"
env.scratchWorkspace = workfolder+"/TEMP"
env.overwriteOutput = True
env.addOutputsToMap = True
outfname = r"D:\educational\Masters_spring2022\CEI613_GIS2\Assignment2\vol_area.txt"
outf = open(outfname,'w')

#3 Creating clip contour 

spa.ContourList(DEM,"contMax",MaxE)
man.MakeFeatureLayer("contMax","contMax_lyr")
man.SelectLayerByLocation("contMax_lyr","INTERSECT",Damshp)

#4 Coverting clip contour and dam to clip polygon

man.FeatureToPolygon([Damshp,"contMax_lyr"],"Clip_Lyr")

#5 Clipping DEM using the polygon

DEM_Clipped = spa.ExtractByMask (DEM,"Clip_Lyr")
LowestE = DEM_Clipped.minimum

#6 Surface volume data extraction

outf.write("Elev(m),Area2D(m2),Volume(m3)\n")
E=[]
A=[]
V=[]
for i in range(MinE,MaxE+StepE,StepE):
    if i < LowestE:
        outf.write(str(i)+",0,0\n")
        continue
    Results = TD.SurfaceVolume(DEM_Clipped,"","BELOW",i).getMessage(2)
    Area= Results.split("=")[1].split(" ")[0]
    Vol=Results.split("=")[3]
    outf.write(str(i)+","+Area+","+Vol+"\n")
    E.append(i)
    A.append(Area)
    V.append(Vol)

#7 Removing unnecessary files and closing files
outf.close()
man.Delete("contMax_lyr")
man.Delete("contMax")

#Extra: Plotting curves
#plotting Area vs stage

plt.xlabel("Elevation (m)")
plt.ylabel("Area (m2)")
plt.title("Area vs Stage")
plt.plot(E,A)
plt.savefig(workfolder+"\AreaElevation")

#plotting Volume vs stage

plt.xlabel("Elevation (m)")
plt.ylabel("Volume (m3)")
plt.title("Volume vs Stage")
plt.plot(E,V)
plt.savefig(workfolder+"\VolElevation")
    



