from fastapi import FastAPI, Query
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from model.db_handler import match_exact, match_like


app = FastAPI()


@app.get('/')
def index():
    '''
    Index provides usage instractions in JSON format
    '''
    response = {'usage': '/dict?=<word>'}
    return response


@app.get('/dict')
def dictionary(word: str):
    
    if not word:
        response = {'status': 'error', 'word': word, 'data': 'word not found'}
        return jsonable_encoder(response)

    definitions = match_exact(word)
    if definitions:
        response = {'status': 'success', 'word': word, 'data': definitions}
        return jsonable_encoder(definitions)

    definitions = match_like(word)
    if definitions:
        response = {'status': 'partial', 'word': word, 'data': definitions}
        return jsonable_encoder(definitions)
    
    response = {'status': 'error', 'word': word, 'data': 'word not found'}
    return jsonable_encoder(response)
