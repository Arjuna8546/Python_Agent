# 🛠 Project Setup Guide

This guide explains how to set up, run, and deploy your Django backend (with WebSocket support via Daphne and Redis) and how to compile your Python agent into a standalone executable.

---

## 🚀 Prerequisites

### Backend

* Python 3.9+
* pip
* Redis (local or hosted like Upstash)
* Virtualenv (recommended)

### Agent (Client)

* Python 3.9+
* PyInstaller

---

## ⚙️ Backend Setup (Django)

### 1. Clone and Navigate

```bash
https://github.com/Arjuna8546/Python_Agent.git
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. (Optional) Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Server (Daphne)

```bash
daphne backend.asgi:application
```

---

## 🧠 WebSocket Configuration

### `settings.py`
provide appropriate REDIS_URL IN env file.
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.getenv("REDIS_URL", "redis://localhost:6379")],
        },
    },
}
```


---

## 🧪 Running the Agent (Python Script)

### Example WebSocket Client (agent.py)

## 📦 Compile Agent to EXE

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build EXE

```bash
pyinstaller --onefile agent.py
```

#### Output:

Executable will be in the `dist/` folder. (agent.exe)

Optional flags:

* `--noconsole` : Hide terminal window
* `--icon=your_icon.ico` : Add icon
* `--add-data="file_or_folder;."` : Bundle extra files

---


## 📁 Environment Variables (.env)

```
REDIS_URL=redis://localhost:6379
DEBUG=True
SECRET_KEY=your-secret

```

---

Feel free to customize this README for your project’s exact structure.
