import subprocess
import sys

try:
    from osgeo import ogr, osr, gdal
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')

def checkGDAL():
    print("holi")
    ProbarGDAL_OGR()
    print("adiós")

def ProbarGDAL_OGR():
    # Se comprueba la versión
    version_num = int(gdal.VersionInfo('VERSION_NUM'))

    print('Versión de GDAL/OGR: ', version_num)
    print('----------')
    print(' ')
    if version_num < 1100000:
        sys.exit('ERROR: Python bindings of GDAL 1.10 or later required')

    # Listar drivers Vectoriales
    cnt = ogr.GetDriverCount()
    formatsList = []  # Empty List

    for i in range(cnt):
        driver = ogr.GetDriver(i)
        driverName = driver.GetName()
        if not driverName in formatsList:
            formatsList.append(driverName)

    formatsList.sort() # Sorting the messy list of ogr drivers

    print(' ')
    print('----------')
    print('Drivers vectoriales')
    print('----------')
    print(' ')
    for i in formatsList:
        print(i)

    
    # Listar drivers Ráster
    cnt = gdal.GetDriverCount()
    formatsList = []  # Empty List

    for i in range(cnt):
        driver = gdal.GetDriver(i)
        driverName = driver.LongName
        # driverName = driver.ShortName
        if not driverName in formatsList:
            formatsList.append(driverName)

    formatsList.sort() # Sorting the messy list of ogr drivers

    print(' ')
    print('----------')
    print('DTodos los Drivers')
    print('----------')
    print(' ')
    for i in formatsList:
        print(i)
    print(' ')


    # Se habilitan las excepciones para tener más control
    gdal.UseExceptions()

    # Se intenta abrir un archivo
    ds = gdal.Open('test.tif')


    def gdal_error_handler(err_class, err_num, err_msg):
        errtype = {
                gdal.CE_None:'None',
                gdal.CE_Debug:'Debug',
                gdal.CE_Warning:'Warning',
                gdal.CE_Failure:'Failure',
                gdal.CE_Fatal:'Fatal'
        }
        err_msg = err_msg.replace('\n',' ')
        err_class = errtype.get(err_class, 'None')
        print( 'Error Number: %s' % (err_num))
        print( 'Error Type: %s' % (err_class))
        print( 'Error Message: %s' % (err_msg))

    # install error handler
    gdal.PushErrorHandler(gdal_error_handler)

    # Raise a dummy error
    gdal.Error(1, 2, 'test error')

    #uninstall error handler
    gdal.PopErrorHandler()

    gdal.DontUseExceptions()

    

if __name__ == "__main__":
    checkGDAL()
