# Contributing to android-gradle-skills

Thank you for your interest in contributing! This document outlines the guidelines for contributing new Gradle knowledge, examples, or scripts to this repository.

## How to Contribute

### 1. Adding New Gradle Knowledge

Add markdown files to `android-gradle/references/` following the naming convention:
- `build-basics.md` - Gradle fundamentals
- `dependency-management.md` - Version catalogs and dependency handling
- `build-variants.md` - Build types, product flavors
- `signing-and-release.md` - Signing配置
- `performance-optimization.md` - Build速度优化
- `troubleshooting.md` - Common errors and solutions
- `ci-cd-integration.md` - CI/CD integration examples

### 2. Adding Example Projects

Place example projects in `examples/` directory with:
- `README.md` explaining how to run and key points
- Minimal but complete project structure
- Comments in build files explaining the configuration

Example structure:
```
examples/
└── my-example/
    ├── README.md
    ├── build.gradle.kts
    ├── settings.gradle.kts
    ├── gradle.properties
    └── app/
        └── ...
```

### 3. Adding Scripts

Scripts should be:
- Well-documented with usage examples
- Cross-platform compatible (Unix/Windows)
- Follow existing naming conventions

## Guidelines

- All documentation should be clear and practical
- Code examples must be tested and working
- Avoid hardcoded paths - use environment variables or placeholders
- Keep files organized by category/function

## Submitting Changes

1. Fork the repository
2. Create a new branch for your changes
3. Make your changes with clear commit messages
4. Submit a pull request with description

## Questions?

Open an issue for discussion before making significant changes.