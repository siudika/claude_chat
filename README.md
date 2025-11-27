# 🔐 Claude Chat - Secure Streamlit GUI

A sophisticated, locally-hosted Streamlit application for Claude API with **end-to-end encryption**, **TOTP-based authentication**, and **mobile-responsive design**. Encrypt your conversation threads at rest, gate access with your authenticator app, and chat with Claude on any device.

---

## ✨ Features

### 🔒 Security First
- **End-to-End Encryption**: All conversation threads are encrypted with Fernet (AES) before being written to disk
- **TOTP Authentication**: 2FA-style login using Time-based One-Time Passwords (compatible with Google Authenticator, Microsoft Authenticator, Authy, etc.)
- **No Plaintext Secrets**: API keys and encryption keys live only in environment variables, never in the repo or `data/` directory
- **Encrypted Storage**: `data/` directory contains only encrypted `.json.enc` files; plaintext conversations are automatically migrated and deleted on first load

### 💬 Chat & Thread Management
- **Persistent Threads**: Save and organize multiple conversation threads, encrypted at rest
- **Thread Editing**: Rename, delete, and quickly switch between past conversations
- **Model Selection**: Choose between Claude 3.5 Sonnet, Claude 3 Opus, and other available models
- **Usage Tracking**: Monitor token usage and estimated costs over the last 24 hours

### 📁 Files API Integration
- **Document Upload**: Upload PDF and text files to Anthropic's Files API
- **Smart Indexing**: Local index tracks uploaded files; refresh from Anthropic anytime
- **Context-Aware Analysis**: Attach files to prompts with actions: Analyze, Edit, or Summarize
- **Automatic Refresh**: One-click sync with Anthropic's Files API to recover files from other clients

### 📱 Mobile-First Responsive Design
- **Touch-Optimized UI**: 44px+ touch targets, auto-collapsible sidebar, full-width chat on small screens
- **Adaptive Layout**: Streamlit centered layout adjusts from 320px phones to 4K desktop displays
- **Sticky Bottom Input**: Chat input always accessible on mobile, never covered by keyboard
- **Collapsible Sections**: Usage stats, Files API, and chat history hidden on mobile by default

### 🔄 Backward Compatibility
- **Legacy Support**: Automatically migrates plaintext `.json` threads to encrypted format on first load
- **Transparent Encryption**: No user action required; migration happens silently and securely

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+**
- **pip** (Python package manager)
- **Authenticator App** (Google Authenticator, Microsoft Authenticator, Authy, etc.)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/claude-chat.git
cd claude-chat
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt includes:**
```
streamlit
anthropic
python-dotenv
cryptography
requests
pyotp
streamlit-nested-layout
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root with the following:

```bash
# Anthropic API Key (get from https://console.anthropic.com)
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE

# Fernet Encryption Key (for encrypting conversation threads)
# Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
CLAUDE_CHAT_KEY=YOUR_FERNET_KEY_HERE

# TOTP Secret (for authenticator app 2FA)
# Generate with: python -c "import pyotp; print(pyotp.random_base32())"
CLAUDE_TOTP_SECRET=YOUR_TOTP_SECRET_HERE
```

### 4. Generate Encryption Key

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the output and paste it as `CLAUDE_CHAT_KEY` in your `.env` file.

### 5. Generate TOTP Secret & Register with Authenticator

```bash
python -c "import pyotp; print(pyotp.random_base32())"
```

- Copy the output and paste it as `CLAUDE_TOTP_SECRET` in your `.env` file
- Open your authenticator app (Google Authenticator, Microsoft Authenticator, Authy, etc.)
- Add a new account:
  - Select **Manual entry** (or scan QR code if you generate one)
  - **Issuer**: `Claude Chat`
  - **Account**: `your-email@example.com` (or any identifier)
  - **Secret**: Paste the TOTP secret from above
- Save and verify a 6-digit code appears and rotates every ~30 seconds

### 6. Run the App

```bash
streamlit run claude_gui.py
```

The app will start at `http://localhost:8501`. You'll see a login screen asking for your 6-digit authenticator code. Enter it to proceed.

