# Multi-Module Clean Architecture

Demonstrates layered architecture with Convention Plugins and Version Catalogs.

## Structure

```
multi-module-clean/
├── core/
│   ├── network/      # Network layer
│   └── ui/           # Shared UI components
├── feature/
│   └── home/         # Home feature module
├── app/              # Application module
└── build-logic/     # Convention plugins
```

## Module Dependencies

```
:app
  └── :feature:home
        └── :core:ui
              └── :core:network
```

## Key Features

- Convention Plugins for shared build logic
- Version Catalogs for centralized dependency management
- Clean separation between layers
- Build cache optimization with `implementation` vs `api`

## How to Run

```bash
./gradlew :app:assembleDebug
./gradlew :app:installDebug
```