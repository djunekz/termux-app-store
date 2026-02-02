# Binary Disclaimer

This project provides **prebuilt binaries** for convenience.

By downloading or executing the binary, you acknowledge and agree to the following terms.

---

## ⚠️ No Warranty

The binary is provided **"AS IS"**, without warranty of any kind, express or implied.

The author makes **no guarantees** regarding:
- Stability
- Performance
- Compatibility
- Security

Use at your own risk.

---

## 🧠 Transparency & Trust

This project is **open-source**.

- Source code is publicly available
- Binary releases are built **from the same source**
- No telemetry, tracking, or hidden network behavior is intentionally included

If you do not trust the binary, **build it yourself from source**.

---

## 🧪 Environment-Specific Behavior

The binary is designed for:
- **Termux**
- Linux-based userland
- ARM / AArch64 / x86_64 architectures

Behavior may vary depending on:
- Device
- Architecture
- Termux version
- Installed system packages

---

## 🔐 Security Considerations

- The binary may execute shell commands (e.g. `build-package.sh`)
- It may install system packages via `pkg`
- It may write files under `$PREFIX`

You should **review permissions** and **understand the build process** before use.

---

## ❌ No Liability

In no event shall the author be liable for:
- Data loss
- System damage
- Security breaches
- Device instability
- Misuse of the application

---

## ✅ Recommended Usage

✔ Prefer the official GitHub Releases  
✔ Verify checksums when available  
✔ Run inside a trusted Termux environment  
✔ Do not run as root  

---

## 📌 Final Note

If you are unsure or uncomfortable running a precompiled binary,
**do not use it** and build from source instead.
