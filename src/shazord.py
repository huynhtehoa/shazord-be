from fastapi import HTTPException, UploadFile
from shazamio import Shazam

def validate_file(file: UploadFile):
  if file.content_type != 'audio/mpeg':
    raise HTTPException(status_code=415, detail='Unsupported media type')


def get_shazamio():
    shazam = Shazam()
    yield shazam
