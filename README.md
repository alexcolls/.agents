# 🤖 .agents

> Automate social media by monitoring WhatsApp groups and reposting videos

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

> **Automate your social media presence by monitoring WhatsApp groups and automatically reposting videos to Instagram, TikTok, YouTube, and LinkedIn.**

---

## ⚠️ IMPORTANT DISCLAIMER

**USE AT YOUR OWN RISK!**

This tool uses **unofficial APIs and automation techniques** that may violate the Terms of Service of:
- WhatsApp
- Instagram
- TikTok
- YouTube
- LinkedIn

**Potential Risks:**
- 🚫 **Account bans** or permanent suspension
- 🔒 **Shadowbanning** or reduced reach
- ⚖️ **Legal consequences** for ToS violations
- 🛡️ **Security risks** from storing credentials

**This software is provided for educational purposes only.** The authors and contributors are not responsible for any misuse, damages, or consequences arising from the use of this tool.

---

## 🌟 What is This?

Imagine this: You're part of multiple WhatsApp groups where people share amazing videos from Instagram, TikTok, or YouTube. Instead of manually downloading and reposting these videos to your social media accounts, this tool does it **automatically** for you!

**How it works:**
1. 📱 You create an "Agent" for each WhatsApp group you want to monitor
2. 🔗 When someone shares a video link in the group (Instagram, TikTok, YouTube, LinkedIn)
3. ⬇️ The agent automatically downloads the video
4. ⬆️ Then uploads it to all your configured social media accounts
5. 🧹 Cleans up temporary files after successful uploads
6. 🔄 Repeats automatically every few minutes!

**Perfect for:**
- Content creators who curate videos from multiple sources
- Social media managers handling multiple accounts
- Marketers automating content distribution
- Anyone who wants to save time on manual reposting

---

## ✨ Features

### Current Features (v0.1.0)
- 📱 **WhatsApp Group Monitoring** - Track multiple WhatsApp groups simultaneously
- 📥 **Smart Video Downloading** - Supports Instagram, TikTok, YouTube, LinkedIn links
- 📤 **Instagram Auto-Upload** - Automatically post videos to Instagram accounts
- 🔐 **Military-Grade Encryption** - All credentials encrypted with AES-256
- 🎨 **Retro Terminal Interface** - Beautiful vintage CLI with keyboard navigation
- 🤖 **Multi-Agent System** - Create unlimited agents, one per WhatsApp group
- 📊 **Account Analytics** - View stats for all connected social media accounts
- 🐳 **Docker Ready** - Each agent can be deployed as an independent container
- 🔒 **Security First** - Input validation, error handling, secure credential storage

### Coming Soon
- 📱 TikTok auto-upload
- 🎥 YouTube Shorts auto-upload
- 💼 LinkedIn auto-upload
- 📈 Advanced analytics dashboard
- 🤝 Team collaboration features
- 🌐 Web dashboard interface

---

## 🎯 Quick Start (For Complete Beginners)

### What You'll Need

1. **A Computer** - Linux (Ubuntu), macOS, or Windows with WSL2
2. **Internet Connection** - To download software and interact with social media
3. **15 Minutes** - That's all it takes to get started!

### Step 1: Open the Terminal

**"What's a terminal?"** It's a black window where you type commands. Don't worry, we'll guide you!

**How to open it:**
- **Linux/Ubuntu**: Press `Ctrl + Alt + T`
- **macOS**: Press `Cmd + Space`, type "Terminal", press Enter
- **Windows**: Install [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install) first

### Step 2: Install Required Software

#### Install Python (if you don't have it)

Python is the programming language this tool uses. Check if you have it:

```bash
python3 --version
```

If you see something like `Python 3.10.x` or higher, you're good! If not:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

**macOS (with Homebrew):**
```bash
brew install python@3.10
```

#### Install Poetry (Dependency Manager)

Poetry manages all the code libraries this tool needs. Install it:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Add Poetry to your PATH (so your computer knows where to find it):

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Verify it worked:

```bash
poetry --version
```

#### Install Git (Version Control)

Git helps you download and update the code:

**Ubuntu/Debian:**
```bash
sudo apt install git
```

**macOS:**
```bash
brew install git
```

### Step 3: Download This Project

Navigate to where you want to store the project (e.g., your home folder):

```bash
cd ~
mkdir -p labs
cd labs
```

Download ("clone") the project:

```bash
git clone https://github.com/alexcolls/.agents.git
cd .agents
```

### Step 4: Install the Project Dependencies

This installs all the code libraries the tool needs:

```bash
poetry install
```

**This might take 2-5 minutes.** Go grab a coffee! ☕

### Step 5: Configure Your Environment

