from requests_html import HTMLSession
from datetime import datetime

from .GarbageCollection import GarbageCollection

class StadtreinigungHamburg:
    def get_garbage_collections(self, street, number, use_asid=False, use_hnid=False):

        street = street.lower()
        street = street.replace(u"ä", u"ae")
        street = street.replace(u"ö", u"oe")
        street = street.replace(u"ü", u"ue")
        street = street.replace(u"ß", u"ss")

        session = HTMLSession()
        params = {
            'bestaetigung': 'true',
            'mode': 'search',
            'suche': 'Abfuhrtermine+suchen',
        }
        if (use_hnid):
            params['hnId'] = number
        else:
            params['hausnummer'] = number

        if (use_asid):
            params['asId'] = street
        else:
            params['strasse'] = street

        r = session.get('https://www.stadtreinigung.hamburg/privatkunden/abfuhrkalender/', params=params)
        collections = []

        # check for errors
        possible_err = r.html.find('div.adresse')
        if(len(possible_err) > 0):
            print(possible_err[0].text)
            if("Straße" in possible_err[0].text):
                raise StreetNotFoundException("street not found.")
            elif("Hausnummer" in possible_err[0].text):
                hausnummer_sel = r.html.find('#hausnummer')
                if(len(hausnummer_sel) == 1):
                    hnids = [(option.text, option.attrs['value']) for option in r.html.find('#hausnummer option')[1:]]
                    raise StreetNumberNotFoundException("street number not found.", hnids)
                raise StreetNumberNotFoundException("street number not found and recommendations were not available.", [])

        uuid = r.html.find("input[name=asId]")[0].attrs["value"]
        uuid += "-" + r.html.find("input[name=hnId]")[0].attrs["value"]

        for tr in r.html.find("#abfuhrkalender table tr"):
            content = [td.text for td in tr.find("td")]
            if len(content) == 3:
                collection = GarbageCollection(datetime.strptime(content[0][4:], '%d.%m.%Y'), content[1], content[2], uuid + "-" + content[1])
                collections.append(collection)

        return collections

class StreetNotFoundException(Exception):
    pass

class StreetNumberNotFoundException(Exception):
    pass

