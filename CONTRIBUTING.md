# Contributing to .agents

First off, thank you for considering contributing to this project! 🎉

We welcome contributions from everyone, whether you're fixing a typo, adding a feature, or reporting a bug.

## 📜 Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## 🤔 How Can I Contribute?

### Reporting Bugs 🐛

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**
```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. Ubuntu 22.04]
 - Python Version: [e.g. 3.10.5]
 - Project Version: [e.g. 0.1.0]

**Additional context**
Any other context about the problem.
```

### Suggesting Features ✨

Feature suggestions are welcome! Before submitting:

1. Check if the feature is already planned (see [Roadmap in README](README.md#roadmap))
2. Search existing issues to avoid duplicates
3. Provide a clear use case for why the feature would be valuable

**Feature Request Template:**
```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Any alternative solutions or features.

**Additional context**
Any other context, screenshots, or examples.
```

### Contributing Code 💻

We love pull requests! Here's how to contribute:

## 🚀 Getting Started

### 1. Fork & Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/.agents.git
cd .agents
```

### 2. Set Up Development Environment

```bash
# Install Poetry if you haven't
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install --with dev

# Activate virtual environment
poetry shell

# Install pre-commit hooks
pre-commit install
```

### 3. Create a Branch

```bash
# Create a new branch for your feature
git checkout -b feature/amazing-feature

# Or for a bug fix
git checkout -b fix/bug-description
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Adding tests
- `chore/` - Maintenance tasks

### 4. Make Your Changes

#### Code Style Guidelines

We use automated tools to maintain code quality:

```bash
# Format code with Black
poetry run black agents/

# Lint with Ruff
poetry run ruff check agents/

# Type check with mypy
poetry run mypy agents/

# Run all checks
poetry run black agents/ && poetry run ruff check agents/ && poetry run mypy agents/
```

**Code Standards:**
- Line length: 100 characters
- Use type hints wherever possible
- Write docstrings for all public functions/classes
- Follow PEP 8 style guide
- Use absolute imports (per project rules)

**Example Function:**
```python
def download_video(url: str, output_path: str) -> bool:
    """
    Download a video from a given URL.
    
    Args:
        url: The video URL to download
        output_path: Path where the video should be saved
        
    Returns:
        True if download successful, False otherwise
        
    Raises:
        ValueError: If URL is invalid
        IOError: If output path is not writable
    """
    # Implementation here
    pass
```

#### Commit Message Convention

We use emoji prefixes for commit messages (per project rules):

```bash
# Format: <emoji> <type>: <description>

git commit -m "✨ feat: Add TikTok platform integration"
git commit -m "🐛 fix: Resolve Instagram login timeout"
git commit -m "📝 docs: Update installation guide"
git commit -m "🎨 style: Format code with Black"
git commit -m "♻️ refactor: Simplify video downloader logic"
git commit -m "⚡ perf: Optimize encryption performance"
git commit -m "🔒 security: Fix credential exposure vulnerability"
git commit -m "✅ test: Add tests for agent creation"
git commit -m "🔧 chore: Update dependencies"
```

**Emoji Reference:**
- ✨ `:sparkles:` - New feature
- 🐛 `:bug:` - Bug fix
- 📝 `:memo:` - Documentation
- 🎨 `:art:` - Code style/formatting
- ♻️ `:recycle:` - Refactoring
- ⚡ `:zap:` - Performance improvement
- 🔒 `:lock:` - Security fix
- ✅ `:white_check_mark:` - Add tests
- 🔧 `:wrench:` - Configuration changes
- 🚀 `:rocket:` - Deployment
- 🔥 `:fire:` - Remove code/files
- 💚 `:green_heart:` - Fix CI build
- 📦 `:package:` - Update dependencies

**Important:** Always group related changes by feature when committing!

### 5. Write Tests

All new features must include tests:

```bash
# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=agents --cov-report=html

# Run specific test file
poetry run pytest tests/test_agent.py

# Run specific test
poetry run pytest tests/test_agent.py::test_agent_creation
```

**Test Guidelines:**
- Aim for 80%+ code coverage
- Use descriptive test names: `test_agent_creation_with_invalid_name_raises_error`
- Mock external APIs (Instagram, WhatsApp, etc.)
- Test both success and failure cases
- Use pytest fixtures for reusable test data

### 6. Update Documentation

If your changes affect:
- **User behavior**: Update README.md
- **Configuration**: Update .env.sample
- **API/modules**: Update relevant files in docs/
- **Breaking changes**: Update CHANGELOG.md with migration guide

### 7. Update CHANGELOG

**IMPORTANT:** Always update CHANGELOG.md with your changes!

Add your changes under the `[Unreleased]` section:

```markdown
## [Unreleased]

### ✨ Added
- 📱 TikTok platform integration with video upload support

### 🐛 Fixed
- 🔧 Instagram login timeout when 2FA is enabled

### 🔄 Changed
- ⚡ Improved video download speed by 50%

### 🗑️ Removed
- 🔥 Deprecated legacy configuration format
```

### 8. Push & Create Pull Request

```bash
# Push your branch
git push origin feature/amazing-feature
```

Then create a Pull Request on GitHub with:

**PR Title Format:**
```
✨ feat: Add TikTok platform integration
```

**PR Description Template:**
```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran.

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have updated the documentation
- [ ] I have updated CHANGELOG.md
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally
- [ ] Any dependent changes have been merged

## Screenshots (if applicable)

## Related Issues
Closes #123
```

## 🔍 Code Review Process

1. **Automated Checks**: GitHub Actions will run tests and linting
2. **Maintainer Review**: A project maintainer will review your code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, your PR will be merged!

**What we look for:**
- ✅ Clean, readable code
- ✅ Proper error handling
- ✅ Security best practices
- ✅ Comprehensive tests
- ✅ Updated documentation
- ✅ No breaking changes (without discussion)

## 🎯 Priority Areas

We especially welcome contributions in these areas:

### High Priority
- 🔒 Security improvements
- 🐛 Bug fixes
- 📝 Documentation improvements
- ✅ Test coverage improvements

### Medium Priority
- 📱 TikTok integration
- 🎥 YouTube Shorts integration
- 💼 LinkedIn integration
- 📊 Analytics features

### Lower Priority
- 🌐 Web dashboard
- 🤝 Team collaboration
- 🧠 AI features

## 📚 Additional Resources

### Project Structure
```
agents/
├── cli/          # Command-line interface
├── core/         # Core business logic
├── platforms/    # Social media integrations
├── security/     # Encryption & validation
└── utils/        # Utility functions
```

### Key Files
- `agents/cli/main.py` - CLI entry point
- `agents/core/agent.py` - Agent management
- `agents/platforms/instagram.py` - Instagram integration
- `agents/security/encryption.py` - Credential encryption

### Useful Commands
```bash
# Format all code
poetry run black .

# Lint all code
poetry run ruff check .

# Type check
poetry run mypy agents/

# Run all tests with coverage
poetry run pytest --cov=agents --cov-report=term-missing

# Install package in editable mode
poetry install
```

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Questions?

- 📖 Read the [Documentation](docs/)
- 🐛 Check [existing issues](https://github.com/alexcolls/.agents/issues)
- 💬 Start a [discussion](https://github.com/alexcolls/.agents/discussions)
- 📧 Email: alex@example.com

## 🙏 Thank You!

Every contribution, no matter how small, makes this project better. We appreciate your time and effort!

---

**Happy Coding!** 🚀
