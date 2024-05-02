import csv
import json
import os 
from flask import Flask
from markupsafe import escape
from flask_cors import CORS

#run: flask --app backend-server/main run


app = Flask(__name__) CORS(app)




@app.route("/listed-assets")
def listed_assets():
    
    output = []

    
    index = 0
    with open("final-datasets/listed_investments.csv", mode ='r') as file:
        csvFile = csv.reader(file)
        print
        
        for row in csvFile:
            index += 1 
            if index == 1:
                continue
            

            holdings = []

            if row[6] == "Y":
                
                for file_name in os.listdir("Data-Collection/json-outputs"):
                    
                    if file_name.replace('.json','') == row[0]:
                        file_path = os.path.join("Data-Collection/json-outputs", file_name)
                        source = file_name.split('.')[0]
                        fundData = json.load(open(file_path))

                        holdings = fundData["restricted assets"]


                        money_holdings = []

                        for investment in holdings:
                            if investment["holding wt"] == '' or investment["holding wt"] == None:
                                weight = 0
                            else:
                                weight = investment["holding wt"] 
                            money_holdings.append({"security name": investment["security name"], "ammount invested": float(weight)*float(row[2])})
                            


            output.append({
                "Asset Name":row[0],
                "Asset Type":row[1],
                "Total Investment":row[2],
                "Funding Sources": [{"Source:":"UCRP Investment", "Ammount":row[3]},{"Source:":"GEP Investment", "Ammount":row[4]}],
                "Holdings (restricted)":money_holdings
            })
    
    return output

def company_composition(filePath):
    output = json.load(open(filePath))
    del output["invesmtent names list"]
    return output

@app.route("/company-composition/<class_grouping>/<estimation>")
def composition(class_grouping,estimation):
    return company_composition(f"final-datasets/full_investments_{escape(estimation)}_estimation_{escape(class_grouping)}_class_grouping.json")



@app.route("/company-composition/<class_grouping>/<estimation>/<query>")
def composition_search(class_grouping,estimation,query):

    data = json.load(open(f"final-datasets/full_investments_{escape(estimation)}_estimation_{escape(class_grouping)}_class_grouping.json"))
    
    query = escape(query)

    suggestions = sorted(
        [name for name in data["invesmtent names list"] if query in name.lower()],
        key=lambda name: name.lower().find(query)
    )

    suggestions = suggestions[:10]

    return suggestions

if __name__ == '__main__':
    app.run()