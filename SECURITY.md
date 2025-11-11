# Security Policy

## 🎮 Project Context

AntiPattern Bird is a **single-player desktop game** with no network connectivity, 
no data collection, and no user authentication. Security risks are minimal, but we 
still follow best practices.

## 📦 Supported Versions

| Version | Supported          | Notes |
| ------- | ------------------ | ----- |
| Latest release | :white_check_mark: | Always recommended |
| Older releases | :x: | Security fixes only in latest |
| Development branch | :warning: | Use at your own risk |

**Recommendation:** Always use the [latest release](https://github.com/dvdred/antipattern-bird/releases/latest).

## 🛡️ Security Considerations

### What This Game Does
- ✅ Runs **locally** on your machine (no internet required)
- ✅ Reads **only bundled assets** (images, sounds, fonts)
- ✅ **No data collection** or telemetry
- ✅ **No external dependencies** at runtime (only Pygame)

### What This Game Does NOT Do
- ❌ No network connections
- ❌ No file system writes (except optional high score in future versions)
- ❌ No execution of external code
- ❌ No personal data handling

### Dependencies
The game uses **Pygame** as its only runtime dependency. We rely on:
- [Pygame Security Policy](https://github.com/pygame/pygame/security/policy)
- Regular dependency updates via Dependabot

## 🐛 Reporting a Vulnerability

If you discover a security issue, please report it responsibly:

### For Critical Issues (RCE, arbitrary code execution, etc.)
📧 **Email:** dvdred@gmail.com  
⏱️ **Response time:** Within 48 hours  
🔒 **Please include:**
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### For Non-Critical Issues (crashes, resource leaks, etc.)
Open a [GitHub Issue](https://github.com/dvdred/antipattern-bird/issues) with the 
`security` label.

## 🔐 Security Best Practices for Users

When downloading and running this game:

1. **Download from official sources only:**
   - ✅ [GitHub Releases](https://github.com/dvdred/antipattern-bird/releases)
   - ✅ Clone from official repo
   - ❌ Avoid third-party mirrors

2. **Verify integrity (optional):**
   ```bash
   # Check SHA256 hash of downloaded file (provided in release notes)
   sha256sum antipattern-bird.exe