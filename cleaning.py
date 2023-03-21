import pandas as pd 
import numpy as np
import os

## LOADING DATA ##
def clean_restaurant(data):
    '''
    Given a json dictionary of information, access & pull most relevant data.
    Helps to reshape the full dataframe. 
    '''
    
    keys_of_interest = ['name', 'rating', 'price', 'categories', 'coordinates']
    
    cleaned_data = {}
    
    for i in range(len(keys_of_interest)):
        
        key = keys_of_interest[i]
        
        if key in data.keys():
            
            if key == 'categories':
                
                cleaned_data['categories'] = ', '.join([cat['alias'] for cat in data['categories']])
            
            elif key == 'coordinates':
                
                cleaned_data['latitude'] = data['coordinates']['latitude']
                cleaned_data['longitude'] = data['coordinates']['longitude']
                
            elif key == 'price':
                
                cleaned_data['price'] = data['price'].count('$')
                
            else:
                
                cleaned_data[key] = data[key]
        else:
            
            cleaned_data[key] = np.NaN
    
    return cleaned_data

def load_data(full_path):
    
    files = os.listdir(full_path)

    df = pd.DataFrame()
    for file in files:

        league = full_path + file + '/'
        teams = os.listdir(league)

        for team in teams:

            curr = full_path + file + '/' + team
            big_df = pd.read_json(curr)

            curr_df = pd.DataFrame()
            restaurants = big_df['businesses'].apply(clean_restaurant)

            for rest in restaurants:

                rest['league'] = file
                rest['team'] = big_df['team'].iloc[0]
                rest['stadium'] = big_df['stadium'].iloc[0]
                rest['team_latitude'] = big_df['stadium latitude'].iloc[0]
                rest['team_longitude'] = big_df['stadium longitude'].iloc[0]
                rest['state'] = big_df['state'].iloc[0]
                rest['city'] = big_df['city'].iloc[0]

                curr_df = pd.concat([curr_df, pd.DataFrame(rest, index = [0])], ignore_index=True)

            df = pd.concat([df, curr_df], ignore_index = True)

    df.reset_index(drop = True, inplace = True)
    
    return df
    
    
## PROCESSING DATA ## 

def clean_cats(cat):
    
    if not pd.isnull(cat):
        
        cat += ', '
        
    return cat

def clean_city(city):
    '''
    Replaces a city marked as a NYC burrough as New York City. 
    '''
    
    nyc_burrough = ['Brooklyn', 'Queens', 'Manhattan', 'Bronx', 'Long Island']
    if city in nyc_burrough:
        city = 'New York City'
        
    return city

def find_max(category, category_count):
    
    '''
    Finds the key with the max value for a list of keys
    '''
    
    # find max
    max_count = 0
    best_category = 'null'
    for entry in category:
        entry = entry.replace(' ', '')
        if category_count[entry] > max_count:
            max_count = category_count[entry]
            best_category = entry
            
    return best_category

def combine_categories(category): 

    asian_categories = [
        'himalayan',
        'japanese',
        'korean',
        'sushi',
        'thai',
        'vietnamese'
    ]
    
    italian_categories = ['italian', 'pastashops']
    latin_categories = ['latin', 'mexican', 'puertorican', 'spanish', 'tacos']
    
    novelty_categories = [
        'juicebars', 'meats', 'shavedice', 'vegan'
    ]
    
    american_categories = ['hotdog', 'sandwiches', 'seafood', 'tradamerican']
    
    central_europe_asia = ['greek', 'mediterranean', 'mideastern', 'turkish', 'ukrainian']
    
    grocery = ['grocery', 'intlgrocery']
    
    if category in asian_categories:
        category = 'asian'
    elif category in italian_categories:
        category = 'italian'
    elif category in latin_categories:
        category = 'latin'
    elif category in novelty_categories:
        category = 'novelty'
    elif category in american_categories:
        category = 'american'
    elif category in central_europe_asia:
        category = 'central_europe_asia'
    elif category in grocery:
        category = 'grocery'
    else:
        category = 'other'
        
    return category

def clean_cats(cat):
    
    if not pd.isnull(cat):
        
        cat += ', '
        
    return cat