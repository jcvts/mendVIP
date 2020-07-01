# Integration Engineer Coding Challenge
# 2020@josesalgueiro, all rights reserved

from urllib.request import urlopen, build_opener, Request
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
import json

def xml_to_json():

    # --- General Parameters --- 
    xml_dict = {"members": None} # we'll store all data here
    xml_list = []
    elem_dict = {"firstName": None, "lastName": None, "fullName": None,
                 "chartId": None, "mobile": None, "address": None} # a dict for each element
    address_dict = {"street": None, "city": None, "state": None, "postal": None} # dict for the address node of each element

    # --- Connection Parameters ---    
    target_url = 'https://www.senate.gov/general/contact_information/senators_cfm.xml'
    headers = {"User-Agent": "Mozilla/5.0"}
    req = Request(target_url, data=None, headers = headers)
   
    # --- Downloading XML data from API ---
    try:
        print("Connecting to API and retrieving data...", end='')
        f = urlopen(req)
        xml_data = f.read().decode('utf-8')
        # read the XML data, retrieve the relevant elements and create a dictionary with them.
        root = ET.fromstring(xml_data)
        print("Done", end="\n\n")

        # --- Processing Downloaded Data ---
        try:
            print("Processing downloaded data...", end="")
            for elem in root.findall("member"):
                elem_dict["lastName"] = elem.find("last_name").text
                elem_dict["firstName"] = elem.find("first_name").text
                elem_dict["fullName"] = elem_dict["firstName"] + " " + elem_dict["lastName"]
                elem_dict["chartId"] = elem.find("bioguide_id").text
                address_dict["street"] = elem.find("address").text
                address_dict["city"] = "Washington DC"
                address_dict["state"] = elem.find("state").text
                address_dict["postal"] = "20510"
                elem_dict["address"] = [address_dict]
                xml_list.append(elem_dict)
            xml_dict["members"] = xml_list
            xml_json_str = json.dumps(xml_dict)
            xml_json = json.loads(xml_json_str)
            print("Done", end="\n\n")
            print("Generated JSON: ")
            print(xml_json)
        except Exception as e:
            print("\nAn Error occurred while processing the XML Data: ", str(e))
        
    except Exception as e:
        print("\nAn error Occurred while trying to retrieve data from API: ", str(e))
        
if __name__ == '__main__':
    xml_to_json()


