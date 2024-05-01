import os
import pandas as pd
from fuzzywuzzy import process, fuzz

#reweighting function to make non ESG funds ESG empty


directory = "Data-Collection/final-fund-holdings/pre-adjusted-funds/cleansed"


restricted_companies = [
    "exxonmobil corporation", "chevron corporation", "conocophillips", 'exxon mobil corp',  'chevron corp',
    "bp plc", "royal dutch shell plc", "total se", "equinor asa",
    "eni s.p.a.", "petroleo brasileiro s.a. (petrobras)",
    "canadian natural resources limited", "occidental petroleum corporation",
    "marathon oil corporation", "devon energy corporation", "apache corporation",
    "anadarko petroleum corporation", "eog resources, inc.", "hess corporation",
    "murphy oil corporation", "halliburton company", "schlumberger limited",
    "philip morris companies inc.", "altria group, inc.", "british american tobacco plc (bat)",
    "imperial brands plc", "japan tobacco inc.", "swedish match ab", "vector group ltd.",
    "22nd century group, inc.", "universal corporation", "pyxus international, inc.",
    "exxonmobil", "chevron", "hess", "philip morris international inc", "philip morris international"
]

def remove_fuzzy_matches(df, column, companies_to_remove, threshold=95):
   
    df[column] = df[column].apply(lambda x: str(x).strip().lower() if isinstance(x, str) else "")
    companies_to_remove = [c.lower() for c in companies_to_remove]

    to_remove = set()

    for company in df[column]:
       
        match = process.extractOne(company, companies_to_remove, scorer=fuzz.token_sort_ratio)
        if match and match[1] >= threshold:
            to_remove.add(company)

            print(f"Matched {company} to {match}")

    return df[~df[column].isin(to_remove)]

def process_csv(file_path):
    df = pd.read_csv(file_path)

    df = remove_fuzzy_matches(df, "Company", restricted_companies)

    total_weight = df["Index Weight"].sum()
    df["Index Weight"] = df["Index Weight"] / total_weight

    new_file_name = os.path.basename(file_path)
    df.to_csv(os.path.join("Data-Collection/final-fund-holdings/", new_file_name), index=False)

for file in os.listdir(directory):
    if file.endswith(".csv"):
        process_csv(os.path.join(directory, file))
