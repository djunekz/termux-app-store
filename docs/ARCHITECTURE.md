# Architecture Overview

This document describes the internal architecture and design principles of  
**Termux App Store**.

---

## 🎯 Design Goals

Termux App Store is designed with the following goals:

- **Portable** — runnable from any directory
- **Self-healing** — survives folder moves or renames
- **Safe** — blocks unsupported packages
- **Source-based** — transparent build process
- **UI-first** — modern TUI using Textual
- **Binary-friendly** — supports frozen/binary builds

---

## 🧱 High-Level Architecture
```Text
┌──────────────────────────┐
│      User Interface      │ 
│   (Textual TUI Layer)    │ 
└─────────────┬────────────┘ 
┌─────────────▼────────────┐ 
│     Application Core     │ 
│  (State, Events, Logic)  │ 
└─────────────┬────────────┘  
┌─────────────▼────────────┐ 
│     Package Resolver     │ 
│   (build.sh inspection)  │ 
└─────────────┬────────────┘  
┌─────────────▼────────────┐ 
│     Build Executor       │ 
│  (build-package.sh hook) │ 
└─────────────┬────────────┘  
┌─────────────▼────────────┐ 
│     Termux Environment   │ 
│    (pkg / apt / shell)   │ 
└──────────────────────────┘
```

---

## 🧠 Core Components

### 1. UI Layer (Textual)

- Implemented using **Textual**
- Handles:
  - List rendering
  - Preview panel
  - Logs
  - Progress bar
  - User interaction (keyboard / touch)

**No business logic is embedded in UI rendering.**

---

### 2. Application Core

Responsible for:
- Application state
- Async task scheduling
- Worker queue
- Install locking
- UI updates from threads

Uses:
- `asyncio`
- `asyncio.Queue`
- `call_from_thread()` for UI safety

---

### 3. Path Resolver (Self-Healing)

The app never trusts:
- Current working directory
- Symlink location
- Invocation path

Instead it uses:

- `__file__` (source mode)
- `sys.executable` (binary mode)

This allows:
- Execution from anywhere
- Symlink support
- Folder relocation without breaking

---

### 4. Package Discovery Engine

Packages are discovered by:
- Scanning `packages/`
- Validating `build.sh`
- Extracting metadata:
  - Name
  - Version
  - Description
  - Dependencies

No external index or registry is required.

---

### 5. Package Validation Layer

Before build:
- `build.sh` is validated
- Unsupported dependencies are detected
- Packages can be marked:
  - INSTALLED
  - UPDATE
  - NEW
  - UNSUPPORTED

This prevents broken builds early.

---

### 6. Build Executor

All builds are executed via:
`build-package.sh`
Responsibilities:
- Architecture detection
- Dependency installation
- Source fetching
- Build & packaging
- `.deb` generation (if enabled)

The UI **never executes build logic directly**.

---

## 🔄 Data Flow

1. App starts
2. Root directory resolved
3. Packages scanned
4. UI list populated
5. User selects package
6. Validation performed
7. Build executed in background thread
8. Logs streamed live to UI
9. Status refreshed

---

## 🧵 Concurrency Model

- UI runs in the main event loop
- Builds run in background threads
- Thread → UI communication via:
  - `call_from_thread()`
- Only one install allowed at a time

This avoids:
- UI freezes
- Race conditions
- Corrupted state

---

## 📦 Binary Distribution Architecture

Binary builds:
- Bundle Python runtime
- Bundle Textual
- Freeze source code
- Run without system Python

Binary mode is detected via:
```python
getattr(sys, "frozen", False)
```
---

## 🔐 Security Considerations
- No root access required
- No system-level writes
- All shell execution is explicit
- No dynamic code execution
- No network calls from UI layer

---

## 🧪 Extensibility
Future extensions may include:
- Remote repositories
- Plugin system
- Package categories
- Search index
- Offline cache
Architecture is intentionally modular.

---

## 🚫 Non-Goals
This project intentionally does not:
- Replace `pkg`
- Act as a full Linux distro
- Support systemd
- Support desktop GUI frameworks

---

## 🧭 Summary
Termux App Store is:
- Modular
- Portable
- Safe
- Source-driven
- UI-focused
Designed for power users who want control without chaos.

*© Termux App Store* — **Architecture Documentation**
