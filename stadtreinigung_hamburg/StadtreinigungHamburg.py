import logging
from requests_html import HTMLSession
from datetime import datetime
import dateutil.parser

from .GarbageCollection import GarbageCollection

class StadtreinigungHamburg:
    def get_garbage_collections(self, street, number, use_asid=False, use_hnid=False):

        logger = logging.getLogger(__name__)

        session = HTMLSession()
        
        if (use_asid ^ use_hnid):
            raise Exception("Provide either asid AND hnid or provide street and street number. Mixed mode is not supported in this version!")

        if (use_asid):
            asId = street
            hnId = number
            logger.debug(F"asId is {asId}, hnId is {hnId}")
        else:
            r = session.post('https://www.stadtreinigung.hamburg/abfuhrkalender?tx_srh_pickups%5Baction%5D=addresses&tx_srh_pickups%5Bcontroller%5D=PickUps&type=10002&cHash=549969ec3dc1f708797c7e8762ea3b2b',
                    data= {
                        'tx_srh_pickups[street]':street,
                        'tx_srh_pickups[limit]':1
                    },
                    headers={
                        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
                        'Referer': 'https://www.stadtreinigung.hamburg/abfuhrkalender/',
                        'Origin': 'https://www.stadtreinigung.hamburg',
                        'Content-Length': '333',
                        'Connection': 'keep-alive',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin'
                    }
                )
            if(r.status_code!=200): raise Exception(F"Fetching asId and hnId failed: Status code was {r.status_code}.")

            streets = r.json()
            logger.debug(F"found {len(streets)} street(s)")

            if(len(streets) == 0): raise StreetNotFoundException(F"Street not found with name {street}.")

            asId = streets[0]["asId"]
            logger.debug(F"asId is {asId}")

            hnIds = streets[0]["hnIds"]
            logger.debug(F"There are {len(hnIds)} numbers in this street.")
            if(len(hnIds) == 0): raise StreetNumberNotFoundException(F"The street has no numbers.", [])

            hn = next((item for item in hnIds if item["name"] == number), None)
            if(hn == None):
                logger.info("Retrying house number search with casefold")
                hn = next((item for item in hnIds if item["name"].casefold() == number.casefold()), None)
                
            if(hn == None):
                raise StreetNumberNotFoundException(F"The street has {len(hnIds)} house numbers, but {number} is none of them.", [hn["name"] for hn in hnIds])
            hnId = hn["hnId"]
            logger.debug(F"hnId is {hnId}")
        

        # now fetch the actual garbage pickups
        r = session.get(F"https://www.stadtreinigung.hamburg/abfuhrkalender/?tx_srh_pickups%5Bstreet%5D={asId}&tx_srh_pickups%5Bhousenumber%5D={hnId}&tx_srh_pickups%5BisAllowedOwner%5D=1")
        if(r.status_code!=200): raise Exception(F"Fetching step2 failed: Status code was {r.status_code}!")
        
        collections = []

        uuid = F"{asId}-{hnId}"
        logger.debug(F"uuid is {uuid}")
        
        rows = r.html.find("tbody tr")
        logger.debug(F"found {len(rows)} garbage collection data rows.")
        for tr in rows:
            content = [td.text for td in tr.find("td")]
            
            for type in content[1].split("\n"):
                collection = GarbageCollection(parseDate(content[0]), type, "interval unknown", uuid + "-" + type)
                collections.append(collection)

        logger.debug("succeeded with fetching and parsing!")
        return collections

def parseDate(text):
    return dateutil.parser.parse(text)

class StreetNotFoundException(Exception):
    pass

class StreetNumberNotFoundException(Exception):
    pass

