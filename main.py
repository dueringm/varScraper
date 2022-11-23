import json
import os
import pprint
import re

from bs4 import BeautifulSoup


# Set directory here:
master_directory = ""

# Iterate over folders in POC-Tests
for folder_name in os.listdir(master_directory):
    directory = os.path.join(master_directory, folder_name)
    if os.path.isdir(directory):

        # Iterate over files in folder
        for filename in os.listdir(directory):
            if filename.endswith(""):

                json_dict = {}
                try:
                    filepath = os.path.join(directory, filename)

                    # Parse file for scraping
                    with open(filepath, 'r') as file:
                        soup = BeautifulSoup(file, "html.parser")

                    mandant = re.findall("(-.*?-)", filename, flags=re.DOTALL)[0][1:-1]
                    var_tags = soup.find_all("poc-variable")

                    json_dict[mandant] = {}
                    var_dict = json_dict[mandant]

                    for tag in var_tags:
                        # If double value, add to array
                        if tag['id'] in var_dict:
                            var_dict[tag['id']].append(tag.text)
                        # Else create new array entry
                        else:
                            var_dict[tag['id']] = [tag.text]

                    # Create JSON in POC-tests sub-folder
                    write_path = directory + '/values.json'
                    with open(write_path, 'w') as file_to_write:
                        json.dump(json_dict, file_to_write, ensure_ascii=False, indent=4)
                        print("JSON created at: ", write_path)

                    pp = pprint.PrettyPrinter(indent=2)
                    pp.pprint(json_dict)

                except:
                    print("Error occurred in file: ", filename)
