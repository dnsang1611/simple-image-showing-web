from fastapi import FastAPI, Request, Form, Depends, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from glob import glob
import json 

LABEL_PATH = './static/data/labels'

app = FastAPI()

templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

img_paths = sorted(os.listdir('static/data/images'))
print(f'Total images: {len(img_paths)}')

n_imgs = len(img_paths)
batch_size = 16
n_batch = n_imgs // batch_size + (n_imgs % batch_size != 0)

@app.get('/index', response_class=HTMLResponse)
def index(request: Request):
    context = {
        'request': request,
        'img_paths': img_paths[0: batch_size],
        'batch_id': 0,
        'last_id': n_batch - 1
    }

    print(f'N.o images: {len(img_paths[0: batch_size])}')

    return templates.TemplateResponse('index.html', context)

@app.get('/index/{batch_id}', response_class=HTMLResponse)
def get_batch(*, request: Request, batch_id: int):
    context = {
        'request': request,
        'img_paths': img_paths[batch_id * batch_size : (batch_id + 1) * batch_size],
        'batch_id': batch_id,
        'last_id': n_batch - 1
    }

    print(f'N.o images: {len(img_paths[batch_id * batch_size : (batch_id + 1) * batch_size])}')
    return templates.TemplateResponse('index.html', context)

@app.get('/images/{img_path}', response_class=HTMLResponse)
def get_image_info(*, request: Request, img_path: str, batch_id: int):
    label_path = f"{LABEL_PATH}/{img_path.split('.')[0]}.json"
    with open(label_path) as rf:
        info = json.load(rf)

    print(info)
    context = {
        'request': request,
        'img_path': img_path,
        'info': info,
        'prev_id': batch_id
    }
    print(batch_id)
    return templates.TemplateResponse('single_img.html', context)
