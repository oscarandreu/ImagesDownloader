import hashlib
import os
from PIL import Image
import imagehash
import shutil
from multiprocessing.dummy import Pool as ThreadPool
import piexif

class ImageHelper(object):

    def  __init__(self):
        self.hashList = {}
        self.it = 0
        self.path = None

    def __del__(self):
        self.hasher = None
        self.hashList = None


    def saveFile(self, name, data):
        f = open(name, 'wb')
        f.write(data)
        f.close()
        

    def getFileHash(self, file):
        image = None
        try:            
            image = Image.open(file)
            h = str(imagehash.dhash(image))
        except:
            h = 'error'
        finally:
            if image != None:
                image.close()
        return h

    def getImageHash(self, image):        
        hasher = hashlib.md5()
        hasher.update(image)
        return hasher.hexdigest()


    def checkDuplicate(self, f):
        self.it += 1

        fp = os.path.join(self.path, f)
        h = self.getFileHash(fp)
        if h == 'error':
            os.rename(fp, os.path.join(self.path, '____'+f+'_ERROR.jpg'))

        elif h in self.hashList:            
            print('dupe')
            try:
                #shutil.copy(self.hashList[h], os.path.join(self.path, '__'+h+'_000_.jpg'))
                #os.rename(fp, os.path.join(self.path, '__'+h+'_'+str(self.it)+'.jpg'))
                os.remove(fp)
            except:
                print('error')

        else:
            self.hashList[h] = fp
            #os.rename(fp, os.path.join(path, h + '.jpg'))
            print(h)

    def extracMetadataFromImage(self, file):
        h = False
        try:    
            fp = os.path.join(self.path, file)        
            exif_dict = piexif.load(fp)
            for ifd in ("0th", "Exif", "GPS", "1st"):
                for tag in exif_dict[ifd]:
                    print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])
                    h = True
            if(not h):
                print("No EXIF data\n")
        except:            
            print("Error\n")
        return h

    def extracMetadataFromFiles(self, path):
        self.path = path

        pool = ThreadPool(10)
        files = os.listdir(self.path)
        pool.map(self.extracMetadataFromImage, files) 
        pool.close()
        pool.join()

    def cleanDuplicates(self, path):
        self.it = 0
        self.path = path

        pool = ThreadPool(10)
        files = os.listdir(self.path)
        pool.map(self.checkDuplicate, files) 
        pool.close()
        pool.join()