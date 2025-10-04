# 🎬 Installation Demo - What You'll See

This guide shows you **exactly** what the installation process looks like step-by-step.

---

## 📺 Visual Walkthrough

### Step 1: Open Terminal

Your terminal will look something like this:

```
quantium@computer:~$
```

The `~` means you're in your home directory.

---

### Step 2: Navigate to Project

Type: `cd labs/.agents`

```bash
quantium@computer:~$ cd labs/.agents
quantium@computer:~/labs/.agents$
```

---

### Step 3: Run Installer

Type: `./install.sh`

```bash
quantium@computer:~/labs/.agents$ ./install.sh
```

You'll see:

```
╔════════════════════════════════════════════════════════════════╗
║                    🤖 .agents Installer                        ║
║            WhatsApp to Social Media Automation                 ║
╚════════════════════════════════════════════════════════════════╝

ℹ Detected OS: debian

Choose installation mode:
1) Developer Mode  - Full development environment with all tools
2) User Mode       - Minimal installation for running the tool

Enter your choice (1 or 2):
```

**What to do:** Type `2` and press Enter (for User Mode)

---

### Step 4: Python Check

The installer will check for Python:

```
▶ Checking Python installation...

✓ Python 3.10.12 detected
```

**If Python is not found, you'll see:**

```
⚠ Python 3 not found
Install Python automatically? (Y/n):
```

**What to do:** Press `Y` and Enter

The installer will then install Python:

```
▶ Installing Python 3.10+

ℹ Installing Python using apt...
[sudo] password for quantium:
```

