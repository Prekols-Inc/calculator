# calculator

## Запуск базы данных (MySQL)

Для работы приложения требуется запущенный сервер MySQL.  
Самый простой способ поднять базу — через Docker.

```bash
docker run --name calculator-mysql \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=calculator_db \
  -e MYSQL_USER=calc_user \
  -e MYSQL_PASSWORD=calc_pass \
  -p 3306:3306 \
  -d mysql:8

После запуска контейнера можно проверить, что база работает:

```bash
docker ps
Ожидаемый результат — запущенный контейнер calculator-mysql.

Чтобы подключиться внутрь контейнера и проверить базу:
docker exec -it calculator-mysql mysql -u calc_user -p
# вводим пароль: calc_pass