Create your configuration file:

```bash
cp .env.sample .env
```

Edit the `.env` file with your favorite text editor (nano is easiest for beginners):

```bash
nano .env
```

**Change these important settings:**
```bash
MASTER_PASSWORD=your-super-secret-password-here-make-it-long-and-random
CHECK_INTERVAL_MINUTES=5
```

Press `Ctrl + X`, then `Y`, then `Enter` to save and exit.

### Step 6: Run the Tool!

Activate the Poetry environment and start the tool:

```bash
poetry run agents
```

**You should see a beautiful retro terminal interface!** 🎉

---

## 🎮 How to Use

### Main Menu Options

When you run the tool, you'll see 4 options:

```
╔════════════════════════════════════════════╗
║  WhatsApp Video to Social Media Agent     ║
║                                            ║
║  1. 🤖 Add AGENT                          ║
║  2. ⚙️  Config AGENT                       ║
║  3. 📊 See ACCOUNTS                        ║
║  4. 🚪 Exit                                ║
╚════════════════════════════════════════════╝
```

**Navigate with:** ⬆️ ⬇️ Arrow keys | **Select with:** Enter ↵

---

### 1. 🤖 Adding Your First Agent

**An "Agent" is a worker that monitors one WhatsApp group and posts to your social media accounts.**

Select `Add AGENT` and follow the prompts:

#### Step 1: Connect WhatsApp
- A QR code will appear
- Open WhatsApp on your phone
- Go to Settings → Linked Devices → Link a Device
- Scan the QR code
- ✅ Connected!

#### Step 2: Select WhatsApp Group
- You'll see a list of all your WhatsApp groups
- Use ⬆️ ⬇️ arrows to navigate
- Press Enter to select

#### Step 3: Choose Platforms
- Use Space to select platforms (Instagram, TikTok, YouTube, LinkedIn)
- Press Enter when done
- **For now, only Instagram is fully implemented**

#### Step 4: Add Social Media Accounts

For each platform you selected:

1. **Enter username**: Type the username you want to use
2. **Account exists?**
   - **Yes**: Enter your password
   - **No**: The tool will create it for you (just press Enter for auto-generated secure password)
3. **Add another account?** Choose Yes or No

#### Step 5: Success! 🎉

You'll see a beautiful ASCII art celebration:

```
   █████╗  ██████╗ ███████╗███╗   ██╗████████╗    
  ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝    
  ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║       
  ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║       
  ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║       
  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝       
                                                    
   ██████╗██████╗ ███████╗ █████╗ ████████╗███████╗██████╗ ██╗
  ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██║
  ██║     ██████╔╝█████╗  ███████║   ██║   █████╗  ██║  ██║██║
  ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██╔══╝  ██║  ██║╚═╝
  ╚██████╗██║  ██║███████╗██║  ██║   ██║   ███████╗██████╔╝██╗
   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═════╝ ╚═╝
```

Your agent is now monitoring the WhatsApp group and will automatically download and repost videos!

---

### 2. ⚙️ Configuring Agents

Select `Config AGENT` to:
- **View all agents** and their status
- **Modify** platform/account settings
- **Activate/Deactivate** agents temporarily
- **Delete** agents permanently

---

### 3. 📊 Viewing Account Stats

Select `See ACCOUNTS` to view a beautiful table:

```
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┓
┃ WhatsApp Group    ┃ Platform  ┃ Username  ┃ Videos  ┃ Followers┃ Views  ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━┩
│ Tech News         │ Instagram │ @techie   │ 142     │ 12.5K    │ 89.2K  │
│ Funny Videos      │ Instagram │ @laughs   │ 89      │ 5.2K     │ 34.1K  │
│ Travel Content    │ Instagram │ @wanderer │ 67      │ 8.9K     │ 67.8K  │
└───────────────────┴───────────┴───────────┴─────────┴──────────┴────────┘
```

**Features:**
- 📊 Real-time statistics
- 📈 Sort by any column
- 🔄 Auto-refresh every 30 seconds
- 📥 Export to CSV

---

### 4. 🚪 Exit

Safely closes all agents and exits the program.

---

## 🏗️ Architecture

### Project Structure

