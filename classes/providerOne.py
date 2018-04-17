import urllib3
import json
import math

class ProviderOne:

    def __init__(self, partTypeId, pageSize):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)        
        
        self.http = urllib3.PoolManager()
        self.partTypeId = partTypeId
        self.pageSize = pageSize

    def getPage(self, page):  
        bodyData = {
            'getAutoCareSearchResults': {
                'perPage': self.pageSize,
                'page': page,    
                'baseVehicleRegion': "USA",
                'partTypeIds': self.partTypeId,
                'includeParts': True,
                'includeBrandFacets': False
            }
        }
        response = self.http.request(
            'POST',
            'https://foo.bar.com',
            body = json.dumps(bodyData).encode('utf-8'),
            headers={
                'Authorization' : 'Basic FOOBAR='
            }, timeout=10.0)
        return json.loads(response.data)

    def getImagesFromPage(self, page):
        images = []
        try:
            response = self.getPage(page)        
            items = response['parts']
            pages = math.ceil(response['total'] / self.pageSize)
            
            for item in items:
                # Ugly checks
                if('piesItem' in item and 'digitalAssets' in item['piesItem'] and len(item['piesItem']) > 0 and len(item['piesItem']['digitalAssets']) > 0 and 'imageURL1600' in item['piesItem']['digitalAssets'][0]):
                    imgUrl = item['piesItem']['digitalAssets'][0]['imageURL1600']
                    if imgUrl != "":
                        images.append(imgUrl)
                else:
                    print("No image")
        except:
            pages = None
            
        return pages, images     