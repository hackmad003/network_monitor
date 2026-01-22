# Contributing to Network Monitor

Thank you for your interest in contributing to Network Monitor! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/network-monitor.git
   cd network-monitor
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

1. **Install Python 3.8+** if not already installed
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies** including dev tools:
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```
4. **Set up your database** following QUICKSTART.md
5. **Configure your .env** file

## Coding Standards

### Python Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions, classes, and modules
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

### Code Quality Tools
Run these before committing:
```bash
# Format code
black src/

# Check style
flake8 src/

# Type checking
mypy src/

# Linting
pylint src/
```

### Testing
- Write tests for new features
- Ensure existing tests pass
- Aim for >80% code coverage
```bash
pytest tests/
pytest --cov=src tests/
```

## Commit Messages

Use clear, descriptive commit messages:
- **Format**: `type: brief description`
- **Types**: 
  - `feat`: New feature
  - `fix`: Bug fix
  - `docs`: Documentation changes
  - `style`: Code style changes (formatting, etc.)
  - `refactor`: Code refactoring
  - `test`: Adding or updating tests
  - `chore`: Maintenance tasks

**Examples**:
```
feat: add email notifications for device events
fix: resolve database connection timeout issue
docs: update installation instructions for Linux
```

## Pull Request Process

1. **Update documentation** if you've changed functionality
2. **Add tests** for new features
3. **Update CHANGELOG.md** with your changes
4. **Ensure all tests pass** and code meets quality standards
5. **Create a Pull Request** with:
   - Clear title describing the change
   - Detailed description of what and why
   - Reference any related issues (#123)
   - Screenshots if applicable (UI changes)

## Code Review

- Be open to feedback and suggestions
- Respond to review comments promptly
- Make requested changes in new commits
- Once approved, a maintainer will merge your PR

## Reporting Bugs

Use GitHub Issues and include:
- **Description**: Clear description of the bug
- **Steps to Reproduce**: Detailed steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python version, SQL Server version
- **Logs**: Relevant log output
- **Screenshots**: If applicable

## Feature Requests

We welcome feature requests! Please:
- Check if the feature already exists or is planned
- Describe the use case and benefits
- Provide examples if possible
- Be open to discussion and alternatives

## Questions?

- Check existing documentation (README.md, QUICKSTART.md)
- Search existing issues on GitHub
- Create a new issue with the "question" label

## Code of Conduct

### Our Standards
- Be respectful and inclusive
- Welcome newcomers and beginners
- Accept constructive criticism gracefully
- Focus on what's best for the project
- Show empathy towards others

### Unacceptable Behavior
- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Network Monitor! 🎉
