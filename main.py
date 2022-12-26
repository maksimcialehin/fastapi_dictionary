import uvicorn, io
from fastapi import FastAPI, Query, UploadFile, File
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from model.db_handler import match_exact, match_like
from bin.filters import apply_filter


app = FastAPI()


filters_availbale = [
    'blur',
    'contour',
    'detail',
    'edge_enhance',
    'edge_enhance_more',
    'emboss',
    'find_edges',
    'sharpen',
    'smooth',
    'smooth_more',
]


@app.api_route('/', methods=['GET', 'POST'])
def index():
    '''
    Index provides usage instractions in JSON format
    '''
    response = {
        'filters_available': filters_availbale,
        'usage': {'http_method': 'POST', 'URL': '/<filter_available>'}
        }
    return jsonable_encoder(response)


@app.post('/{filter}')
def image_filter(filter: str, img: UploadFile = File(...)):
    
    if filter not in filters_availbale:
        response = {'error': 'incorrect filter'}
        return jsonable_encoder(response)

    filtered_image = apply_filter(img.file, filter)

    return StreamingResponse(filtered_image, media_type='image/jpeg')


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
