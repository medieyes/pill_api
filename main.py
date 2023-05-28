import mymodel

from tempfile import NamedTemporaryFile
from typing import IO

from typing import Union
from fastapi import FastAPI, UploadFile, File
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



async def save_file(file: IO):
    # s3 업로드라고 생각해 봅시다. delete=True(기본값)이면
    # 현재 함수가 닫히고 파일도 지워집니다.
    with NamedTemporaryFile("wb", delete=False) as tempfile:
        tempfile.write(file.read())
        return tempfile.name

@app.post("/file/")
async def store_file(file: UploadFile = File(...)):
    path = await save_file(file.file)
    res = mymodel.detect(path).rstrip()
    return {"filepath": path,
            "class": res
          }

@app.post("/file/info")
def get_file_info(file: UploadFile = File(...)):
    return {
        "content_type": file.content_type,
        "filename": file.filename
    }