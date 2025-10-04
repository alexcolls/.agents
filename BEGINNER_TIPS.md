# 💡 Beginner Tips & Tricks

Welcome! Here are some helpful tips for using `.agents` if you're new to programming or automation tools.

---

## 🎓 Terminal Basics

### Understanding Commands

When you see commands like this:

```bash
./install.sh
```

- `./` means "run this file in the current directory"
- `install.sh` is the name of the script file

### Common Terminal Commands

| Command    | What it does           | Example               |
| ---------- | ---------------------- | --------------------- |
| `cd`       | Change directory       | `cd labs`             |
| `ls`       | List files             | `ls -la`              |
| `pwd`      | Show current directory | `pwd`                 |
| `nano`     | Edit files             | `nano .env`           |
| `cat`      | Display file contents  | `cat .env`            |
| `chmod +x` | Make file executable   | `chmod +x install.sh` |
| `./`       | Run a script           | `./run.sh`            |

### Keyboard Shortcuts

| Shortcut     | What it does                    |
| ------------ | ------------------------------- |
| `Ctrl + C`   | Stop current command            |
| `Ctrl + D`   | Exit terminal                   |
| `Tab`        | Auto-complete file/folder names |
| `Up Arrow`   | Previous command                |
| `Down Arrow` | Next command                    |
| `Ctrl + L`   | Clear screen                    |

---

## 🛠️ Installation Tips

### Before Installing

1. **Check your internet connection** - You'll download ~500MB of data
2. **Have 15 minutes free** - Don't interrupt the installation
3. **Close other programs** - Free up system resources

### During Installation

- **Read the prompts carefully** - The installer asks questions
- **Type "1" or "2"** when choosing modes
- **Press Enter** to confirm choices
- **Wait patiently** when it says "Installing..." (can take 2-5 minutes)

### After Installation

1. **Always configure .env first** before running
2. **Use a strong password** for MASTER_PASSWORD
3. **Test with one agent** before creating multiple

---

## ⚙️ Configuration Guide

### Editing the .env File

#### Step-by-step:

1. Open the file:

   ```bash
   nano .env
   ```

2. You'll see something like:

   ```
   MASTER_PASSWORD=please-change-this...
   ```

3. Use arrow keys to navigate to the text you want to change

4. Delete old text with `Backspace`

5. Type your new password

6. Save and exit:
   - Press `Ctrl + X`
   - Press `Y` (Yes, save)
   - Press `Enter` (confirm filename)

### Choosing a Master Password

**Good password examples:**

- `MyV3ryS3cur3Passw0rd!2025#AgentsRock`
- `Sup3rS@f3P@ssw0rd!For.Agents#2025`
- `I<3Autom@tion!Agents.2025@MyPassword`

**Bad password examples:**

- `password123` ❌ Too simple
- `12345678` ❌ Too simple
- `qwerty` ❌ Too simple

**Password requirements:**

