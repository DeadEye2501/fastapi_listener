## Fast Api Listener

Этот проект является тествым заданием. Он предоставляет апи, на которое через `swagger` можно передать некоторую строку,
которая будет преобразована в `JSON` и передана в очередь в сервис `kafka`, далее другой микровервис вытащит эти
данные из брокера сообщений и запишет их в базу данных.

### Используемый стек:

- `Docker-compose`
- `Fastapi`
- `Postgresql`
- `Kafka`

Для запуска приложения требоется развернуть контейнеры, используя следующую команду: `docker-compose up --build`,
после чего перейти по адресу `http://localhost/docs` и внести нужные данные в окно формы.