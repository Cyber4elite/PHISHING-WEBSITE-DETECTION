# Contributing to PhishShield

Thank you for your interest in contributing to PhishShield! This guide will help you get started with contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Contributing Guidelines](#contributing-guidelines)
- [Types of Contributions](#types-of-contributions)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what's best for the community
- Show empathy towards other community members
- Be constructive in feedback and discussions

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A code editor (VS Code, PyCharm, etc.)
- Basic knowledge of Django and Python

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/phishshield.git
   cd phishshield
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-repo/phishshield.git
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-number-description
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements/development.txt

# Set up database
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 3. Make Your Changes

- Write clean, readable code
- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes

```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test scanner.tests.test_models

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### 5. Commit Your Changes

```bash
# Add your changes
git add .

# Commit with descriptive message
git commit -m "Add feature: brief description of changes"

# Push to your fork
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill out the pull request template
5. Submit the pull request

## Contributing Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Use type hints where appropriate

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add feature: URL validation with regex patterns"
git commit -m "Fix bug: handle empty URL input gracefully"
git commit -m "Update docs: add API endpoint examples"

# Bad
git commit -m "fix stuff"
git commit -m "update"
git commit -m "changes"
```

### Pull Request Guidelines

- **One feature per PR**: Keep pull requests focused on a single feature or bug fix
- **Descriptive title**: Use a clear, descriptive title
- **Detailed description**: Explain what changes you made and why
- **Reference issues**: Link to related issues using `#issue-number`
- **Screenshots**: Include screenshots for UI changes
- **Testing**: Ensure all tests pass

## Types of Contributions

### Bug Reports

When reporting bugs, include:

1. **Clear description** of the bug
2. **Steps to reproduce** the issue
3. **Expected behavior** vs actual behavior
4. **System information** (OS, Python version, etc.)
5. **Error messages** and logs
6. **Screenshots** if applicable

### Feature Requests

When requesting features, include:

1. **Clear description** of the feature
2. **Use case** and motivation
3. **Proposed implementation** (if you have ideas)
4. **Alternatives considered**
5. **Additional context**

### Code Contributions

We welcome contributions in:

- **Bug fixes**
- **New features**
- **Performance improvements**
- **Documentation updates**
- **Test coverage**
- **Code refactoring**

### Documentation

Help improve documentation:

- **User guides**
- **API documentation**
- **Code comments**
- **README updates**
- **Troubleshooting guides**

## Development Setup

### Environment Configuration

Create a `.env` file for development:

```bash
# .env
DEBUG=True
SECRET_KEY=your-development-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### IDE Configuration

#### VS Code

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["."],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/node_modules": true,
        "**/.pytest_cache": true
    }
}
```

#### PyCharm

1. Open project in PyCharm
2. Configure Python interpreter to use virtual environment
3. Enable Django support
4. Configure test runner to use pytest

### Pre-commit Hooks

Set up pre-commit hooks for code quality:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files
```

## Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test scanner.tests.test_models

# Run specific test
python manage.py test scanner.tests.test_models.ScanReportModelTest.test_scan_report_creation

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Writing Tests

Follow these guidelines:

1. **Test naming**: Use descriptive test names
2. **Test structure**: Arrange, Act, Assert
3. **Test isolation**: Each test should be independent
4. **Test coverage**: Aim for high test coverage
5. **Mock external dependencies**: Use mocks for external services

Example test:

```python
def test_scan_report_creation(self):
    """Test creating a scan report with valid data"""
    # Arrange
    url = 'https://example.com'
    features = {'url_length': 19, 'is_https': True}
    
    # Act
    report = ScanReport.objects.create(
        url=url,
        result='legitimate',
        confidence=0.95,
        features=features
    )
    
    # Assert
    self.assertEqual(report.url, url)
    self.assertEqual(report.result, 'legitimate')
    self.assertEqual(report.confidence, 0.95)
```

## Documentation

### Code Documentation

- **Docstrings**: Add docstrings to all functions and classes
- **Comments**: Add comments for complex logic
- **Type hints**: Use type hints for better code clarity

Example:

```python
def extract_features(url: str) -> dict:
    """
    Extract features from URL for phishing detection.
    
    Args:
        url (str): The URL to analyze
        
    Returns:
        dict: Dictionary containing extracted features
        
    Raises:
        ValueError: If URL is invalid
    """
    # Implementation
    pass
```

### User Documentation

- **Clear instructions**: Write clear, step-by-step instructions
- **Examples**: Include practical examples
- **Screenshots**: Add screenshots for UI documentation
- **Troubleshooting**: Include common issues and solutions

## Submitting Changes

### Before Submitting

1. **Run tests**: Ensure all tests pass
2. **Check code style**: Run linting tools
3. **Update documentation**: Update relevant documentation
4. **Test manually**: Test your changes manually
5. **Check for conflicts**: Ensure no merge conflicts

### Pull Request Template

Use this template for pull requests:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Related Issues
Fixes #issue-number
```

## Review Process

### What We Look For

1. **Code quality**: Clean, readable, well-documented code
2. **Functionality**: Does it work as intended?
3. **Testing**: Adequate test coverage
4. **Documentation**: Updated documentation
5. **Performance**: No performance regressions
6. **Security**: No security vulnerabilities

### Review Timeline

- **Initial review**: Within 48 hours
- **Feedback**: Within 1 week
- **Final approval**: Within 2 weeks

### Addressing Feedback

1. **Read feedback carefully**: Understand what's being asked
2. **Ask questions**: If feedback is unclear, ask for clarification
3. **Make changes**: Implement requested changes
4. **Update tests**: Add tests if needed
5. **Respond to comments**: Acknowledge feedback and changes

## Recognition

Contributors will be recognized in:

- **CONTRIBUTORS.md**: List of all contributors
- **Release notes**: Mentioned in release notes
- **GitHub**: Listed as contributors on GitHub

## Getting Help

If you need help:

1. **Check documentation**: Review existing documentation
2. **Search issues**: Look for similar issues or discussions
3. **Ask questions**: Open a discussion or issue
4. **Join community**: Participate in community discussions

## License

By contributing to PhishShield, you agree that your contributions will be licensed under the same license as the project.

## Thank You

Thank you for contributing to PhishShield! Your contributions help make the project better for everyone.

---

*Last updated: September 2024*
*Contributing Guide version: 1.0.0*
