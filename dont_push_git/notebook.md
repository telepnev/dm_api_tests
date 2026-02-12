
pip install requests
pip install pytest
pip install faker
pip install structlog  # для красивых и читабельных логов
pip install curlify    # для создания curl, удобно бросить в разраба курл

pip install retrying # старая библиотека, уже не поддерживается 
pip install tenacity # современная альтернатива !!!!




pip freeze > requerments.txt



Прочитать  про : 
from requests import session
Что за зверь - session


### =================================================
1️⃣ Кратко и простыми словами

Эта архитектура нужна, чтобы:
- тесты были читаемыми
- бизнес-логика не лежала в тестах
- HTTP / auth / логи не дублировались
- один тест мог дергать несколько API за один шаг

👉 Ключевая идея:
тест → helper → facade → api → client → HTTP

2️⃣ Схема архитектуры в текстовом виде

┌───────────────┐
│     TEST      │  ← pytest test
└───────┬───────┘
        │
        ▼
┌────────────────────┐
│  App Layer         │
│  AccountHelper     │
│  (бизнес-действия) │
└───────┬────────────┘
        │
        ▼
┌────────────────────┐
│  Facade Layer      │
│  AccountFacade     │
│  (объединяет API)  │
└───────┬────────────┘
        │
        ▼
┌────────────────────┐
│  API Layer         │
│  AccountApi        │
│  LoginApi          │
│  V2Api             │
└───────┬────────────┘
        │
        ▼
┌────────────────────┐
│  Proxy Layer       │
│  RestClient        │
│  (auth, logs)      │
└───────┬────────────┘
        │
        ▼
┌────────────────────┐
│  Session Layer     │
│  requests.Session │
│  HTTP (GET/POST)  │
└───────┬────────────┘
        │
        ▼
┌────────────────────┐
│  SERVER (NGINX)    │
│  JSON response     │
└────────────────────┘

