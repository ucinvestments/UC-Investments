import csv
import json
import os 

def convert_func(path):
  output = {"restricted assets":[],
                "non restricted assets": [],
                }

  inResSwitch = False
  inPubSwitch = False
  skipLine = 0

  testcount = 0 

  with open(path, mode ='r')as file:
    csvFile = csv.reader(file)
    for line in csvFile:  

      # if hellscape



      if line[0] == "Fund Name (AS CITED)":
        output["Fund Name (AS CITED)"] = line[1]

      if line[0] == "Internal Name":
        output["Internal Name"] = line[1]

      if line[0] == "Restricted y/n":
        output["Restricted"] = line[1]

      if line[0] == "Ammount of companies in fund (restricted)":
        output["Ammount of companies in fund (restricted)"] = line[1]

      if line[0] == "Source" and not inResSwitch:
        output["Source (unrestricted)"] = line[1]

      if line[0] == "Source" and not inResSwitch and not inPubSwitch:
        output["Source (restricted)"] = line[1]

      #I'm a dummy and re-used the same names in the csv for both restricted and unrestricted
      if line[0] == "Filing Date (restricted)" and not inResSwitch:
        output["Filing Date (unrestricted)"] = line[1]

      if line[0] == "Filing Date (restricted)" and not inResSwitch and not inPubSwitch:
        output["Filing Date (restricted)"] = line[1]

      if line[0] == "Ammount of companies in fund (restricted)" and not inResSwitch:
        output["Ammount of companies in fund (restricted)"] = line[1]
      
      if line[0] == "Ammount of companies in fund (restricted)" and not inResSwitch and not inPubSwitch:
        output["Ammount of companies in fund (unrestricted)"] = line[1]
      
      if line[0] == "Note:":
        output["Note"] = line[1]

      if line[0] == "Restricted Data:":
      
        inResSwitch = True 
        skipLine = 1
        continue 
        # skipLine = 1 
      
      if line[0] == "Unrestricted Data Divider":
          inResSwitch = False 
          inPubSwitch = True 
          skipLine = 5
          
          continue  

      if line[0] == "Fund Name:" or line[0] == "Unrestricted Fund Name": # this is 
        output["Unrestricted Fund Name"] = line[1]

      if inResSwitch:
      
        if skipLine > 0:
          skipLine = skipLine - 1
          continue
        output["restricted assets"].append({"security name":line[0], "holding wt":line[1]})

      if inPubSwitch:

        
        if skipLine > 0:
          skipLine = skipLine - 1
          continue

        # if testcount < 20:
        #   print('in pubswitch', line)
        # testcount += 1
        output["non restricted assets"].append({"security name":line[0], "holding wt":line[1]})


  #print(output)
  return output 


def iter_in_dir(input_path, output_path):
  for file_name in os.listdir(input_path):
    if file_name.endswith('.csv'): 
        file_path = os.path.join(input_path, file_name)
        source = file_name.split('.')[0]  

        with open(f"{output_path}{source}.json", 'w') as f:
          print(f"{output_path}{source}.json")
          json.dump(convert_func(file_path), f)

        

            
iter_in_dir("Data-Collection/csv-files", "Data-Collection/json-outputs/")