---

## 🔐 Authentication & Security

### TOTP Login Flow

1. **App starts** → Login screen appears
2. **Open authenticator app** → Copy the 6-digit code
3. **Paste code** → App verifies and unlocks
4. **Access granted** → Full chat interface available

Codes rotate every ~30 seconds and are cryptographically verified on the server. Invalid or expired codes are rejected.

### Encryption Details

- **Thread Storage**: All conversation JSON files are encrypted with Fernet (symmetric AES-128) before being written to `data/`
- **Key Management**: Encryption key lives only in `CLAUDE_CHAT_KEY` environment variable; never hardcoded or committed to git
- **Migration**: Existing plaintext `.json` threads are automatically re-encrypted and deleted on first load
- **At-Rest Security**: Even with access to `data/` directory, without the correct `CLAUDE_CHAT_KEY`, threads cannot be decrypted

---

## 📖 Usage Guide

### Starting a New Chat

1. Click **➕ New Chat** in the sidebar
2. Type your message and hit Enter or click the chat input
3. The thread auto-generates a name from your first message + timestamp
4. Chat history is encrypted and saved automatically

### Renaming a Thread

1. Click **✎ Edit** next to a thread name in the sidebar
2. Enter the new name and click **✓ Confirm** or **✕ Cancel**

### Attaching Files

