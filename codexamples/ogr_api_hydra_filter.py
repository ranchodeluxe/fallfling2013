from osgeo import ogr

import os, sys


# Get the input Layer

inShapefile = "/home/gcorradini/Dropbox/LINUX_BASE_WORKSPACE/DATA/SHAPES/KC_ADMIN/parcel_address/parcel_address.shp"

inDriver = ogr.GetDriverByName("ESRI Shapefile")

inDataSource = inDriver.Open(inShapefile, 0)

inLayer = inDataSource.GetLayer()

inLayer.SetAttributeFilter("PIN = '0000200001'") # filter only one record

#
#  GOTCHA: we can still access features
#  that are not covered by the filter 
#  using inLayer.GetFeature(<n+>)
#  
print "\nFeatures not covered by attribute filter, but still accessible ( YIKES! )..."
#  imagine that this next line was `for i in range(0, inLayer.GetFeatureCount() )`
for i in range(0, 10):
    feat = inLayer.GetFeature( i )
    print feat.GetField(1)


#
#  CORRECT: the filter is only
#  respected if we use the iterator
#  OGR_L_GetNextFeature()
#  which, looping through the inLayer
#  accomplishes
#
print "\nFeatures covered by attribute filter..."
for feat in inLayer:
    print feat.GetField(1) # this should only print one feature

