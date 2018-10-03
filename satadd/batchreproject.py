import os

def reproject(dest,output,epsg):
    for root, dirs, files in os.walk(dest, topdown=False):
        [head,tail]=os.path.split(root)
        destfold=output
        if not os.path.isdir(destfold):
            os.makedirs(destfold)
            print("Creating folder "+str(destfold))
        try:
            for items in os.listdir(root):
                if items.endswith('.tif'):
                    print('Processing Rasters in '+str(root))
                    base=os.path.join(root,items)
                    target=os.path.join(destfold,items)
                    os.system('gdalwarp -t_srs EPSG:'+str(epsg)+' '+base+' '+target)
        except Exception as e:
            print(e)
#4326
