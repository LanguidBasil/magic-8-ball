import os


APP_LOGS_PATH = os.environ.get("APP_LOGS_PATH", default="./app_logs")
DATABASE_URL = os.environ.get("DATABASE_URL", default="sqlite+aiosqlite:///magic_8_ball.db") 

ANSWER_OPTIONS = os.environ.get(
    "ANSWER_OPTIONS", 
    default="Да~Нет~Возможно~Вопрос не ясен~Абсолютно точно~Никогда~Даже не думай~Сконцентрируйся и спроси опять",
).split("~")