1. Open **📁 Files API** expander in the sidebar
2. Click **Upload** and select PDF or text files
3. Wait for upload confirmation (files go to Anthropic's Files API)
4. In the chat area, check **📎 Files**, select files, and choose an action:
   - **🔍 Analyze**: Get insights from the files
   - **✏️ Edit**: Propose code/text changes
   - **📝 Summarize**: High-level overview of contents
5. Type your question and send

### Selecting a Model

1. In the sidebar, use the **Model** dropdown
2. Choose between Claude 3.5 Sonnet (faster, cheaper) or Claude 3 Opus (smarter, more capable)
3. The model selection applies to all future messages in that chat

### Checking Usage & Costs

1. Open **📊 Usage (24h)** expander in the sidebar
2. See total tokens and estimated costs for the last 24 hours
3. Recent requests are logged at the bottom

---

## 🌐 Deploying to Streamlit Cloud

### Step 1: Push to GitHub

Ensure your repo is public or private on GitHub. **Do not commit `.env`** — add it to `.gitignore`.

### Step 2: Create Streamlit Account

1. Go to https://share.streamlit.io
2. Click "New app" and authorize with GitHub

### Step 3: Deploy

1. Select your repo, branch, and `claude_gui.py` as the main file
2. Click **Deploy**

### Step 4: Add Secrets

1. After deployment, go to **App settings → Secrets**
2. Paste your secrets in TOML format:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
CLAUDE_CHAT_KEY = "your-fernet-key"
CLAUDE_TOTP_SECRET = "your-totp-secret"
```

3. Save and the app will restart with secrets injected

### Step 5: Restrict Access

1. Go to **App settings → Permissions**
2. Set visibility to **Private**
3. Optionally add specific GitHub users/emails

Your app is now live and private! Access it from any device by logging in with your authenticator app.

---

## 🏠 Running Locally for Development

### Start the Dev Server

```bash
streamlit run claude_gui.py
```

The app hot-reloads on file changes.

### Local Testing with Secrets

Create `.streamlit/secrets.toml` (not committed):

```toml
ANTHROPIC_API_KEY = "sk-ant-YOUR_LOCAL_KEY"
CLAUDE_CHAT_KEY = "YOUR_LOCAL_FERNET_KEY"
CLAUDE_TOTP_SECRET = "YOUR_LOCAL_TOTP_SECRET"
```

Streamlit will use these if environment variables are not set.

---

## 📋 Project Structure

```
claude-chat/
├── claude_gui.py           # Main Streamlit app (all-in-one)
├── requirements.txt         # Python dependencies
├── .env                     # SECRETS (DO NOT COMMIT)
├── .gitignore              # Excludes .env, data/, __pycache__
├── README.md               # This file
└── data/                   # Encrypted thread files & indexes (auto-created)
    ├── *.json.enc          # Encrypted conversation threads
    ├── project_index.json  # Project file summaries (unencrypted)
    ├── files_index.json    # Uploaded file metadata
    └── usage_log.json      # Token usage history
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Example |
|---|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key | `sk-ant-...` |
| `CLAUDE_CHAT_KEY` | Fernet encryption key for threads | Output of `Fernet.generate_key().decode()` |
| `CLAUDE_TOTP_SECRET` | Base32 TOTP secret for 2FA | Output of `pyotp.random_base32()` |

### Streamlit Config (Optional)

Create `.streamlit/config.toml` for customization:

```toml
[client]
showErrorDetails = false
toolbarMode = "minimal"

[theme]
primaryColor = "#2180b0"
backgroundColor = "#f5f5f5"
secondaryBackgroundColor = "#ffffff"
textColor = "#333333"
font = "sans serif"
```

---

## 🐛 Troubleshooting

### "CLAUDE_CHAT_KEY not found"
Ensure your `.env` file exists in the project root and contains:
```
CLAUDE_CHAT_KEY=your-fernet-key-here
```

### "CLAUDE_TOTP_SECRET not set"
Generate a TOTP secret and add it to `.env`:
```bash
python -c "import pyotp; print(pyotp.random_base32())"
```

### "Invalid or expired code" on login
- Ensure your authenticator app is synced (check device time)
- The code rotates every ~30 seconds; re-generate if too old
- Regenerate the TOTP secret and re-add to your authenticator app if issues persist

### "Failed to decrypt thread"
- Encryption key mismatch: Check that `CLAUDE_CHAT_KEY` is correct
- If you changed the key, old threads cannot be decrypted (data loss); keep backups of `.json.enc` files
- Plaintext `.json` threads are automatically migrated; if errors occur, check file permissions

### "Files API integration not working"
- Ensure `ANTHROPIC_API_KEY` is valid
- Only PDF and text files are supported; other formats are converted to plain text
- File upload timeouts may occur on slow connections; retry or upload smaller files

### Sidebar not showing on mobile
- This is normal; swipe from the left edge or tap the hamburger menu icon in the top-left
- Sidebar auto-expands on larger screens

---

## 🤝 Contributing

Found a bug? Have a feature idea?

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-idea`
3. Make changes and test locally
4. Commit: `git commit -m "Add your feature"`
5. Push: `git push origin feature/your-idea`
6. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**. See `LICENSE` file for details.

---

## 🙏 Acknowledgments

- **Anthropic** for the Claude API and Files API
- **Streamlit** for the web framework
- **pyotp** for TOTP implementation
- **cryptography** for Fernet encryption

---

## 📞 Support

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Docs**: See in-app tooltips and this README for help
- **Security**: If you find a security issue, please responsibly disclose it by emailing the maintainer

---

## 🚀 What's Next?

Future improvements planned:
- [ ] S3/cloud storage backend for thread migration
- [ ] Multi-user support with role-based access
- [ ] Conversation search and tagging
- [ ] Custom system prompts per thread
- [ ] Voice input/output support
- [ ] Dark mode theme toggle
- [ ] Export conversations as PDF/Markdown

---

## 📊 Privacy & Data

- **Local Storage**: All conversations are stored locally in `data/` (encrypted)
- **Files**: Uploaded files are sent to Anthropic's Files API; refer to their [privacy policy](https://www.anthropic.com/privacy)
- **No Telemetry**: This app does not send any data to third parties except Anthropic for API calls
- **Your Data**: You own and control your conversations; encryption keys are only in your environment

---

**Built with ❤️ for secure, private Claude conversations**

---

### Quick Commands Reference

```bash
# Generate Fernet key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Generate TOTP secret
python -c "import pyotp; print(pyotp.random_base32())"

# Start app
streamlit run claude_gui.py

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=your_key_here
CLAUDE_CHAT_KEY=your_fernet_key
CLAUDE_TOTP_SECRET=your_totp_secret
EOF
```

---

**Version**: 1.0.0 | **Last Updated**: November 2025
