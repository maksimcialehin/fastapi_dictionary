from fastapi import FastAPI, Query
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from model.db_handler import match_exact, match_like
import uvicorn


app = FastAPI()


@app.get('/')
def index():
    '''
    Index provides usage instractions in JSON format
    '''
    response = {'usage': '/dict?=<word>'}
    return response


@app.get('/dict')
def dictionary(words: List[str] = Query(None)):
    print(words)
    
    if not words:
        response = {'status': 'error', 'word': words, 'data': 'word not found'}
        return jsonable_encoder(response)

    response = {'words': []}

    for word in words:
        print(word)
        definitions = match_exact(word)
        if definitions:
            response['words'].append({'status': 'success', 'word': word, 'data': definitions})
        else:
            definitions = match_like(word)
            if definitions:
                response['words'].append({'status': 'partial', 'word': word, 'data': definitions})
            else:
                response['words'].append({'status': 'error', 'word': word, 'data': 'word not found'})
    
    return jsonable_encoder(response)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
