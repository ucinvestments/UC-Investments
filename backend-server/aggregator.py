# import requests
import os 
import csv
import json 
import re

from fuzzywuzzy import process, fuzz
# def get_stock_ticker(api_key,company_name):
#     url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={api_key}'
#     r = requests.get(url)
#     data = r.json()
    

#     print(data)

#     for match in data["bestMatches"]:
#         if match["4. region"] == 'United States':
#             return match["1. symbol"]
        
    
#     return data["bestMatches"][0]["1. symbol"]


# print(get_stock_ticker("1H0KGFAKR59J8UHY", "berkshire hathaway inc class b"))


def subDictSearch(list_to_search, search_field, search_term):
    index = 0 
    for item in list_to_search:
        if item[search_field] == search_term:
            return item , index 
        
        index += 1
        
    return None, None

def parse_csv(csv_list, search, search_index, return_index):
    
    for line in csv_list:
        if line[search_index] == search:
            return line[return_index]
        

    return None

def aggregate(dir_path, all_fund_data_path, output_path, restrict, consolidate_voting_shares):


    total_investments = {"invesmtent names list":[], "summed investments":[], "unknown money":0}
    total_sum = 0
    total_upper_sum = 0


    for file_name in os.listdir(dir_path):
        if file_name.endswith('.json'): 
            file_path = os.path.join(dir_path, file_name)
            source = file_name.split('.')[0]

            with open(all_fund_data_path, mode ='r') as file:
                csvFile = csv.reader(file)

                money_in_fund = parse_csv(csvFile, source, 0, 2)
              
                if money_in_fund == None:
                    raise KeyError()
                
                total_upper_sum += int(money_in_fund)
                
                
                fundData = json.load(open(file_path))
                fundSum = 0 

                if restrict == True:
                    holdings_list = fundData["restricted assets"]

                else:
                    if len(fundData["restricted assets"]) > len(fundData["non restricted assets"]):
                        holdings_list = fundData["restricted assets"]

                    else:
                        holdings_list = fundData["non restricted assets"]
                
                
                weightSum = 0
                for investment in holdings_list:
                    
                    securityName = investment["security name"].lower().replace('corporation', "corp").replace("incorporated", "inc")
                    
                    
                    securityName = re.sub(r'class (.*)', ' ', securityName)
                    securityName = re.sub(r'cl (.*)', ' ', securityName)
                    

                   
                    if securityName not in total_investments["invesmtent names list"]:

                        match = process.extractOne(securityName, total_investments["invesmtent names list"], scorer=fuzz.token_sort_ratio)
                        if match and match[1] >= 95:
                            securityName = match[0]
                        else:
                            total_investments["invesmtent names list"].append(securityName)
                            total_investments["summed investments"].append(
                                {
                                    "asset":securityName,
                                    "total investment":0,
                                    "funding sources":[]
                                }

                        )
                    
                    dictObj, index = subDictSearch(total_investments["summed investments"], "asset", securityName)

                    if index == None:
                        raise NameError #wrong error type but idc, for debugging
                    

                    if investment["holding wt"] == None or len(investment["holding wt"]) == 0:
                        holding_weight = 0

                    else:
                        holding_weight = float(investment["holding wt"])


                    if holding_weight > 1: #fixes arrowstreet percents
                        holding_weight = holding_weight * .01

                    total_investments["summed investments"][index]["total investment"] += float(money_in_fund) * holding_weight
                    total_investments["summed investments"][index]["funding sources"].append({
                        "fund name:":source, 
                        "ammount_invested": float(money_in_fund) * holding_weight} )
                    total_sum += float(money_in_fund) * holding_weight
                    fundSum += float(money_in_fund) * holding_weight
                     
                    weightSum += holding_weight
                print(source, "Discrepancy between money in fund-fundsum:", int(money_in_fund)-fundSum)
                print("FUND WEIGHT SUM", source, weightSum)

                

                
    print("total disc",total_upper_sum-total_sum)
    with open(f"{output_path}FULLINVESTMENTS.json", 'w') as f:
          
          json.dump(total_investments, f)     

    



aggregate("Data-Collection/json-outputs", "Data-Collection/combined_investments - combined_investments.csv", "/Users/alexforman/Documents/GitHub/UC-Investments/backend-server/", False, True)