- ✅ At least 20 characters
- ✅ Mix of uppercase and lowercase
- ✅ Include numbers
- ✅ Include special characters (@, #, !, etc.)
- ✅ No personal information (birthdays, names)

---

## 🚀 Running the Tool

### Three Ways to Run

#### 1. Quick Run (Easiest!)

```bash
./run.sh
```

- Checks if everything is installed
- Installs if needed
- Launches the program

#### 2. Poetry Run (Recommended)

```bash
poetry run python -m src.main
```

- Runs in isolated environment
- Safest method
- Always works

#### 3. Global Command (After Installation)

```bash
.agents
```

- Run from anywhere
- Only works after User Mode installation
- Fastest method

---

## 🐛 Common Problems & Solutions

### Problem: "Permission denied"

**Error message:**

```
bash: ./install.sh: Permission denied
```

**Solution:**

```bash
chmod +x install.sh run.sh
```

### Problem: "Poetry not found"

**Error message:**

```
bash: poetry: command not found
```

**Solutions:**

1. Add Poetry to PATH:

   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

2. Restart terminal

3. Or reinstall Poetry:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

### Problem: "Python version too old"

**Error message:**

```
Python 3.8 found, but we need Python 3.10+
```

**Solution:**
Let the installer handle it, or manually install:

**Ubuntu:**

```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

**macOS:**

```bash
brew install python@3.10
```

### Problem: ".env file not found"

**Error message:**

```
Warning: .env file not found!
```

**Solution:**

```bash
cp .env.sample .env
nano .env  # Edit and set your MASTER_PASSWORD
```

### Problem: "Module not found"

**Error message:**

```
ModuleNotFoundError: No module named 'rich'
```

**Solution:**

```bash
poetry install
```

---

## 🔒 Security Best Practices

### Do's ✅

- ✅ Use a unique, strong master password
- ✅ Keep your `.env` file secret
- ✅ Use burner accounts for testing
- ✅ Check `.gitignore` includes `.env`
- ✅ Enable 2FA on your social accounts
- ✅ Regularly backup `.agents/` folder
- ✅ Monitor your accounts for suspicious activity

### Don'ts ❌

- ❌ Share your `.env` file with anyone
- ❌ Commit `.env` to git
- ❌ Use your main social accounts for testing
- ❌ Use the default master password
- ❌ Share screenshots with passwords visible
- ❌ Run on public/shared computers
- ❌ Ignore platform Terms of Service warnings

---

## 📚 Understanding Project Structure

```
.agents/
├── install.sh          ← Run this to install
├── run.sh              ← Run this to start
├── QUICKSTART.md       ← Quick start guide (you are here!)
├── README.md           ← Full documentation
├── .env                ← Your configuration (git-ignored)
├── .env.sample         ← Template for .env
├── pyproject.toml      ← Project dependencies
├── poetry.lock         ← Locked dependency versions
├── src/                ← Source code
│   ├── main.py         ← Entry point
│   ├── cli/            ← Command-line interface
│   ├── core/           ← Business logic
│   ├── platforms/      ← Instagram, TikTok, etc.
│   ├── security/       ← Encryption & validation
│   └── utils/          ← Helper functions
├── .agents/            ← Agent storage (created automatically)
│   ├── tmp/            ← Temporary video downloads
│   ├── build/          ← Docker images
│   └── *.json          ← Agent configurations (encrypted)
└── tests/              ← Test suite
```

### Important Files

| File             | Purpose            | Can I Edit?                |
| ---------------- | ------------------ | -------------------------- |
| `.env`           | Your configuration | ✅ Yes, you must!          |
| `.env.sample`    | Template           | ⚠️ Don't need to           |
| `install.sh`     | Installer          | ⚠️ Advanced users only     |
| `run.sh`         | Launcher           | ⚠️ Advanced users only     |
| `src/*`          | Source code        | ⚠️ For developers          |
| `.agents/*.json` | Agents             | ❌ Don't touch (encrypted) |

---

## 💬 Getting Help

### Before Asking for Help

1. **Read error messages carefully** - They often tell you what's wrong
2. **Check this guide** - Most issues are covered here
3. **Try restarting your terminal** - Fixes PATH issues
4. **Reinstall dependencies** - Run `poetry install`
5. **Check your .env file** - Is it configured correctly?

### Where to Get Help

1. **QUICKSTART.md** - Basic setup guide
2. **README.md** - Full documentation
3. **GitHub Issues** - Report bugs
4. **GitHub Discussions** - Ask questions
5. **Stack Overflow** - General programming questions

### How to Report a Bug

Include this information:

1. **What you tried to do**

   - "I ran ./install.sh"

2. **What happened**

   - "Got error: Poetry not found"

3. **Your system**

   - OS: Ubuntu 22.04
   - Python: 3.10.12
   - Shell: bash

4. **Error message** (copy the full text)

   ```
   bash: poetry: command not found
   ```

5. **What you've tried**
   - "Restarted terminal"
   - "Ran export PATH=..."

---

## 🎯 Next Steps

After reading this guide:

1. ✅ Run the installer: `./install.sh`
2. ✅ Configure your .env: `nano .env`
3. ✅ Run the tool: `./run.sh`
4. ✅ Create your first agent
5. ✅ Start automating!

---

## 📝 Quick Reference Card

Print this out and keep it near your computer!

```
╔══════════════════════════════════════════════════════════╗
║              .AGENTS QUICK REFERENCE                     ║
╠══════════════════════════════════════════════════════════╣
║ Install          │  ./install.sh                         ║
║ Run              │  ./run.sh or .agents                  ║
║ Configure        │  nano .env                            ║
║ Update deps      │  poetry install                       ║
║ Check Python     │  python3 --version                    ║
║ Check Poetry     │  poetry --version                     ║
╠══════════════════════════════════════════════════════════╣
║ Save in nano     │  Ctrl+X, then Y, then Enter          ║
║ Stop command     │  Ctrl+C                               ║
║ Clear screen     │  Ctrl+L or 'clear'                    ║
║ Previous command │  Up Arrow                             ║
╠══════════════════════════════════════════════════════════╣
║ IMPORTANT:       │  Always edit .env first!              ║
║                  │  Set a strong MASTER_PASSWORD         ║
║                  │  Never commit .env to git             ║
╚══════════════════════════════════════════════════════════╝
```

---

**You've got this! 💪**

Remember: Everyone was a beginner once. Don't be afraid to ask questions!

**Happy Automating! 🤖**