**What to do:** Enter your computer password (you won't see characters as you type - this is normal!)

---

### Step 5: Poetry Installation

```
▶ Installing Poetry (dependency manager)

ℹ Downloading Poetry installer...
Retrieving Poetry metadata

# Welcome to Poetry!

✓ Poetry installed successfully!
Poetry (version 1.7.1)
```

---

### Step 6: Installing Dependencies

```
▶ Installing project dependencies

ℹ This might take 2-5 minutes... ☕

Installing dependencies from lock file

Package operations: 42 installs, 0 updates, 0 removals

  • Installing certifi (2024.2.2)
  • Installing charset-normalizer (3.3.2)
  • Installing idna (3.6)
  • Installing urllib3 (2.2.0)
  • Installing requests (2.31.0)
  • Installing rich (13.7.0)
  • Installing questionary (2.0.1)
  ...
  • Installing instagrapi (2.1.0)
  • Installing yt-dlp (2024.1.0)

✓ All dependencies installed!
```

---

### Step 7: Environment Setup

```
▶ Setting up environment configuration

✓ Created .env file from template
⚠ IMPORTANT: Edit .env file and set your MASTER_PASSWORD!
ℹ Run: nano .env
```

---

### Step 8: Global Alias (User Mode)

```
▶ Creating global command '.agents'

Create global '.agents' command? (Y/n):
```

**What to do:** Press `Y` and Enter

```
✓ Added alias to /home/quantium/.bashrc
ℹ You can now run '.agents' from anywhere!
⚠ Restart your terminal or run: source ~/.bashrc
```

---

### Step 9: Installation Complete! 🎉

```

╔════════════════════════════════════════════════════════════════╗
║              ✓ Installation Complete! 🎉                      ║
╚════════════════════════════════════════════════════════════════╝

ℹ Next steps:
  1. Edit .env file: nano .env
  2. Set a strong MASTER_PASSWORD
  3. Restart your terminal or run: source ~/.bashrc
  4. Run the tool from anywhere: .agents


Do you want to run the tool now? (Y/n):
```

**What to do:** Press `n` (you need to configure .env first!)

---

## 🎯 Quick Run Demo

After installation, when you run `./run.sh`:

```bash
quantium@computer:~/labs/.agents$ ./run.sh
```

You'll see:

```
🤖 .agents - Quick Run

✓ Poetry found
✓ Dependencies installed
✓ .env file found

Starting .agents...

╔════════════════════════════════════════════════════════════════╗
║                    🤖 Welcome to .agents                       ║
║                                                                ║
║         WhatsApp to Social Media Automation Tool               ║
║                      Version 0.1.0                            ║
║                                                                ║
║              ⚠️  This is a development preview                 ║
║          The full CLI interface is coming soon!                ║
╚════════════════════════════════════════════════════════════════╝

Quick Start:
  1. Make sure your .env file is configured
  2. Set a strong MASTER_PASSWORD
  3. The full CLI interface is under development

For more information, visit: https://github.com/alexcolls/.agents
```

---

## 🛠️ Editing .env Demo

Type: `nano .env`

```bash
quantium@computer:~/labs/.agents$ nano .env
```

You'll see the nano editor:

```
  GNU nano 6.2                    .env                    Modified

# Master password for encrypting credentials (CHANGE THIS!)
MASTER_PASSWORD=please-change-this-to-a-very-secure-password

# How often to check WhatsApp groups for new videos (in minutes)
CHECK_INTERVAL_MINUTES=5

# Maximum video file size to download (in MB)
MAX_VIDEO_SIZE_MB=500

...






^G Help      ^O Write Out  ^W Where Is   ^K Cut        ^T Execute
^X Exit      ^R Read File  ^\ Replace    ^U Paste      ^J Justify
```

**Steps to edit:**

1. Use **arrow keys** to navigate to the password line
2. Use **Backspace** to delete the default password
3. Type your new secure password
4. Press **Ctrl + X** to exit
5. Press **Y** to save
6. Press **Enter** to confirm

You should see:

```
[ Wrote 27 lines ]
quantium@computer:~/labs/.agents$
```

---

## 🎊 Success! You're Ready!

Now you can run the tool:

**Option 1: From the project directory**

```bash
./run.sh
```

**Option 2: From anywhere (after User Mode install)**

```bash
.agents
```

**Option 3: Using Poetry directly**

```bash
poetry run python -m src.main
```

---

## 🐛 Common Error Messages

### "Permission denied"

```bash
quantium@computer:~/labs/.agents$ ./install.sh
bash: ./install.sh: Permission denied
```

**Fix:**

```bash
chmod +x install.sh run.sh
```

### "Poetry not found" (after installation)

```bash
quantium@computer:~/labs/.agents$ ./run.sh
Poetry not found. Running installer...
```

**Fix:** Restart your terminal or run:

```bash
source ~/.bashrc
```

### ".env file not found"

```bash
Warning: .env file not found!
Creating .env from .env.sample...
IMPORTANT: Edit .env and set your MASTER_PASSWORD!
Run: nano .env

Press Enter after editing .env to continue...
```

**Fix:** Edit the .env file as instructed, then press Enter.

---

## 💡 Pro Tips

### Tip 1: Use Tab Completion

Instead of typing the full filename:

```bash
./ins[TAB]
```

Press Tab and it auto-completes to:

```bash
./install.sh
```

### Tip 2: View Command History

Press **Up Arrow** to see previous commands. Super useful for repeating commands!

### Tip 3: Clear Screen

Terminal getting messy? Press **Ctrl + L** or type `clear`

### Tip 4: Stop a Running Command

If something goes wrong, press **Ctrl + C** to stop the current command.

---

## 📞 Need Help?

If your installation doesn't look like this, or you encounter errors:

1. Check [BEGINNER_TIPS.md](BEGINNER_TIPS.md) for troubleshooting
2. Read [QUICKSTART.md](QUICKSTART.md) for step-by-step guide
3. Check [GitHub Issues](https://github.com/alexcolls/.agents/issues)
4. Ask in [GitHub Discussions](https://github.com/alexcolls/.agents/discussions)

---

**Remember:** The installer is interactive and beginner-friendly. Just follow the prompts, and you'll be up and running in minutes! 🚀

**Good luck! 🎉**
