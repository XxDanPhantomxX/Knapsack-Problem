import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import os

PATH_CSV = 'Discretas/Codicioso/data.csv'

def load_data():
    try:
        dataset = pd.read_csv(PATH_CSV)
    except FileNotFoundError:
        print("Error: The file 'data.csv' was not found.")
        exit(1)
    except pd.errors.EmptyDataError:
        print("Error: The file 'data.csv' is empty.")
        exit(1)
    except pd.errors.ParserError:
        print("Error: The file 'data.csv' could not be parsed.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
    return dataset

dataset = load_data()   
print(dataset.head())