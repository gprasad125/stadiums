import pandas as pd 
import numpy as np

def clean_cats(cat):
    
    if not pd.isnull(cat):
        
        cat += ', '
        
    return cat

def clean_state(state):
    
    state = state.lower()
    new_york = ['new york', 'new york city', 'manhattan', 'brooklyn', 'queens', 'bronx', 'long island']
    
    if state in new_york:
        state = 'new york'
    elif state == 'bc':
        state = 'british columbia'
    
    return state