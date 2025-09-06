# calculator

## Build

### Backend

```bash
cd backend
python3 -m venv .venv # create virtual environment
source .venv/bin/activate # activate venv
pip install # install all dependencies from requirements.txt

python3 app.py # start server
```

### Frontend

Dev build

```bash
cd frontend
npm install
npm run dev
```

Release build

```bash
cd frontend
npm install
npm run build
npm run preview
```

