# Claude Chat

A Streamlit web app for Anthropic's Claude API with encrypted storage and TOTP authentication.

## Features

- **Encrypted threads**: Conversations stored as encrypted files using Fernet
- **TOTP login**: 2FA authentication via authenticator apps
- **Files API**: Upload and attach documents to conversations
- **Mobile responsive**: Works on desktop and mobile browsers
- **Thread management**: Save, rename, and organize chat history

## Setup

### 1. Clone and install

```

git clone https://github.com/siudika/claude_chat.git
cd claude-chat
pip install -r requirements.txt

```

### 2. Create `.env` file

```


# Generate encryption key

python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Generate TOTP secret

python -c "import pyotp; print(pyotp.random_base32())"

```

Create `.env` with:

```

ANTHROPIC_API_KEY=sk-ant-your-key
CLAUDE_CHAT_KEY=your-generated-fernet-key
CLAUDE_TOTP_SECRET=your-generated-totp-secret

```

### 3. Add TOTP to authenticator app

- Open Google Authenticator / Microsoft Authenticator / Authy
- Add account manually with the `CLAUDE_TOTP_SECRET` value
- Save as "Claude Chat"

### 4. Run

```

streamlit run claude_gui.py

```

Open http://localhost:8501 and log in with your authenticator code.

## Usage

- **New chat**: Click "New Chat" in sidebar
- **Attach files**: Enable "Files" checkbox, upload PDFs/text files, select them before sending
- **Switch threads**: Click thread names in sidebar
- **Change model**: Use model dropdown in sidebar

## Deploy to Streamlit Cloud

1. Push repo to GitHub (don't commit `.env`)
2. Deploy at https://share.streamlit.io
3. Add secrets in App Settings → Secrets:

```

ANTHROPIC_API_KEY = "sk-ant-..."
CLAUDE_CHAT_KEY = "your-key"
CLAUDE_TOTP_SECRET = "your-secret"

```

## Structure

```

claude-chat/
├── claude_gui.py          \# Main app
├── requirements.txt       \# Dependencies
├── .env                   \# Secrets (not committed)
└── data/                  \# Encrypted threads (auto-created)
├── *.json.enc         \# Encrypted conversations
├── files_index.json   \# File metadata
└── usage_log.json     \# Token usage

```

## Tech Stack

- **Streamlit**: Web framework
- **Anthropic SDK**: Claude API client
- **cryptography**: Fernet encryption
- **pyotp**: TOTP implementation

## Troubleshooting

**"CLAUDE_CHAT_KEY not found"**  
Make sure `.env` exists and contains the key.

**"Invalid code" on login**  
Check your device time is synced. Codes expire every 30 seconds.

**"Failed to decrypt thread"**  
Encryption key changed. Old threads can't be read without the original key.

## License

MIT
```