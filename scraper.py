import re
import requests

import pandas as pd
from bs4 import BeautifulSoup

# Loops all of the pages for a given body type
# and collects information on each car listing
def loop_site_pages(baseURL, bodytypes, obv_limit=1000):

    for body in bodytypes:

        # Get number of total observations for each body type
        num_obv_body = bodytypes[body]

        # Specify URL for a certain body type and page limit
        url = baseURL.replace('cars', body).replace('OBV_LIMIT', str(obv_limit))

        # Loop all pages and look at k cars per page
        # k is specified by obv_limit
        for page in range(num_obv_body // obv_limit):

            # Current page URL
            current_page_url = url + str(page + 1)

            # Get current page content, try again if connection error
            try:
                current_page_content = requests.get(current_page_url)
            except requests.exceptions.ConnectionError:
                current_page_content = requests.get(current_page_url)

            # Parse page into csv and save results
            parse_page_content(current_page_content, body)

# Parses downloaded page content
def parse_page_content(page, btype):
    colNames = ['Num_Pics', 'Model Name', '']

    soup = BeautifulSoup(page.content, 'html.parser')
    cars = soup.findAll('tr', {'class': 'car-row'})

    # Loop through all car entries
    for car in cars:

        # Get all car attributes
        attr = [i.text for i in car.findAll('td')]

        num_pics = int(re.findall('\\d+', attr[0].split('-')[0])[0])

        discount = int(re.findall('\\d+', attr[0].split('-')[-1].replace('%', ''))[-1]) / 100

        model = attr[1].split('CFJ')[0]

        body_type = btype

        date = attr[2]

        km = ''.join(re.findall('\\d+', attr[3]))

        engine_cc = ''.join(re.findall('\\d+', attr[4]))

        grade = attr[5].split(' ')[-1]

        # Get additional attributes from car sub-page
        # If no additional attributes create empty list
        try:
            sub_page_res = parse_sub_page_content(car)
        except IndexError:
            sub_page_res = [[''] * 9
                            ['price', 'trans', 'fuel_type', 'seats', 'num_doors',
                             'steering', 'drive_type', 'dim', 'ext_color']]



        # Create single row dataframe of current car
        car_df = pd.DataFrame([[num_pics, discount, model, body_type, date,
                                km, engine_cc, grade] + sub_page_res[0]],
                     columns=['num_pics', 'discount', 'model', 'body_type',
                              'date', 'km', 'engine_cc', 'grade'] + sub_page_res[1])

        # Append dataframe to existing data
        write_df_to_csv(car_df, 'JDM_car_data_scraped.csv')

# Parses page content for each sub page of car listings
def parse_sub_page_content(car_page):

    # Get subpage url
    sub_url = car_page.find('a', {'target': '_blank'})['href']

    # Get subpage content
    # Try again if there is connection error
    try:
        sub_page = requests.get('https://carfromjapan.com' + sub_url)
    except requests.exceptions.ConnectionError:
        sub_page = requests.get('https://carfromjapan.com' + sub_url)

    sub_soup = BeautifulSoup(sub_page.content, 'html.parser')

    # Get subpage car attributes
    sub_attr = [i.text for i in sub_soup.findAll('div', {'class': 'item info-value flex1'})]

    try:
        price = ''.join(re.findall('\\d+' ,sub_soup.find('span', {'class': 'big-price blue-color'}).text))
    except AttributeError:
        price = '-'

    trans = sub_attr[5]

    fuel_type = sub_attr[8]

    seats = sub_attr[9]

    num_doors = sub_attr[10]

    steering = sub_attr[11]

    drive_type = sub_attr[12]

    dim = sub_attr[13].replace(' m3', '')

    ext_color = sub_attr[15]

    # List of attributes
    return [[price, trans, fuel_type, seats, num_doors, steering, drive_type, dim, ext_color],
            ['price', 'trans', 'fuel_type', 'seats', 'num_doors', 'steering', 'drive_type', 'dim', 'ext_color']]

# Writes dataframe to file path
# Checks if the file already exists
def write_df_to_csv(df, out_path):

    # If output file exists, append results to output file
    try:
        pd.read_csv(out_path)

        # append results to file
        df.to_csv(out_path, mode='a', header=False)

    except FileNotFoundError:
        df.to_csv(out_path)

    return 0



# Dictionary of different car types and relative amount of observations from JDM vendor website
body_types =  {'sedan': 13000, 'minivan': 13000, 'SUV': 16000, 'hatchback': 26000, 'convertible': 1000,
                  'coupe': 4000, 'mini_vehicle': 15000, 'truck': 10000}

# Scrape Car From Japan data
loop_site_pages('https://carfromjapan.com/cheap-used-cars-for-sale?limit=OBV_LIMIT&page=', body_types)

