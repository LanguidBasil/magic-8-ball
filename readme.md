# Magic 8 Ball

Одностраничное приложение, с шаром предсказаний
- Логин по email
- История вопросов с счетчиком сколько еще пользователей их задали
- Генерация ответа на стороне сервера

![image](https://github.com/LanguidBasil/magic-8-ball/assets/72715882/aca9f457-c382-49d5-812a-6d4b04bc3ef5)

[Изображение в docker hub](https://hub.docker.com/repository/docker/languidbasil/softorium-test-task/general)
с инструкцией по использованию

## Возникшие сложности при решении задания
- Как сделать авторизацию. Так как приложение одностраничное, и пользователи не будут на него заходить часто (больше игрушка на один вечер), я решил пойти легким путем "логин" каждый раз. Если проект будет расти логирование нужно будет улучшить и хранить user_id (способ идентификации) хотя бы в cookies
- Race conditions при увеличении счетчика "сколько раз вопрос задали". По умолчанию SQLAlchemy использует уровень изоляции драйвера базы данных. Прямо сейчас это aiosqlite (для SQLite) у которого уровень serializable (максимальный) и беспокоится вообще не стоит. А в будущем скорее всего asyncpg (для Postgres) у которого это read committed. Здесь больших проблем тоже не возникнет, так как сложных запросов на несколько чтений внутри транзакции не предвидется, также как и частых обновлений.
- Выбор как будут ссылаться пользователи на вопросы. Нам точно нужно знать какие вопросы задал пользователь чтобы выдавать его историю, поэтому у него будет ссылка на вопросы которые он задал. И при этом один и тот же вопрос могут задать множество людей, поэтому отношение будет Many to Many
- Как определить сколько раз вопрос был задан. Ввести два счетчика, сколько раз вопрос спросили всего, и какие пользователи его спрашивали это сложно и немного "а зачем". Поэтому я решил пойти путем попроще и определять "сколько уникальных пользователей задали этот вопрос". Это не только проще в реализации но и более стабильно так как теперь можно просто выполнить Count запрос к ассоциативной таблице вопросов и пользователей