```
.agents/
├── agents/                      # Main application package
│   ├── __init__.py             # Package initialization
│   ├── cli/                    # Command-line interface
│   │   ├── __init__.py
│   │   ├── main.py            # Entry point
│   │   ├── menus.py           # Interactive menus
│   │   ├── ascii_art.py       # ASCII art and banners
│   │   ├── themes.py          # Terminal themes
│   │   └── styles.py          # Styling utilities
│   ├── core/                   # Core business logic
│   │   ├── __init__.py
│   │   ├── agent.py           # Agent management
│   │   ├── whatsapp_monitor.py # WhatsApp monitoring
│   │   ├── video_downloader.py # Video download logic
│   │   └── social_uploader.py  # Social media upload
│   ├── platforms/              # Platform integrations
│   │   ├── __init__.py
│   │   ├── instagram.py       # Instagram API
│   │   ├── tiktok.py          # TikTok API (coming soon)
│   │   ├── youtube.py         # YouTube API (coming soon)
│   │   └── linkedin.py        # LinkedIn API (coming soon)
│   ├── security/               # Security and encryption
│   │   ├── __init__.py
│   │   ├── encryption.py      # AES-256 encryption
│   │   └── validators.py      # Input validation
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── config.py          # Configuration management
│       ├── logger.py          # Logging setup
│       ├── constants.py       # Application constants
│       └── helpers.py         # Helper functions
├── .agents/                     # Agent storage (git-ignored)
│   ├── tmp/                    # Temporary video files
│   ├── build/                  # Docker images per agent
│   └── *.json                  # Agent configurations (encrypted)
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_agent.py
│   ├── test_encryption.py
│   ├── test_downloader.py
│   └── test_platforms.py
├── docs/                        # Documentation
│   ├── architecture.md
│   ├── api.md
│   ├── deployment.md
│   └── security.md
├── .env                         # Environment variables (git-ignored)
├── .env.sample                  # Environment template
├── .gitignore                   # Git ignore rules
├── pyproject.toml               # Poetry configuration
├── poetry.lock                  # Dependency lock file
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Docker orchestration
├── LICENSE                      # MIT License
├── README.md                    # This file!
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guidelines
└── CODE_OF_CONDUCT.md          # Community standards
```

### Data Flow

```
┌─────────────────┐
│  WhatsApp Group │
│   (New Message) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ WhatsApp Monitor│  ← Scans for video links every X minutes
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Video Downloader│  ← Downloads video to .agents/tmp/
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Social Uploader │  ← Uploads to configured platforms
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ✅ Success!    │  ← Deletes temp file, updates stats
└─────────────────┘
```

---

## 🐳 Docker Deployment

### Why Docker?

Docker lets you run each agent in its own isolated container. This means:
- 🔒 **Security**: Agents can't interfere with each other
- 🚀 **Portability**: Deploy anywhere (your computer, cloud, VPS)
- 📦 **Simplicity**: Everything packaged and ready to go

### Building an Agent Container

After creating an agent through the CLI, build its Docker image:

```bash
poetry run agents build <whatsapp-group-name>
```

This creates a Docker image in `.agents/build/<whatsapp-group-name>.agent`

### Running an Agent Container

```bash
docker run -d \
  --name agent-tech-news \
  -v $(pwd)/.agents:/app/.agents \
  -v $(pwd)/.env:/app/.env \
  --restart unless-stopped \
  whatsapp-social-agent:tech-news
```

### Docker Compose (Multiple Agents)

Run all agents at once:

```bash
docker-compose up -d
```

View logs:

```bash
docker-compose logs -f
```

Stop all agents:

```bash
docker-compose down
```

---

## 🔐 Security

### Encryption

All sensitive data is encrypted using **AES-256** (military-grade encryption):
- Social media passwords
- Session tokens
- API keys
- WhatsApp credentials

The encryption key is derived from your `MASTER_PASSWORD` in `.env`.

**IMPORTANT:** Keep your `.env` file secret! Add it to `.gitignore` (already done).

### Best Practices

1. **Use a strong MASTER_PASSWORD**: At least 20 characters, mix of letters, numbers, symbols
2. **Never commit `.env`**: It contains your master password
3. **Use unique passwords**: Don't reuse passwords across accounts
4. **Enable 2FA where possible**: On your social media accounts
5. **Regular backups**: Backup `.agents/` folder regularly
6. **Monitor for suspicious activity**: Check your accounts regularly

### Data Storage

Agent configurations are stored in `.agents/*.json` with this structure:

```json
{
  "whatsapp_group": "Tech News",
  "created_at": "2025-01-15T10:30:00Z",
  "active": true,
  "platforms": {
    "instagram": {
      "accounts": [
        {
          "username": "techie",
          "password": "<ENCRYPTED>",
          "session_token": "<ENCRYPTED>",
          "stats": {
            "followers": 12500,
            "videos_posted": 142,
            "total_views": 89200
          }
        }
      ]
    }
  }
}
```

---

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/alexcolls/.agents.git
cd .agents

# Install dependencies including dev tools
poetry install --with dev

# Activate the virtual environment
poetry shell

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=agents --cov-report=html

