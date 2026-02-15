# Security Policy

## Supported Versions

This project is actively maintained. Security updates are provided for:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please follow these steps:

### How to Report

1. **Do NOT open a public issue** for security vulnerabilities
2. **Email**: Open an issue with title "Security Concern" (without details)
3. **Or**: Use GitHub's private vulnerability reporting feature
4. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Response Time**: Within 48 hours
- **Updates**: You'll receive updates every 3-5 days
- **Fix Timeline**: Critical issues fixed within 7 days
- **Disclosure**: Coordinated disclosure after fix is released

### Security Considerations

This project:
- ✅ Does NOT connect to the internet
- ✅ Does NOT store user data
- ✅ Runs locally on your machine
- ✅ Uses safe `eval()` with restricted namespace for equations
- ✅ Only accesses local files you explicitly save/load

**Risk Level: Low** - This is a local GUI application with no network access.

## Safe Usage

- Only run code from official repository
- Don't execute untrusted `.py` files
- Review equation inputs if sharing with others
- Keep Python and dependencies updated

## Questions?

Open an issue for general security questions (non-sensitive).
