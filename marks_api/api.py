import hashlib
import os
import ast
import requests

file = 'Book - Sheet1.csv'

size = os.path.getsize(file)

hash_md5 = hashlib.md5()

CHUNK_SIZE = 50

start = 0
existingPath='null'

with open(file, 'rb') as f:
    url = 'http://127.0.0.1:8000/chunkuplodation/'
    offset = 0
    for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
        hash_md5.update(chunk)
        uploadedChunk = start + CHUNK_SIZE
        nextChunk = start + CHUNK_SIZE
        if (uploadedChunk >= size):
            end = 1
        else:
            end = 0
        res = requests.put(
            url,
            data={'filename': 'my_new_file','existingPath':existingPath,'end':end,'nextSlice':nextChunk},
            files={'file': chunk},
        )
        if(nextChunk<size):
            dictionary = ast.literal_eval(res.text)
            existingPath = dictionary['existingPath']
            start = nextChunk
