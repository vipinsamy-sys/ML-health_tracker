# ML Health Tracker 

## OpenAI Chat Integration

This project includes a chatbox backed by OpenAI in two places:

- `templates/index.html` (served by Flask at `http://127.0.0.1:5000/`) — calls the Flask endpoint on the same origin.
- `public/login.html` (served by Node/Express at `http://127.0.0.1:3001/`) — calls the Flask endpoint cross-origin.

### 1) Python dependencies

Install required packages (preferably in a virtualenv):

```bash
pip install flask numpy joblib openai>=1.40.0
```

Optional (for broader CORS support you can also install):

```bash
pip install flask-cors
```

### 2) Environment variable

Set your OpenAI API key before starting Flask:

```powershell
$env:OPENAI_API_KEY = "sk-..."  # Windows PowerShell
```

On macOS/Linux Bash:

```bash
export OPENAI_API_KEY="sk-..."
```

### 3) Start servers

- Flask (serves prediction form + chat under `/api/chat`):

```bash
python app.py
```

- Node/Express (optional, serves the login page with chat):

```bash
npm install
npm run start  # or: node server.js
```

### 4) Chat usage

- In `templates/index.html`, click the chat bubble and send a message.
- In `public/login.html`, the chat will POST to `http://127.0.0.1:5000/api/chat`. The Flask endpoint adds permissive CORS headers for local development.

### 5) Model used

The Flask endpoint uses the OpenAI Chat Completions API (default `gpt-4o-mini`). Adjust the model in `app.py` if desired. 
