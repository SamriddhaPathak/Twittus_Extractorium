# Contributing to Twitter/X Web Scraper

Thank you for your interest in contributing to this project! We welcome contributions from the community and appreciate your efforts to improve this tool.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background or identity.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Trolling, insulting, or derogatory comments
- Personal or political attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**How to Submit a Bug Report:**

1. Use a clear and descriptive title
2. Describe the exact steps to reproduce the problem
3. Provide specific examples to demonstrate the steps
4. Describe the behavior you observed and what you expected
5. Include screenshots if applicable
6. Provide your environment details:
   - Python version
   - Playwright version
   - Operating System
   - Browser version

**Bug Report Template:**

```markdown
**Description:**
A clear description of the bug.

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What you expected to happen.

**Actual Behavior:**
What actually happened.

**Environment:**
- Python version: 
- Playwright version: 
- OS: 
- Browser: 

**Screenshots/Logs:**
If applicable, add screenshots or log output.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**How to Submit an Enhancement:**

1. Use a clear and descriptive title
2. Provide a detailed description of the proposed feature
3. Explain why this enhancement would be useful
4. List any alternative solutions you've considered
5. Include mockups or examples if applicable

**Enhancement Template:**

```markdown
**Feature Description:**
Clear description of the proposed feature.

**Use Case:**
Why is this feature needed? What problem does it solve?

**Proposed Solution:**
How should this feature work?

**Alternatives Considered:**
What other approaches have you thought about?

**Additional Context:**
Any other relevant information.
```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- GitHub account

### Setup Steps

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/twitter-scraper.git
   cd twitter-scraper
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/twitter-scraper.git
   ```

4. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

6. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line Length**: Maximum 100 characters (not 79)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes for strings (except when single quotes avoid escaping)

### Code Quality

**Use Type Hints:**
```python
def scrape_profile(self, username: str, max_scrolls: int = 5) -> List[Dict]:
    """Scrape tweets from a profile."""
    pass
```

**Write Docstrings:**
```python
def parse_tweet(self, article_element, source_type: str, source_query: str) -> Optional[Dict]:
    """
    Parse tweet data from article element.
    
    Args:
        article_element: Playwright element containing tweet
        source_type: 'profile' or 'search'
        source_query: Username or search term
        
    Returns:
        Dictionary with tweet data or None if parsing fails
        
    Raises:
        Exception: If critical parsing error occurs
    """
    pass
```

**Handle Errors Properly:**
```python
try:
    # Risky operation
    result = some_function()
except SpecificException as e:
    logger.error(f"Specific error occurred: {e}")
    # Handle appropriately
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    import traceback
    logger.debug(traceback.format_exc())
```

**Use Meaningful Variable Names:**
```python
# Good
tweet_count = len(tweets)
author_username = extract_username(url)

# Bad
tc = len(tweets)
x = extract_username(url)
```

### Logging

Use appropriate logging levels:

```python
logger.debug("Detailed debugging information")
logger.info("General informational messages")
logger.warning("Warning messages for unusual events")
logger.error("Error messages for failures")
```

### Testing

Before submitting a pull request:

1. **Test your changes manually**
   - Run the scraper with your modifications
   - Test edge cases
   - Verify no regressions

2. **Check for common issues**
   - No syntax errors
   - No import errors
   - Functions work as expected

3. **Verify database integrity**
   ```python
   # Check for duplicates
   SELECT tweet_id, COUNT(*) FROM tweets 
   GROUP BY tweet_id HAVING COUNT(*) > 1;
   ```

## Pull Request Process

### Before Submitting

1. **Update from upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test thoroughly**
   - Manual testing of all changes
   - Verify no breaking changes
   - Check database operations

3. **Update documentation**
   - Update README.md if needed
   - Add comments to complex code
   - Update CHANGELOG.md

4. **Clean commit history**
   ```bash
   # Squash commits if needed
   git rebase -i HEAD~N
   ```

### Submitting the Pull Request

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create pull request on GitHub**
   - Use a clear, descriptive title
   - Fill out the PR template completely
   - Reference any related issues

3. **PR Description Template**
   ```markdown
   ## Description
   Brief description of changes.
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   Describe how you tested your changes.
   
   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Comments added to complex code
   - [ ] Documentation updated
   - [ ] No new warnings generated
   - [ ] Manual testing completed
   
   ## Related Issues
   Fixes #(issue number)
   ```

### Review Process

1. **Automated checks** (if configured)
   - Linting passes
   - Tests pass
   - No merge conflicts

2. **Code review**
   - Maintainer will review your code
   - Address feedback promptly
   - Make requested changes

3. **Approval and merge**
   - Once approved, maintainer will merge
   - Delete your feature branch after merge

## Specific Contribution Areas

### High Priority

- **Error handling improvements**: Better exception handling and recovery
- **Performance optimization**: Faster scraping without violating rate limits
- **Documentation**: Tutorials, examples, troubleshooting guides
- **Testing**: Unit tests, integration tests

### Medium Priority

- **Additional scraping features**: New data extraction capabilities
- **Export formats**: Support for more data export formats
- **Configuration options**: More customizable behavior
- **Logging enhancements**: Better debugging information

### Low Priority

- **UI improvements**: Better console output formatting
- **Code refactoring**: Cleaner, more maintainable code
- **Additional examples**: More use case demonstrations

## Questions?

If you have questions about contributing:

1. Check existing issues and pull requests
2. Review documentation thoroughly
3. Create a discussion or issue for clarification
4. Reach out to maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Acknowledged in documentation

Thank you for contributing to this project!

---

**Last Updated**: February 2026
