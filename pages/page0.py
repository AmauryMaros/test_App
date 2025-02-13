import dropbox
import pandas as pd
import streamlit as st

# Replace with your actual access token
access_token = st.secrets["dropbox"]["access_token"]

# Initialize Dropbox client
dbx = dropbox.Dropbox(access_token)

st.write(acces_token)

# Path to the folder (adjust to your folder path)
folder_path = '/path/to/folder'

# List files in the folder
try:
    result = dbx.files_list_folder(folder_path)
    
    # Iterate through files
    for entry in result.entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            # Check for the file you need
            if entry.name == "my_species.csv":
                # Download the file
                metadata, res = dbx.files_download(path=entry.path_lower)
                
                # Load the CSV into a DataFrame
                df = pd.read_csv(res.content)
                print("File loaded successfully")
                print(df.head())
                break
    else:
        print("File 'my_species.csv' not found in the folder.")
except dropbox.exceptions.ApiError as e:
    print(f"Error: {e}")
