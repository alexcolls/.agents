# 🎉 START HERE - Complete Beginner's Guide

**Welcome to .agents!** This file will guide you to get started in **3 simple steps**.

---

## 🚀 3 Steps to Get Started

### Step 1: Open Terminal ⌨️

**How to open terminal:**
- **Linux**: Press `Ctrl + Alt + T`
- **macOS**: Press `Cmd + Space`, type "Terminal", press Enter
- **Windows**: Install WSL2 first, then open Ubuntu terminal

### Step 2: Navigate to Project 📁

```bash
cd ~/labs/.agents
```

### Step 3: Run the Installer 🎯

```bash
./install.sh
```

**That's it!** The installer will guide you through everything.

---

## 📚 Which Guide Should I Read?

Choose based on your experience level:

### 🌱 **Complete Beginner** (Never used terminal before)
1. Read **QUICKSTART.md** first (5 min read)
2. Follow **INSTALLATION_DEMO.md** while installing (visual guide)
3. Keep **BEGINNER_TIPS.md** nearby for reference

### 👤 **Regular User** (Some terminal experience)
1. Run `./install.sh` - it's self-explanatory
2. Read **QUICKSTART.md** if you get stuck (5 min read)
3. Check **BEGINNER_TIPS.md** for troubleshooting

### 🛠️ **Developer** (Want to modify the code)
1. Run `./install.sh` and choose "Developer Mode"
2. Read the main **README.md** for architecture details
3. Check **CONTRIBUTING.md** for development guidelines

---

## 📖 All Available Guides

| File | What's Inside | Read Time |
|------|--------------|-----------|
| **START_HERE.md** | You are here! Quick navigation | 2 min |
| **QUICKSTART.md** | Fast installation guide | 5 min |
| **BEGINNER_TIPS.md** | Terminal basics & troubleshooting | 10 min |
| **INSTALLATION_DEMO.md** | Visual walkthrough with screenshots | 8 min |
| **INSTALLATION_FILES.md** | Technical reference | 5 min |
| **README.md** | Full documentation | 20 min |
| **CONTRIBUTING.md** | How to contribute | 10 min |

---

## ⚡ Super Quick Start (TL;DR)

For those who want to get started immediately:

```bash
# 1. Navigate to project
cd ~/labs/.agents

# 2. Run installer
./install.sh

# 3. Configure (set your password)
nano .env

# 4. Run the tool
./run.sh
```

**Done!** 🎉

---

## 🎯 What the Installer Does

When you run `./install.sh`, it will:

1. ✅ Detect your operating system
2. ✅ Check for Python 3.10+ (install if needed)
3. ✅ Install Poetry package manager
4. ✅ Install all dependencies (~2-5 minutes)
5. ✅ Create your `.env` configuration file
6. ✅ Optionally create global `.agents` command
7. ✅ Ask if you want to run the tool now

**No manual steps required!** Just follow the prompts.

---

## ⚙️ Important: Configure Before Running

**After installation**, you MUST edit the `.env` file:

```bash
nano .env
```

**Change this line:**
```
MASTER_PASSWORD=please-change-this-to-a-very-secure-password
```

**To something secure like:**
```
MASTER_PASSWORD=MyV3ryS3cur3P@ssw0rd!2025#Agents
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

---

## 🎮 How to Run After Installation

### Option 1: Quick Run Script (Easiest!)
```bash
./run.sh
```
Automatically checks everything and starts the program.

### Option 2: Global Command (After User Mode Install)
```bash
.agents
```
Run from anywhere in your terminal!

### Option 3: Using Poetry Directly
```bash
poetry run python -m src.main
```
Most reliable method.

---

## 🆘 Having Issues?

### "Permission denied" Error
```bash
chmod +x install.sh run.sh
./install.sh
```

### "Command not found" Error
Restart your terminal or run:
```bash
source ~/.bashrc  # or ~/.zshrc for macOS
```

### Python Version Too Old
The installer will offer to install Python 3.10+ for you.

### Other Issues
Check **BEGINNER_TIPS.md** - it has solutions for common problems!

---

## 🔒 Security Reminder

1. ⚠️ **Never share your `.env` file**
2. ⚠️ **Use a strong MASTER_PASSWORD** (20+ characters)
3. ⚠️ **Test with burner accounts** first
4. ⚠️ **Read the disclaimer** in README.md about ToS violations

---

## 🎊 Next Steps After Installation

1. ✅ Configure your `.env` file
2. ✅ Run the tool: `./run.sh`
3. ✅ Create your first agent (WhatsApp monitor)
4. ✅ Connect social media accounts
5. ✅ Start automating!

---

## 💡 Pro Tips

- **Save time:** Use Tab key for auto-complete
- **See history:** Press Up Arrow for previous commands
- **Stop command:** Press Ctrl+C to interrupt
- **Clear screen:** Press Ctrl+L or type `clear`
- **Get help:** All guides are in Markdown - view in any text editor!

---

## 📞 Need More Help?

- 🐛 **Bug reports:** [GitHub Issues](https://github.com/alexcolls/.agents/issues)
- 💬 **Questions:** [GitHub Discussions](https://github.com/alexcolls/.agents/discussions)
- 📧 **Email:** alexcollsoutumuro@gmail.com
- 🐦 **Twitter:** [@moriarsans](https://x.com/moriarsans)

---

## 🎁 Quick Reference Card

```
╔═══════════════════════════════════════════════════════════╗
║              .AGENTS - QUICK REFERENCE                    ║
╠═══════════════════════════════════════════════════════════╣
║ Install            │  ./install.sh                        ║
║ Run                │  ./run.sh or .agents                 ║
║ Configure          │  nano .env                           ║
║ Update deps        │  poetry install                      ║
╠═══════════════════════════════════════════════════════════╣
║ FIRST TIME SETUP:                                         ║
║   1. ./install.sh                                         ║
║   2. nano .env    (set MASTER_PASSWORD)                   ║
║   3. ./run.sh                                             ║
╠═══════════════════════════════════════════════════════════╣
║ TROUBLESHOOTING:                                          ║
║   • Permission denied → chmod +x install.sh run.sh        ║
║   • Command not found → source ~/.bashrc                  ║
║   • Check BEGINNER_TIPS.md for more                       ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 🌟 You're All Set!

**Everything you need to get started is in this directory.**

The installation is designed to be **beginner-friendly** with:
- 🎨 Colored, interactive prompts
- ✅ Automatic dependency detection
- 📝 Comprehensive error messages
- 🆘 Built-in troubleshooting

**Just run `./install.sh` and follow the prompts!**

---

**Ready? Let's go! 🚀**

```bash
./install.sh
```

---

<div align="center">

**Made with ❤️ for beginners!**

**Star ⭐ this repo if you find it useful!**

[GitHub](https://github.com/alexcolls/.agents) • [Twitter](https://x.com/moriarsans) • [Email](mailto:alexcollsoutumuro@gmail.com)

</div>
