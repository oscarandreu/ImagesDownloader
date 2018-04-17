from os.path import join, dirname, abspath, exists
from os import makedirs
from classes.providerOne import ProviderOne
from classes.downloadPool import DownloadPool
from multiprocessing.dummy import Pool as ThreadPool
from classes.imageHelper import ImageHelper
import time

partTypeId = 1896
partTypeName = "disk_brake_rotot"


class Main():
    
    def __init__(self):
        self.page = 1
        self.pages = None
        self.pages_size = 100
        self.path  = join(dirname(abspath(__file__)), join('images', partTypeName))
        if not exists(self.path):
            makedirs(self.path)        
        self.pool = ThreadPool(20) 
        self.downloader = ProviderOne(partTypeId, self.pages_size)
        self.downloadPool = DownloadPool(self.path)


    def downloadImagesList(self):        
        while self.pages is None or self.page < self.pages:    
            print("PAGE: " + str(self.page))
            
            p, result = self.downloader.getImagesFromPage(self.page) 
            if(self.pages is not None and p is not None):
                self.pages = p
            if(len(result) > 0):
                self.pool.map(self.downloadPool.downloadImage, result)

            self.page += 1
            time.sleep(1)

        self.pool.close()
        self.pool.join()

        img = ImageHelper()
        img.cleanDuplicates(main.path)
        


if __name__ == "__main__":
    print("START:: " + partTypeName)
    main = Main()
    main.downloadImagesList()
    print("DONE:: " + partTypeName)
