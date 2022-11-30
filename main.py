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

                    # Process file for scraping
                    with open(filepath, 'r') as file:
                        parse_string = file.read()
                    # Mark end of template
                    parse_string = parse_string.replace(

                    )
                    soup = BeautifulSoup(parse_string, "html.parser")

                    # mandant = re.findall("(-.*?-)", filename, flags=re.DOTALL)[0][1:-1]
                    mandant = filename[0:4]

                    # JSON Structure
                    # High-level dict for generating json
                    json_dict[mandant] = {}
                    # Dict to encapsulate single templates
                    count = 1
                    template_dict = json_dict[mandant]
                    # Dict where variables/values are saved
                    var_dict = {}

                    var_tags = soup.find_all("poc-variable")
                    for tag in var_tags:
                        # Eliminate \xa0
                        value = tag.text
                        if value == "\xa0":
                            value = ""

                        # Close and var_dict and append it to template_dict
                        if tag['id'] == "new-template":
                            key = "Template " + str(count)
                            count += 1
                            template_dict[key] = var_dict
                            var_dict = {}
                            continue

                        # If double value [WIEDERHOLEN], add to array
                        if tag['id'] in var_dict:
                            var_dict[tag['id']].append(value)
                        # Else create new array entry
                        else:
                            var_dict[tag['id']] = [value]
                    template_dict["Template " + str(count)] = var_dict

                    # Create JSON in POC-tests sub-folder
                    write_path = directory + '/values.json'
                    with open(write_path, 'w') as file_to_write:
                        json.dump(json_dict, file_to_write, ensure_ascii=False, indent=4)
                        print("JSON created at: ", write_path)

                    pp = pprint.PrettyPrinter(indent=2)
                    pp.pprint(json_dict)

                except:
                    print("Error occurred in file: ", filename)