# Run specific test file
poetry run pytest tests/test_agent.py
```

### Code Quality

```bash
# Format code with Black
poetry run black agents/

# Lint with Ruff
poetry run ruff check agents/

# Type checking with mypy
poetry run mypy agents/
```

### Adding a New Platform

1. Create `agents/platforms/newplatform.py`
2. Implement the `Platform` interface:
   ```python
   from agents.platforms.base import Platform
   
   class NewPlatform(Platform):
       def login(self, username: str, password: str) -> bool:
           """Authenticate with the platform"""
           pass
       
       def upload_video(self, video_path: str, caption: str) -> bool:
           """Upload a video"""
           pass
       
       def get_stats(self) -> dict:
           """Retrieve account statistics"""
           pass
   ```
3. Register in `agents/platforms/__init__.py`
4. Add tests in `tests/test_platforms.py`
5. Update documentation

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** and commit: `git commit -m '✨ Add amazing feature'`
4. **Push**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Commit Message Convention

We use emojis for commit messages! Examples:

- ✨ `:sparkles:` New feature
- 🐛 `:bug:` Bug fix
- 📝 `:memo:` Documentation
- 🎨 `:art:` Code style/formatting
- ♻️ `:recycle:` Refactoring
- ⚡ `:zap:` Performance improvement
- 🔒 `:lock:` Security fix
- ✅ `:white_check_mark:` Add tests

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**What this means:**
- ✅ Free to use, modify, and distribute
- ✅ Can be used commercially
- ✅ Must include copyright notice
- ❌ No warranty or liability

---

## 🙏 Credits

### Built With

- [Python](https://www.python.org/) - Programming language
- [Poetry](https://python-poetry.org/) - Dependency management
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- [Questionary](https://questionary.readthedocs.io/) - Interactive prompts
- [Instagrapi](https://github.com/adw0rd/instagrapi) - Instagram private API
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Video downloader
- [Pyppeteer](https://github.com/pyppeteer/pyppeteer) - Browser automation
- [Cryptography](https://cryptography.io/) - Encryption library

### Author

**Alex Colls Outumuro**
- GitHub: [@alexcolls](https://github.com/alexcolls)
- Email: alex@example.com

### Contributors

Thank you to all contributors! 🎉

<!-- Add contributors here -->

---

## 📞 Support

### Need Help?

- 📖 Read the [Documentation](docs/)
- 🐛 Report bugs in [Issues](https://github.com/alexcolls/.agents/issues)
- 💬 Ask questions in [Discussions](https://github.com/alexcolls/.agents/discussions)
- ⭐ Star this repo if you find it useful!

### FAQ

**Q: Is this legal?**
A: The software itself is legal, but using it may violate platform ToS. Use at your own risk.

**Q: Will my accounts get banned?**
A: Possibly. We use unofficial APIs which platforms actively try to block. Use burner accounts for testing.

**Q: Can I use this for commercial purposes?**
A: The code is MIT licensed (free for commercial use), but check platform ToS for automated posting.

**Q: How do I update the tool?**
A: Run `git pull` in the project directory, then `poetry install`.

**Q: Can I monitor multiple WhatsApp groups?**
A: Yes! Create one agent per group.

**Q: How much does this cost?**
A: The software is free. You only pay for hosting if you deploy to a server.

---

## 🗺️ Roadmap

### Version 0.1.0 (Current) - Instagram Only
- ✅ WhatsApp monitoring
- ✅ Video downloading
- ✅ Instagram upload
- ✅ Retro CLI interface
- ✅ Docker support

### Version 0.2.0 - TikTok Integration
- ⏳ TikTok account creation
- ⏳ TikTok video upload
- ⏳ TikTok analytics

### Version 0.3.0 - YouTube Shorts
- ⏳ YouTube authentication
- ⏳ Shorts upload
- ⏳ YouTube analytics

### Version 0.4.0 - LinkedIn
- ⏳ LinkedIn video posts
- ⏳ LinkedIn analytics

### Version 1.0.0 - Full Release
- ⏳ Web dashboard
- ⏳ Advanced scheduling
- ⏳ AI-powered captions
- ⏳ Team collaboration
- ⏳ Cloud deployment templates

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/alexcolls/.agents?style=social)
![GitHub forks](https://img.shields.io/github/forks/alexcolls/.agents?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/alexcolls/.agents?style=social)
![GitHub issues](https://img.shields.io/github/issues/alexcolls/.agents)
![GitHub pull requests](https://img.shields.io/github/issues-pr/alexcolls/.agents)

---

<div align="center">

**Made with ❤️ by [Alex Colls Outumuro](https://github.com/alexcolls)**

**Star ⭐ this repo if you find it useful!**

</div>
