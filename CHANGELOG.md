# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### ✨ Added
- 🛠️ Created `utils/constants.py` with 270+ lines of application constants
- 🎯 Defined all supported platforms (Instagram, TikTok, YouTube, LinkedIn)
- 🔍 Added regex patterns for detecting video URLs from all platforms
- 📝 Defined default configuration values for all settings
- 🎨 Added retro terminal color schemes (Amber, Green Phosphor)
- 📝 Defined all error and success messages
- 🔐 Added validation patterns for usernames and emails

### 🔄 Changed
- 🏷️ Rebranded project to `.agents` for cleaner naming
- 📝 Updated all documentation and repository references
- 🔧 Updated git remote to point to new repository URL

### Planned Features
- 📱 TikTok platform integration
- 🎥 YouTube Shorts platform integration
- 💼 LinkedIn platform integration
- 🌐 Web dashboard interface
- 📊 Advanced analytics and reporting
- 🤝 Team collaboration features
- 🔔 Email and Telegram notifications
- 🧠 AI-powered caption generation
- 📅 Advanced scheduling system
- ☁️ Cloud deployment templates

---

## [0.1.0] - 2025-10-04

### 🎉 Initial Release

This is the first alpha release of WhatsApp Video to Social Media Agent. The project provides automated video reposting from WhatsApp groups to Instagram accounts.

### ✨ Added

#### Project Setup
- 📦 Initialized Poetry project with Python 3.10+ support
- 🏗️ Created complete project structure with modular architecture
- 📝 Added comprehensive README.md with beginner-friendly installation guide
- ⚖️ Added MIT License
- 🔧 Configured pyproject.toml with all dependencies and dev tools
- 🎨 Configured code quality tools (Black, Ruff, Mypy, Pytest)

#### Configuration
- 🔐 Created detailed `.env.sample` with 60+ configuration options
- 📋 Added comprehensive .gitignore with project-specific patterns
- 🛠️ Configured Poetry with local virtual environment support
- 📝 Created CONTRIBUTING.md with detailed contribution guidelines
- 📜 Created CHANGELOG.md to track all project changes

#### Directory Structure
- 📁 `agents/` - Main application package
  - `cli/` - Command-line interface components
  - `core/` - Core business logic
  - `platforms/` - Platform integrations
  - `security/` - Encryption and security utilities
  - `utils/` - Utility functions
- 📁 `.agents/` - Agent storage directory (git-ignored)
  - `tmp/` - Temporary video downloads
  - `build/` - Docker image builds
- 📁 `tests/` - Test suite directory
- 📁 `docs/` - Documentation directory

#### Dependencies

**Production:**
- `rich ^13.7.0` - Beautiful terminal output
- `questionary ^2.0.1` - Interactive CLI prompts
- `cryptography ^42.0.0` - AES-256 encryption
- `python-dotenv ^1.0.0` - Environment variable management
- `instagrapi ^2.1.0` - Instagram private API
- `yt-dlp ^2024.1.0` - Video downloader
- `requests ^2.31.0` - HTTP library
- `pyppeteer ^2.0.0` - Browser automation
- `playwright ^1.40.0` - Browser automation framework
- `pillow ^10.2.0` - Image processing
- `qrcode ^7.4.2` - QR code generation for WhatsApp

**Development:**
- `pytest ^7.4.3` - Testing framework
- `pytest-cov ^4.1.0` - Coverage reporting
- `pytest-asyncio ^0.23.0` - Async testing
- `black ^24.1.0` - Code formatter
- `ruff ^0.1.14` - Fast Python linter
- `mypy ^1.8.0` - Static type checker
- `pre-commit ^3.6.0` - Git hooks
- `ipython ^8.20.0` - Enhanced REPL

### 📚 Documentation
- ✅ Complete README with installation guide for beginners
- ✅ Architecture overview and data flow diagrams
- ✅ Usage instructions for all CLI commands
- ✅ Docker deployment guide
- ✅ Security best practices
- ✅ Development setup guide
- ✅ Contributing guidelines
- ✅ FAQ section

### 🔒 Security
- ✅ AES-256 encryption for all credentials
- ✅ Master password-based key derivation
- ✅ Secure credential storage in `.agents/*.json`
- ✅ Environment variable protection via .gitignore
- ✅ Clear security warnings in documentation

### ⚠️ Known Limitations
- Only Instagram platform is implemented (TikTok, YouTube, LinkedIn coming soon)
- WhatsApp integration uses unofficial APIs (risk of account bans)
- Instagram account creation automation is complex (CAPTCHA challenges)
- No web dashboard yet (CLI only)
- Single-user mode (no team collaboration)

### 🐛 Known Issues
- None yet (first release)

---

## Version History

- **0.1.0** (2025-10-04) - Initial alpha release with Instagram support

---

## Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- How to submit bug reports
- How to propose new features
- Code style guidelines
- Pull request process

---

## Links

- **Repository**: https://github.com/alexcolls/.agents
- **Issue Tracker**: https://github.com/alexcolls/.agents/issues
- **Documentation**: [docs/](docs/)

---

**Note**: This project uses unofficial APIs which may violate platform Terms of Service. Use at your own risk. See [README.md](README.md) for full disclaimer.
