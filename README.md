```bash
  # install venv
  python3 -m venv .venv

  # install ffmpeg
  sudo apt install ffmpeg

  # activate venv
  source .venv/bin/activate

  # install dependencies
  pip install -r requirements.txt

  # start server
  uvicorn main:app --reload

  # deactivate venv
  deactivate
```
