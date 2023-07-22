import json
import os
import glob
import re

current_dir = os.path.dirname(os.path.realpath(__file__))
json_files = glob.glob(os.path.join(current_dir, "*.json")) 

#Match only strings that start with "Map" followed by exactly three digits (0-9)
map_file_pattern = re.compile(r'^Map\d{3}\.json$')

for json_file in json_files:
    with open(json_file, encoding='utf-8-sig') as file:
        json_data = json.load(file)

    output_filename = os.path.splitext(json_file)[0] + '.csv'  

    if "CommonEvents.json" in json_file:
        try:
            if os.path.exists(output_filename):  
                os.remove(output_filename)
        except OSError as e:
            print(f"Error: {e.strerror}. {e.filename}")
        
        print("Processing: " + json_file)
        with open(output_filename, "w", encoding='utf-8-sig') as f:
            for n in range(0, len(json_data)):
                data = json_data[n]
                if data is not None:
                    for x in range(0, len(json_data[n]["list"])):
                        if json_data[n]["list"][x]["code"] == 101:
                            #Check if actor name is empty and replace it with "語り手"
                            if json_data[n]["list"][x]["parameters"][4] == "": 
                                f.write("語り手" + "\t")
                            else: 
                                f.write(json_data[n]["list"][x]["parameters"][4] + "\t")
                        if json_data[n]["list"][x]["code"] == 401:
                            if json_data[n]["list"][x-1]["code"] == 401 and json_data[n]["list"][x+1]["code"] == 401: 
                                f.write(json_data[n]["list"][x]["parameters"][0].replace('"', '""') + '\n')
                            if json_data[n]["list"][x-1]["code"] == 401 and json_data[n]["list"][x+1]["code"] != 401: 
                                f.write(json_data[n]["list"][x]["parameters"][0].replace('"', '""') + '"\n')
                            if json_data[n]["list"][x-1]["code"] != 401 and json_data[n]["list"][x+1]["code"] == 401: 
                                f.write('"' + json_data[n]["list"][x]["parameters"][0].replace('"', '""') + '\n')
                            if json_data[n]["list"][x-1]["code"] != 401 and json_data[n]["list"][x+1]["code"] != 401: 
                                f.write('"' + json_data[n]["list"][x]["parameters"][0].replace('"', '""') + '"\n')

    elif map_file_pattern.match(os.path.basename(json_file)):
        try:
            if os.path.exists(output_filename):  
                os.remove(output_filename)
        except OSError as e:
            print(f"Error: {e.strerror}. {e.filename}")

        print("Processing: " + json_file)
        with open(output_filename, "w", encoding='utf-8-sig') as f:
            f.write("ID" + "\t" + "Name" + "\t" + "Actor" + "\t" + "Text" + "\t" + "Note" + "\n")
            for n in range(0, len(json_data["events"])):
                event = json_data["events"][n]
                if event is not None:
                    for x in range(0, len(json_data["events"][n]["pages"][0]["list"])):
                        if json_data["events"][n]["pages"][0]["list"][x]["code"] == 101:
                            f.write(str(json_data["events"][n]["id"]) + "\t" + json_data["events"][n]["name"] + "\t") 
                            #Check if actor name is empty and replace it with "語り手"
                            if json_data["events"][n]["pages"][0]["list"][x]["parameters"][4] == "":
                                f.write("語り手" + "\t")
                            else:
                                f.write(json_data["events"][n]["pages"][0]["list"][x]["parameters"][4] + "\t")

                        if json_data["events"][n]["pages"][0]["list"][x]["code"] == 401:
                            code_minus_1 = json_data["events"][n]["pages"][0]["list"][x-1]["code"]
                            code_plus_1 = json_data["events"][n]["pages"][0]["list"][x+1]["code"]
                            params = json_data["events"][n]["pages"][0]["list"][x]["parameters"][0].replace('"', '""')

                            if code_minus_1 == 401 and code_plus_1 == 401:
                                f.write(params + '\t')
                            elif code_minus_1 == 401 and code_plus_1 != 401:
                                f.write(params + '"\t')
                            elif code_minus_1 != 401 and code_plus_1 == 401:
                                f.write('"' + params + '\t')
                            elif code_minus_1 != 401 and code_plus_1 != 401:
                                f.write('"' + params + '"\t')
                            f.write(json_data["events"][n]["note"] + "\n") 
