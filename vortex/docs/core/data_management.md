# Data Management

## Overview

This document outlines the data structure, storage systems, and management practices for the Vortex of Enlightenment project.

## Data Structure

### Directory Layout
```
data/
├── profiles/          # User profile data
│   ├── active/       # Active user profiles
│   └── archived/     # Archived profiles
├── mythology/        # Mythological system data
│   ├── sefirot/      # Kabbalistic data
│   ├── ogdoad/       # Egyptian system
│   ├── dogon/        # Dogon cosmology
│   └── mayan/        # Mayan calendar system
├── content/          # Game content
│   ├── challenges/   # Challenge templates
│   ├── dialogs/      # Guide interactions
│   └── scenarios/    # Scripted scenarios
└── system/          # System configuration
    ├── config/      # Configuration files
    ├── logs/        # System logs
    └── cache/       # Cache data
```

## Data Models

### Profile Data
```python
class UserProfile:
    """User profile data structure"""
    id: str
    behavioral_matrix: Dict[str, float]
    progress: Dict[str, Any]
    achievements: List[str]
    current_path: str
```

### Mythology Data
```python
class MythologyMapping:
    """Cross-cultural mythology mappings"""
    source_system: str
    target_system: str
    correspondences: Dict[str, str]
    symbols: Dict[str, List[str]]
```

### Content Data
```python
class Challenge:
    """Challenge template structure"""
    id: str
    type: str
    difficulty: float
    requirements: Dict[str, Any]
    content: Dict[str, Any]
```

## Storage Systems

### Database Schema
- SQLAlchemy ORM for relational data
- Redis for caching and session data
- File system for static content
- Alembic for migrations

### Backup System
- Daily automated backups
- Version control for content
- Incremental profile backups
- Disaster recovery plans

## Data Management

### Profile Management
- Regular profile updates
- Progress tracking
- Achievement monitoring
- Path optimization

### Content Management
- Version control
- Content validation
- Localization support
- Dynamic generation

### System Data
- Configuration management
- Log rotation
- Cache invalidation
- Performance metrics

## Security

### Data Protection
- Encryption at rest
- Secure transmission
- Access control
- Privacy compliance

### Backup Security
- Encrypted backups
- Secure storage
- Access logging
- Recovery testing

## Maintenance

### Regular Tasks
- Data cleanup
- Index optimization
- Cache management
- Log analysis

### Monitoring
- Storage usage
- Access patterns
- Error rates
- Performance metrics

## Development Guidelines

### Data Access
```python
# Example data access pattern
async def get_user_profile(user_id: str) -> UserProfile:
    """Retrieve user profile with caching"""
    cache_key = f"profile:{user_id}"
    
    # Check cache first
    if cached := await cache.get(cache_key):
        return UserProfile.from_dict(cached)
    
    # Fallback to database
    profile = await db.profiles.get(user_id)
    await cache.set(cache_key, profile.to_dict())
    return profile
```

### Best Practices
- Use type hints
- Document data structures
- Implement caching
- Handle errors gracefully

## Migration Procedures

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### Content Updates
- Version control
- Backward compatibility
- Update validation
- Rollback procedures

## Troubleshooting

### Common Issues
1. Cache inconsistency
2. Database connection issues
3. Storage capacity problems
4. Backup failures

### Resolution Steps
- Clear cache
- Reconnect database
- Cleanup old data
- Verify backups 