import pandas as pd
import os
import glob
from flask import Flask, jsonify, render_template, request
from fuzzywuzzy import process

# Initialize the Flask app
app = Flask(__name__)

# Utility Functions

def read_main_csv(file_path):
    """Reads the main CSV file into a dataframe."""
    return pd.read_csv(file_path)

def read_fund_files(directory_path):
    """Traverses the directory and reads each fund's spreadsheet into a dictionary of dataframes."""
    fund_files = glob.glob(os.path.join(directory_path, "*.csv"))
    fund_data = {}
    for fund_file in fund_files:
        fund_name = os.path.basename(fund_file).replace('.csv', '')
        fund_data[fund_name] = pd.read_csv(fund_file)
    return fund_data

def match_assets_to_funds(main_csv, fund_data):
    """Matches assets to funds using fuzzy matching."""
    def get_fund_data_for_asset(asset_name):
        matches = process.extract(asset_name, fund_data.keys(), limit=1)
        if matches and matches[0][1] > 80:
            return fund_data[matches[0][0]]
        return None

    matched_data = []
    for _, row in main_csv.iterrows():
        asset_name = row['Name']
        fund_info = get_fund_data_for_asset(asset_name)
        if fund_info is not None:
            row['Fund Composition'] = fund_info.to_dict(orient='records')
        matched_data.append(row)

    return pd.DataFrame(matched_data)

def aggregate_company_investments(main_csv, fund_data):
    """Aggregates investments by company."""
    company_investments = {}

    for fund_name, df in fund_data.items():
        fund_investment = main_csv[main_csv['Name'] == fund_name]['Total_investment'].values[0]

        for _, row in df.iterrows():
            company_name = row['Company']
            weight = float(row['Index Weight'])
            investment_amount = fund_investment * weight

            if company_name in company_investments:
                company_investments[company_name] += investment_amount
            else:
                company_investments[company_name] = investment_amount

    return company_investments

# API Endpoints

@app.route('/data/investments', methods=['GET'])
def get_investments():
    """Returns a JSON response with aggregated investment data."""
    main_csv_path = 'Data-Collection/Helper-Functions/combined-output/combined_investments.csv'
    funds_directory = 'Data-Collection/final-fund-holdings'

    main_csv = read_main_csv(main_csv_path)
    fund_data = read_fund_files(funds_directory)

    matched_data = match_assets_to_funds(main_csv, fund_data)
    company_investments = aggregate_company_investments(main_csv, fund_data)

    response_data = {
        'assets': matched_data.to_dict(orient='records'),
        'companies': company_investments
    }
    return jsonify(response_data)

@app.route('/visualization/asset_pie_chart', methods=['GET'])
def visualize_asset_pie_chart():
    """Generates and displays an asset pie chart."""
    # To be implemented
    pass

@app.route('/visualization/company_pie_chart', methods=['GET'])
def visualize_company_pie_chart():
    """Generates and displays a company pie chart."""
    # To be implemented
    pass

# Main Execution
if __name__ == "__main__":
    app.run(debug=True)

