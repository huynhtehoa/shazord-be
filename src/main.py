import uvicorn
from fastapi import HTTPException, Depends, FastAPI, File, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from models import Token
from auth import fake_users_db, create_access_token, authenticate_user, timedelta, ACCESS_TOKEN_EXPIRE_MINUTES
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

@app.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')


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
