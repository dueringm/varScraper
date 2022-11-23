import os
import pprint
import re

from bs4 import BeautifulSoup


# Set directory here:
directory = "server"

# Globals
json_dict = {}


for filename in os.listdir(directory):
    try:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:

            mandant = re.findall("(-.*?-)", filename, flags=re.DOTALL)[0][1:-1]

            soup = BeautifulSoup(file, "html.parser")
            soup_string = str(soup.prettify())

            var_tags = soup.find_all("datavariable")

            json_dict[mandant] = {}
            var_dict = json_dict[mandant]

            for tag in var_tags:
                # If double value, add to array
                if tag['id'] in var_dict:
                    var_dict[tag['id']].append(tag.text)
                # Else create new array entry
                else:
                    var_dict[tag['id']] = [tag.text]
    except:
        print("Error occured in file: ", filename)

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(json_dict)
