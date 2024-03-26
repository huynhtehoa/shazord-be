import uvicorn
from fastapi import HTTPException, Depends, FastAPI, File, UploadFile

from shazamio import Shazam

app = FastAPI()

def validate_file(file: UploadFile):
  if file.content_type != 'audio/mpeg':
    raise HTTPException(status_code=415, detail='Unsupported media type')


def get_shazamio():
    shazam = Shazam()
    yield shazam


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

      return { 'title': out['track']['title'], 'artist': out['track']['subtitle'] }
    finally:
      file.close()


if __name__ == '__main__':
    uvicorn.run(app)
