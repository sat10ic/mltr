# Security Policy

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x (alpha)  | :white_check_mark: |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **security@yourdomain.com** (replace with your actual security contact)

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information in your report:

* Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
* Full paths of source file(s) related to the manifestation of the issue
* The location of the affected source code (tag/branch/commit or direct URL)
* Any special configuration required to reproduce the issue
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including how an attacker might exploit it

This information will help us triage your report more quickly.

## Security Considerations for Trading Systems

### Critical Areas

This is a trading system that handles:
- **Financial data** - Market prices, positions, P&L
- **API credentials** - Exchange APIs, data providers
- **Trading signals** - Buy/sell recommendations

### Specific Concerns

**1. Data Integrity**
- ⚠️ **Time-series leakage**: Using future data in predictions
- ⚠️ **Data poisoning**: Malicious data affecting models
- ⚠️ **Calculation errors**: Bugs in indicators/returns

**2. Credential Security**
- ⚠️ **API keys in code**: Never commit secrets to Git
- ⚠️ **Weak permissions**: Restrict trading API access
- ⚠️ **Key rotation**: Rotate credentials regularly

**3. Model Security**
- ⚠️ **Model theft**: Protect trained models from unauthorized access
- ⚠️ **Adversarial inputs**: Validate all input data
- ⚠️ **Backdoors**: Review all external code/models

**4. System Access**
- ⚠️ **Unauthorized trading**: Authentication required for signal execution
- ⚠️ **Privilege escalation**: Least privilege principle
- ⚠️ **Audit logging**: Track all trading decisions

### Safe Usage Guidelines

**Before deploying:**

1. ✅ **Never use on live trading** without extensive testing
2. ✅ **Start with paper trading** (simulated) for at least 3 months
3. ✅ **Implement kill switches** for runaway losses
4. ✅ **Use API keys with READ-ONLY access** during development
5. ✅ **Enable 2FA** on all trading accounts
6. ✅ **Monitor for anomalies** continuously
7. ✅ **Have a rollback plan** ready

**Secure configuration:**

```yaml
# Good - Use environment variables
api_key: ${EXCHANGE_API_KEY}

# Bad - Never hardcode
api_key: "sk_live_abc123..."
```

### Known Limitations

**Alpha Release (v0.1.x):**

- ⚠️ No built-in authentication for API endpoints (add your own)
- ⚠️ No encryption at rest for stored credentials (use OS keyring)
- ⚠️ LLM prompts not sanitized for injection attacks
- ⚠️ No rate limiting on API endpoints
- ⚠️ Secrets detection is best-effort (not guaranteed)

**Planned for v1.0:**

- 🔒 Built-in API authentication (JWT)
- 🔒 Encrypted credential storage
- 🔒 Prompt injection prevention
- 🔒 Rate limiting and DDoS protection
- 🔒 Comprehensive security audit

### Security Checklist

Before using in any production-adjacent environment:

- [ ] All API keys stored in environment variables, not code
- [ ] `.env` file in `.gitignore`
- [ ] Pre-commit hooks running (`detect-secrets`)
- [ ] CI/CD security scans passing (Bandit, Safety)
- [ ] Review all external dependencies for CVEs
- [ ] Trading APIs use READ-ONLY keys during development
- [ ] Database credentials rotated and strong
- [ ] System monitoring and alerting configured
- [ ] Backup and disaster recovery plan tested
- [ ] Legal review completed (if required)

### Disclosure Policy

We will:

1. Confirm receipt of your vulnerability report within 48 hours
2. Provide an estimated timeline for a fix within 7 days
3. Notify you when the vulnerability is fixed
4. Credit you in our security advisory (if you wish)

We ask that you:

1. Give us reasonable time to fix the issue before public disclosure
2. Make a good faith effort to avoid privacy violations, data destruction, and interruption or degradation of services
3. Do not access or modify other users' data without explicit permission

### Security Updates

Security updates will be released as:

- **Critical**: Immediate patch release + advisory
- **High**: Patch within 7 days
- **Medium**: Patch in next minor release
- **Low**: Patch in next major release

Subscribe to security advisories:
- Watch this repository for security updates
- Enable GitHub security alerts for dependencies

### Responsible Use

⚠️ **IMPORTANT DISCLAIMER**:

This software is provided for **educational and research purposes only**.

- This is NOT financial advice
- Past performance does not guarantee future results
- Trading involves risk of substantial financial loss
- Use at your own risk

**You are responsible for:**

- Complying with all applicable laws and regulations (SEBI, etc.)
- Securing your own systems and credentials
- Testing thoroughly before any real trading
- Understanding the risks of algorithmic trading

### Attribution

This security policy is based on best practices from:
- [OpenSSF Scorecard](https://github.com/ossf/scorecard)
- [GitHub Security Advisories](https://docs.github.com/en/code-security/security-advisories)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

### Contact

**Security issues**: security@yourdomain.com
**General questions**: Open a GitHub Discussion
**Bug reports**: Open a GitHub Issue (non-security only)

---

Last updated: 2025-11-03
