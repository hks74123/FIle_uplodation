import hashlib
import os
import ast
import requests

# File to be sent through api
api_file = 'Book - Sheet1.csv'

# getting size of the file
file_size = os.path.getsize(api_file)

hash_md5 = hashlib.md5()

# defining chunk size to be sent
chunk_size = 50

start = 0
existing_path='null'

with open(api_file, 'rb') as f:
    url = 'http://127.0.0.1:8000/chunkuplodation/'
    
    # Iterating in file in chunk portion
    for chunk in iter(lambda: f.read(chunk_size), b''):
        hash_md5.update(chunk)
        uploaded_chunk = start + chunk_size
        next_chunk = start + chunk_size
        if (uploaded_chunk >= file_size):
            file_end = 1
        else:
            file_end = 0
        # Sending a Continous PUT request unit end of file. 
        res = requests.put(
            url,
            data={'filename': 'my_new_file','existingPath':existing_path,'end':file_end,'nextSlice':next_chunk},
            files={'file': chunk},
        )
        if(next_chunk<file_size):
            dictionary = ast.literal_eval(res.text)
            existing_path = dictionary['existingPath']
            start = next_chunk
            
