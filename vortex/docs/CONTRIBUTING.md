# Contributing to Vortex

Thank you for your interest in contributing to the Vortex of Enlightenment project. This document outlines the process for contributing and our development standards.

## Getting Started

1. Fork the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Development Standards

### Code Style
- Follow PEP 8 guidelines
- Use Black for formatting (line length: 88)
- Add type hints to all functions
- Use Google-style docstrings

### Testing
- Write tests for all new features
- Maintain or improve test coverage
- Run tests locally before submitting:
  ```bash
  pytest
  ```

### Documentation
- Update relevant documentation
- Add docstrings to new functions/classes
- Include code examples where appropriate
- Follow the documentation standards in `documentation_plan.md`

## Submitting Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes:
   - Write clear commit messages
   - Keep commits focused and atomic
   - Reference issues in commit messages

3. Run quality checks:
   ```bash
   # Format code
   black .
   
   # Run linters
   pylint vortex
   mypy vortex
   flake8 vortex
   
   # Run tests
   pytest
   ```

4. Submit a Pull Request:
   - Describe the changes
   - Link related issues
   - Update documentation
   - Add tests if needed

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Add to CHANGELOG.md
4. Get review from maintainers
5. Address review feedback
6. Maintain clean commit history

## Code Review

### What we look for:
- Code quality and style
- Test coverage
- Documentation
- Performance implications
- Security considerations

### Review Process
1. Automated checks must pass
2. At least one maintainer review
3. Documentation review if needed
4. Security review for sensitive changes

## Community

- Be respectful and inclusive
- Follow our Code of Conduct
- Help others when possible
- Share knowledge and document solutions

## Questions?

- Check existing documentation
- Search closed issues
- Ask in discussions
- Contact maintainers

Thank you for contributing to Vortex! 🌀✨ 