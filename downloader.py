
from classes.imageHelper import ImageHelper
import urllib3
import json
import os
from os.path import join, dirname, abspath, exists
from multiprocessing.dummy import Pool as ThreadPool
from io import BytesIO

partTypeId = 1704
partTypeName = "Disc Brake Caliper"

page = 1
pages = 0
pagesSize = 100
downloaded = 0

def saveFile(name, data):
    f = open(name, 'wb')
    f.write(data)
    f.close()

def getImagesList(page):  
    bodyData = {
        'getAutoCareSearchResults': {
            'perPage': pagesSize,
            'page': page,    
            'baseVehicleRegion': "USA",
            'partTypeIds': partTypeId,
            'includeParts': True,
            'includeBrandFacets': False
        }
    }
    response = http.request(
        'POST',
        'https://foo.bar.com',
        body = json.dumps(bodyData).encode('utf-8'),
        headers={
            'Authorization' : 'Basic FOOBAR='
        })
    return json.loads(response.data)


def downloadImage(imgUrl):
    global downloaded

    response = http.request('GET', imgUrl, preload_content=False)
    imageData = BytesIO(response.data)

    # fileData = bytearray()
    # while True:
    #     chunk = response.read(100)
    #     if not chunk:
    #         break
    #     fileData.append(chunk)
    response.release_conn()

    #name = join(partTypeName, imgUrl.rsplit("/", 1)[1])
    name = img.getImageHash(imageData)
    saveFile(name, imageData)
    
    downloaded += 1
    print(str(downloaded) + ':: ' + name)


def getImagesFromPage(page):
    global pages

    response = getImagesList(page)        
    items = response['parts']
    if pages == 0:
        pages = response['total'] / pagesSize

    images = []
    for item in response['parts']:
        # Ugly checks
        if('piesItem' in item and 'digitalAssets' in item['piesItem'] and len(item['piesItem']) > 0 and len(item['piesItem']['digitalAssets']) > 0 and 'imageURL1600' in item['piesItem']['digitalAssets'][0]):
            imgUrl = item['piesItem']['digitalAssets'][0]['imageURL1600']
            if imgUrl != "":
                images.append(imgUrl)
        else:
            print("No image")

    if len(images) > 0:
        pool.map(downloadImage, images)        
 

        

if __name__ == "__main__":  # guard for multi-platform use

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager()

    path  = join(dirname(abspath(__file__)), partTypeName)
    img = ImageHelper()

    # make the Pool of workers
    pool = ThreadPool(10) 

    if not exists(partTypeName):
        os.path.makedirs(partTypeName)

    while pages == 0 or page < pages:    
        print("PAGE: " + str(page))
        getImagesFromPage(page)
        page += 1
        print("downloaded: " + str(downloaded))

    print("::::::::::::::::::::::::::::::::::::::::::")
    print("ALL WORK DONE")
    print("ITEMS:: " + str(downloaded))
    print("::::::::::::::::::::::::::::::::::::::::::")