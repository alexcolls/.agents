# 🚀 Quick Start Guide for Beginners

Welcome! This guide will help you install and run `.agents` even if you've never used a terminal before.

---

## 📋 What You Need

- **A Computer**: Linux (Ubuntu), macOS, or Windows with WSL2
- **10-15 Minutes**: That's all!
- **Internet Connection**: To download software

---

## 🎯 Super Easy Installation (3 Steps!)

### Step 1: Open Terminal

**"What's a terminal?"** → It's a black window where you type commands.

**How to open:**
- **Linux/Ubuntu**: Press `Ctrl + Alt + T`
- **macOS**: Press `Cmd + Space`, type "Terminal", press Enter
- **Windows**: Install [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install) first, then use Ubuntu

### Step 2: Navigate to the Project

If you haven't downloaded the project yet:

```bash
cd ~
mkdir -p labs
cd labs
git clone https://github.com/alexcolls/.agents.git
cd .agents
```

If you already have the project:

```bash
cd ~/labs/.agents
```

### Step 3: Run the Installer!

Just type this and press Enter:

```bash
./install.sh
```

**That's it!** The installer will:
- ✅ Check if you have Python (install it if needed)
- ✅ Install Poetry (package manager)
- ✅ Install all required libraries
- ✅ Create configuration files
- ✅ Set up the program to run from anywhere

**Follow the prompts** - it's all interactive and easy!

---

## 🎮 Two Easy Ways to Run

### Option 1: Quick Run Script (Easiest!)

```bash
./run.sh
```

This automatically checks everything and launches the program. Perfect for beginners!

### Option 2: Direct Run

```bash
poetry run python -m src.main
```

Or if you installed globally:

```bash
.agents
```

---

## ⚙️ Configuration (Important!)

Before running, you **must** set your master password:

1. Open the configuration file:
   ```bash
   nano .env
   ```

2. Find this line:
   ```
   MASTER_PASSWORD=please-change-this-to-a-very-secure-password-at-least-20-characters
   ```

3. Change it to your own secure password:
   ```
   MASTER_PASSWORD=MyV3ryS3cur3P@ssw0rd!2025#Agents
   ```

4. Save and exit:
   - Press `Ctrl + X`
   - Press `Y` (Yes)
   - Press `Enter`

---

## 🎯 Installation Modes

The installer offers two modes:

### 1. Developer Mode 🛠️
- Full development environment
- Includes testing tools, linters, formatters
- **Choose this if**: You want to contribute or modify the code

### 2. User Mode 👤 (Recommended)
- Minimal installation
- Only what's needed to run the tool
- Creates global `.agents` command
- **Choose this if**: You just want to use the tool

---

## 🐛 Troubleshooting

### "Permission denied" error

Add execute permissions:
```bash
chmod +x install.sh run.sh
```

### "Command not found" after installation

Restart your terminal or run:
```bash
source ~/.bashrc
```

Or for macOS/zsh:
```bash
source ~/.zshrc
```

### Python version too old

The tool needs Python 3.10 or higher. The installer can install it for you, or:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

**macOS:**
```bash
brew install python@3.10
```

### Poetry not working

Make sure Poetry is in your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Add it permanently to your shell:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Dependencies fail to install

Try updating Poetry first:
```bash
poetry self update
poetry update
```

---

## 🔒 Security Tips

1. **Never share your `.env` file** - it contains passwords!
2. **Use a strong master password** - at least 20 characters
3. **Don't commit `.env` to git** - it's already in `.gitignore`
4. **Use burner accounts for testing** - automation can lead to bans

---

## 📚 Next Steps

After installation:

1. ✅ Configure your `.env` file
2. ✅ Run the tool: `./run.sh` or `.agents`
3. ✅ Create your first agent (WhatsApp monitor)
4. ✅ Connect your social media accounts
5. ✅ Let it automate your content!

---

## 🆘 Need Help?

- 📖 Read the full [README.md](README.md)
- 🐛 Report bugs: [GitHub Issues](https://github.com/alexcolls/.agents/issues)
- 💬 Ask questions: [GitHub Discussions](https://github.com/alexcolls/.agents/discussions)
- ⭐ Star the repo if you find it useful!

---

## 📝 Quick Reference

| Command | What it does |
|---------|-------------|
| `./install.sh` | Install the program |
| `./run.sh` | Quick run (checks and starts) |
| `.agents` | Run from anywhere (after install) |
| `nano .env` | Edit configuration |
| `poetry run python -m src.main` | Direct run |
| `poetry install` | Reinstall dependencies |
| `poetry update` | Update dependencies |

---

**Made with ❤️ for beginners!**

If this guide helped you, please ⭐ star the repo!

