from osgeo import ogr

import os, sys



def main( field_name_target ):

    # Get the input Layer

    inShapefile = "/home/gcorradini/Dropbox/LINUX_BASE_WORKSPACE/DATA/SHAPES/KC_ADMIN/parcel_address/parcel_address.shp"

    inDriver = ogr.GetDriverByName("ESRI Shapefile")

    inDataSource = inDriver.Open(inShapefile, 0)

    inLayer = inDataSource.GetLayer()

    inLayer.SetAttributeFilter("minor = 'HYDR'") # approximate the filter



    # Create the output LayerS

    outShapefile = os.path.join( os.path.split( inShapefile )[0], "ogr_api_filter.shp" )

    outDriver = ogr.GetDriverByName("ESRI Shapefile")



    # Remove output shapefile if it already exists

    if os.path.exists(outShapefile):

        outDriver.DeleteDataSource(outShapefile)



    # Create the output shapefile

    outDataSource = outDriver.CreateDataSource(outShapefile)

    out_lyr_name = os.path.splitext( os.path.split( outShapefile )[1] )[0]

    outLayer = outDataSource.CreateLayer( out_lyr_name, geom_type=ogr.wkbMultiPolygon )



    # Add input Layer Fields to the output Layer if it is the one we want

    inLayerDefn = inLayer.GetLayerDefn()

    for i in range(0, inLayerDefn.GetFieldCount()):

        fieldDefn = inLayerDefn.GetFieldDefn(i)

        fieldName = fieldDefn.GetName()

        #
        # approximate the select by only 
        # targeting our fileds of interest
        #
        if fieldName not in field_name_target:

            continue

        outLayer.CreateField(fieldDefn)



    # Get the output Layer's Feature Definition

    outLayerDefn = outLayer.GetLayerDefn()



    # Add features to the ouput Layer
    '''
    NOTE: sgillies mentions in a previous pull request
    that you should use the feature iterator whenever you can to avoid bugs:

        https://github.com/sgillies/py-gdalogr-cookbook/commit/6f658b80e497b1020a0ef89f5dfcdd6860819496

    This is good advice that should be followed. For example, a tricky unexpected
        bug that's worth pointing out happens if we were to use the folloing non-feature iterator code
    to loop through our inLayer features. Remember that inLayer has an attribute filter set:

        for i in range(0, inLayer.GetFeatureCount()):

    The GDAL/OGR Python docs point out that osgeo.ogr.Layer.SetAttributeFilter() works via
    OGR_L_GetNextFeature() function. That means you can still access *any* layer's
    feature regardless of whether it matches the filter or not using inLayer.GetFeature(<n+>). 
    This can lead to mind-boggling outputs. Using the feature iterator means that each feature
    returned will respect the attribute filter we set on the layer.
    '''

    for inFeature in inLayer:

        # Create output Feature

        outFeature = ogr.Feature(outLayerDefn)

        

        # Add field values from input Layer

        for i in range(0, outLayerDefn.GetFieldCount()):

            fieldDefn = outLayerDefn.GetFieldDefn(i)

            fieldName = fieldDefn.GetName()

            #
            # approximate the select by only 
            # targeting our fileds of interest
            #
            if fieldName not in field_name_target:

                continue



            outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(), inFeature.GetField(i))

                

        # Set geometry as centroid

        geom = inFeature.GetGeometryRef()

        outFeature.SetGeometry(geom.Clone())

        # Add new feature to output Layer

        outLayer.CreateFeature(outFeature)



    # Close DataSources

    inDataSource.Destroy()

    outDataSource.Destroy()



if __name__ == '__main__':

    '''
    EXAMPLE RUN: python ogr_api_hydra_filter.py [ FIELD_NAME  FIELD_NAME1  FIELD_NAME2 ]
    $ python ogr_api_hydra_filter.py PIN MINOR
    '''
    if len( sys.argv ) < 2:

        print "[ ERROR ]: you need to pass at least one arg -- the field_name to target"

        sys.exit(1)

    

    main( sys.argv[1:] )

    
