# Vortex Documentation Style Guide

## General Principles

1. **Clarity First**: Write documentation that is clear, concise, and accessible to both technical and non-technical readers.
2. **Consistency**: Maintain consistent terminology, formatting, and structure across all documentation.
3. **Completeness**: Include all necessary information without redundancy.

## Document Structure

### File Headers
Every documentation file should begin with:
```markdown
# [Title in Title Case]

[Brief one-paragraph description]
```

### Section Headers
- Use H1 (#) for document titles
- Use H2 (##) for major sections
- Use H3 (###) for subsections
- Use H4 (####) for detailed points

## Formatting Standards

### Code Blocks
- Use triple backticks with language specification
```python
def example():
    pass
```

### File Paths and Code Elements
- Use single backticks for:
  - File names: `main.py`
  - Directory paths: `src/core/`
  - Class names: `Game`
  - Function names: `start()`
  - Variable names: `player`

### Lists
- Use hyphen (-) for unordered lists
- Use numbers (1.) for ordered lists
- Maintain consistent indentation (4 spaces)

## Content Guidelines

### Technical Terms
- Define technical terms on first use
- Maintain a consistent glossary across documents
- Use the same term throughout (avoid synonyms for technical concepts)

### Code Examples
- Keep examples concise and focused
- Include comments for complex operations
- Use meaningful variable and function names

### Version Information
- Clearly mark version-specific information
- Include Python version requirements
- List dependency versions when relevant

## Documentation Types

### README.md
- Project overview
- Installation instructions
- Basic usage examples
- Links to detailed documentation
- Requirements and dependencies

### API Documentation
- Function/method signatures
- Parameter descriptions
- Return value specifications
- Usage examples
- Error handling

### Tutorials
- Step-by-step instructions
- Clear prerequisites
- Expected outcomes
- Troubleshooting tips

## Terminology Standards

### Consistent Terms
- "Zone" (not "area" or "region")
- "Guide" (not "assistant" or "helper")
- "Player" (not "user" or "participant")
- "Token" (not "coin" or "point")

### Project-Specific Terms
- "Vortex" - The game environment
- "Pond" - A specific location within a zone
- "Stream" - Connection between ponds
- "Sefirot" - The mystical spheres
- "Ogdoad" - The Egyptian primordial forces

## Review Process

1. **Self-Review Checklist**
   - Spelling and grammar
   - Formatting consistency
   - Code block accuracy
   - Link validity
   - Terminology alignment

2. **Peer Review Guidelines**
   - Technical accuracy
   - Clarity and completeness
   - Adherence to style guide
   - Documentation usefulness

## Maintenance

- Review and update documentation with each release
- Maintain a changelog for documentation updates
- Archive outdated documentation appropriately
- Regular validation of examples and instructions 