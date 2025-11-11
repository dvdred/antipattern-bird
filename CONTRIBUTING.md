# Contributing to AntiPattern Bird Epic Game

Thank you for your interest in contributing to AntiPattern Bird Epic Game! 🎮

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Coding Guidelines](#coding-guidelines)
- [Pull Request Process](#pull-request-process)
- [Adding New Features](#adding-new-features)

## Code of Conduct

This project follows a simple code of conduct:
- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs 🐛

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Description**: Clear description of the problem
- **Steps to reproduce**: Step-by-step instructions
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **System info**: OS, Python version, Pygame version
- **Screenshots**: If applicable

### Suggesting Enhancements 💡

Enhancement suggestions are tracked as GitHub issues. When suggesting:

- Use a clear and descriptive title
- Provide detailed description of the suggested enhancement
- Explain why this would be useful
- Include mockups/examples if applicable

### Contributing Code 💻

1. **Bug fixes**: Always welcome!
2. **New pipe types**: Follow the existing pattern (see [Adding New Pipes](#adding-new-pipe-types))
3. **New features**: Open an issue first to discuss
4. **Performance improvements**: Include benchmarks
5. **Documentation**: Always appreciated

## Development Setup

### Prerequisites

```bash
Python 3.8+
pygame >= 2.0.0
```

### Installation

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/antipattern-bird.git
cd antipattern-bird
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Verify installation:
```bash
python app.py
```

## Running Tests

```bash
python -m unittest test_app.py
```

### Test Coverage

When adding new features, please include tests:
- Unit tests for new classes
- Integration tests for game mechanics
- Ensure all tests pass before submitting PR

## Coding Guidelines

### Python Style

- Follow **PEP 8** style guide
- Use **4 spaces** for indentation (no tabs)
- Maximum line length: **120 characters** (flexible for readability)
- Use descriptive variable names

### Code Structure

```python
# Good
class NewPipe(Pipe):
    def __init__(self, x, base_gap=180):
        super().__init__(x, text="", gap=base_gap)
        self.color = (R, G, B)
        self.is_new_type = True
        
# Bad
class NewPipe(Pipe):
    def __init__(self,x,gap=180):
        super().__init__(x,"",gap)
        self.col=(R,G,B)
```

### Constants

- Place all constants at the **top of the file**
- Use **UPPER_CASE** for constants
- Group related constants together with comments

```python
# ---------- NEW PIPE CONFIG ----------
NEW_MIN_MS = 60_000
NEW_MAX_MS = 90_000
NEW_POINTS = 5
NEW_COLOR = (255, 128, 0)
```

### Comments

- Use comments for **why**, not **what**
- Document complex algorithms
- Keep comments up-to-date

## Pull Request Process

### Before Submitting

- [ ] Code follows the style guidelines
- [ ] Self-review of your code
- [ ] Comments added for complex code
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Documentation updated (if needed)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe tests performed

## Screenshots (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex areas
- [ ] Updated documentation
- [ ] Added tests
- [ ] All tests pass
```

### Review Process

1. Maintainers will review within **7 days**
2. Address review comments
3. Once approved, maintainer will merge
4. Your contribution will be credited in releases

## Adding New Features

### Adding New Pipe Types

Follow this pattern:

```python
# 1. Define constants
NEW_PIPE_MIN_MS = 60_000
NEW_PIPE_POINTS = 5
NEW_PIPE_COLOR = (R, G, B)

# 2. Create class inheriting from Pipe
class NewPipe(Pipe):
    def __init__(self, x, base_gap=180):
        super().__init__(x, text="", gap=base_gap)
        self.color = NEW_PIPE_COLOR
        self.is_new_type = True
        self.passed = False
        
    def draw(self, surf, alpha=255):
        # Custom drawing logic
        pass

# 3. Add spawn logic in main() game loop
# 4. Add collision/scoring logic
# 5. Add tests in test_app.py
# 6. Add sound effect (optional)
# 7. Update documentation
```

### Adding Sounds

1. Place sound file in project root
2. Format: **WAV**, **22050 Hz**, **16-bit**, **stereo**
3. Add to `get_resource_path()` section:

```python
new_sound = get_resource_path('new_sound.wav')
S_NEW = pygame.mixer.Sound(new_sound)
S_NEW.set_volume(0.5)
```

### Adding Visual Effects

- Keep effects **lightweight** (60 FPS target)
- Use **alpha blending** for transparency
- Test on different screen sizes

## Project Structure

```
antipattern-bird/
├── app.py              # Main game file
├── test_app.py         # Unit tests
├── CONTRIBUTING.md     # This file
├── README.md           # Project readme
├── LICENSE             # GPL3 license
└── assets/             # Resources (sounds, fonts, images)
```

## Resources Needed

When adding features requiring resources:

### Images
- Format: PNG with transparency
- Icon: 32x32px

### Sounds
- Format: WAV
- Sample rate: 22050 Hz
- Bit depth: 16-bit
- Channels: Stereo

### Fonts
- Include license information
- Prefer open-source fonts

## Questions?

- Open an issue with the **question** label
- Contact: dvdred@gmail.com

## License

By contributing, you agree that your contributions will be licensed under the **GPL3 License**.

---

**Thank you for contributing! 🚀**

Made with Lulz by the AntiPattern Bird community