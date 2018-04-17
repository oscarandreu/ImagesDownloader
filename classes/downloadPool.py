from multiprocessing.dummy import Pool as ThreadPool
from os.path import join
from io import BytesIO
import urllib3
import time
from classes.imageHelper import ImageHelper

class DownloadPool:

    def __init__(self, path):
        self.http = urllib3.PoolManager()
        self.path = path
        self.finalize = False
        self.imageHelper = ImageHelper()
        self.downloadedImages = 0

    def downloadImage(self, imgUrl):
        try:
            response = self.http.request('GET', imgUrl, preload_content=False, timeout=10.0)
            data = BytesIO(response.data).getvalue()
            response.release_conn()
        except:
            return 

        name = self.imageHelper.getImageHash(data)
        fullName = join(self.path, name  + '.jpg')
        self.imageHelper.saveFile(fullName, data)        
        self.downloadedImages += 1
        print(str(self.downloadedImages) + ':: ' + name)