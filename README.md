# calculator

## Build (Linux)

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

## Database launch (MySQL)

To start MySQL in a Docker container run:
```bash
docker run --rm --name calculator-mysql \
  -e MYSQL_ROOT_PASSWORD=passwd \
  -e MYSQL_DATABASE=calculator_db \
  -e MYSQL_USER=calc_user \
  -e MYSQL_PASSWORD=calc_pass \
  -p 3306:3306 \
  -d mysql:8
```

Check for Docker container `calculator-mysql`: 
```bash
docker ps
```
Expected output:
```bash
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                                                    NAMES
aaa9d16acc03   mysql:8   "docker-entrypoint.s…"   5 seconds ago   Up 4 seconds   0.0.0.0:3306->3306/tcp, [::]:3306->3306/tcp, 33060/tcp   calculator-mysql
```

To get into database:
```bash
docker exec -it calculator-mysql mysql -u <username> -p <password>
```
## Tests


```bash
pytest -v # full output of the test results list
pytest -q # brief summary of test results
```
