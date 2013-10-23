from osgeo import ogr

import os, sys


# Get the input Layer

inShapefile = "/home/gcorradini/Dropbox/LINUX_BASE_WORKSPACE/DATA/SHAPES/KC_ADMIN/parcel_address/parcel_address.shp"

inDriver = ogr.GetDriverByName("ESRI Shapefile")

inDataSource = inDriver.Open(inShapefile, 0)

inLayer = inDataSource.GetLayer()

inLayer.SetAttributeFilter("PIN = '0000200001'") # filter only one record

feat = inLayer.GetNextFeature()

print feat
