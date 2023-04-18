""" Retrieves zipfile from companies house, extracts the csv file and then filters the data to get the number of companies 
created in the last x years in y country of the Uk """


import requests
import zipfile
import io
import pandas as pd
import datetime

class comphouse:
    def __init__(self, url, years, country):
        self.url = url
        self.years = years
        self.country = country
       
    def transform(self):
        response = requests.get(self.url)
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            data_file = zip_file.extract(zip_file.namelist()[0])
        df = pd.read_csv(data_file)
        df = pd.read_csv(response.content)
        today = datetime.date.today()
        x_years_ago = today - datetime.timedelta(days=365 * self.years)
        x_years_ago_ts = pd.Timestamp(x_years_ago)
        companies = df[df['RegAddress.Country'] == self.country]
        companies['IncorporationDate'] = pd.to_datetime(companies['IncorporationDate'])
        new_companies = companies[companies['IncorporationDate'] > x_years_ago_ts]
        total_companies = len(new_companies)
        print(f'Total companies created in {self.country} in the last {self.years} years: {total_companies}')
        output_file = 'new_companies_new.csv'
        new_companies.to_csv(output_file, index=False)
        print(f'Exported company details to {output_file}')


if __name__ == '__main__':
    url = 'https://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2023-04-01.zip'
    years_to_go_back = 8
    country = 'SCOTLAND'
    chouse = comphouse(url, years_to_go_back, country)
    chouse.transform()
