# Integration Engineer Coding Challenge
# 2020@josesalgueiro, all rights reserved

from urllib.request import urlopen, build_opener, Request
import xml.etree.ElementTree as ET
import json

def xml_to_json():

    # --- General Parameters --- 
    xml_dict = {"members": None} # we'll store all data here
    xml_list = []   

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
                elem_dict = {} # a dict for each element
                address_dict = {} # dict for the address node of each element
                elem_dict["lastName"] = elem.find("last_name").text
                elem_dict["firstName"] = elem.find("first_name").text
                elem_dict["mobile"] = elem.find("phone").text
                elem_dict["fullName"] = elem_dict["firstName"] + " " + elem_dict["lastName"]
                elem_dict["chartId"] = elem.find("bioguide_id").text
                full_address = elem.find("address").text.split()

                # WARNING: This is error prone and takes advantage of the fact that the addresses are
                # all the same. Adding addresses with another configuration will create faulty addresses.
                address_dict["street"] = " ".join(full_address[0:2])
                
                # WARNING: This is error prone and takes advantage of the fact that the addresses are
                # all the same. Adding addresses with another configuration will create faulty city names.
                # I added a check for city names composed with either 1 or 2 words.
                if len(full_address) < 8:
                    address_dict["city"] = " ".join(full_address[-2])
                else:
                    address_dict["city"] = " ".join(full_address[-3:-1])

                address_dict["state"] = elem.find("state").text
                # WARNING: This is error prone and takes advantage of the fact that the addresses are
                # all the same. Adding addresses with another configuration will create invalid postal codes.
                address_dict["postal"] = full_address[-1]

                elem_dict["address"] = [address_dict]
                xml_list.append(elem_dict)
            xml_dict["members"] = xml_list
            xml_json_str = json.dumps(xml_dict)
            xml_json = json.loads(xml_json_str)
            print("Done", end="\n\n")
            print("Generated JSON: ")
            return xml_json
        except Exception as e:
            print("\nAn Error occurred while processing the XML Data: ", str(e))
            return None
        
    except Exception as e:
        print("\nAn error Occurred while trying to retrieve data from API: ", str(e))
        
if __name__ == '__main__':
    json_str = xml_to_json()
    if json_str is not None:
        print(json_str)


