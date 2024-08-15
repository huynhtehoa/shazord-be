import uvicorn
from fastapi import HTTPException, Depends, FastAPI, File, UploadFile, status
from shazord import get_shazamio, validate_file, Shazam

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["post"],
)

@app.get('/')
def get():
  return 'hello'

@app.post('/recognize')
async def recognize_file(
    shazam_service: Shazam = Depends(get_shazamio), file: UploadFile = File(...)
):
    try:
      validate_file(file)

      out = await shazam_service.recognize_song(await file.read())
      print(out)
      if (len(out['matches']) == 0):
        raise HTTPException(status_code=404, detail='Track not found')

      return out['track']
    finally:
      file.close()


if __name__ == '__main__':
    uvicorn.run(app)
