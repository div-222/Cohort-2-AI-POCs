# IT Security Policy
**Document Type:** IT Policy  
**Category:** Information Security  
**Policy ID:** IT-POL-001  
**Version:** 3.0  
**Effective Date:** January 1, 2026  
**Owner:** IT Security Department  
**Compliance:** ISO 27001, SOC 2 Type II, GDPR  

---

## 1. Overview

This policy establishes the information security standards, acceptable use guidelines, and security responsibilities for all employees, contractors, and third-party vendors who access company systems, networks, and data.

Non-compliance with this policy may result in disciplinary action, including termination and legal proceedings in cases of gross violations.

---

## 2. Scope

This policy applies to:
- All full-time and part-time employees
- Contractors and temporary staff
- Third-party vendors with system access
- All company-owned and personal devices used for company work
- All company data regardless of where it is stored

---

## 3. Information Classification

All company information must be classified into one of the following categories:

| Classification | Definition | Examples |
|--------------|-----------|---------|
| **Confidential** | Highly sensitive data — restricted access | Employee PII, payroll, M&A data, customer contracts |
| **Internal** | Internal business use only | Internal policies, project plans, employee handbooks |
| **Public** | Information approved for public release | Press releases, website content, job postings |

> By default, treat all company information as **Internal** unless explicitly classified otherwise.

---

## 4. Acceptable Use Policy

### 4.1 Company Devices

**Permitted Use:**
- All work-related tasks and official business activities
- Reasonable personal use during non-working hours (browsing, personal email — not excessive)

**Prohibited Use:**
- Installing unauthorized software (refer to Software Installation SOP)
- Storing personal media files (movies, music) on company storage
- Using company devices for personal business ventures
- Accessing or sharing illegal, offensive, or discriminatory content
- Cryptocurrency mining or any activity that consumes abnormal system resources
- Conducting hacking, penetration testing, or network scanning without written IT authorization
- Attempting to bypass security controls, firewalls, or monitoring systems

### 4.2 Internet Use

| Permitted | Prohibited |
|-----------|----------|
| Work-related research | Accessing adult or illegal content |
| Accessing company-approved SaaS tools | Downloading torrents / pirated software |
| Reasonable personal browsing | Streaming large volumes of personal media during work hours |
| Approved cloud services (OneDrive, SharePoint) | Uploading company data to personal cloud accounts |

### 4.3 Email Use

- Company email is for business communication.
- Do not auto-forward company emails to personal email accounts.
- Do not send confidential data over unencrypted email.
- Use encryption (S/MIME or Microsoft 365 Message Encryption) for sensitive data.
- Report phishing emails immediately to `phishing@company.com`.

---

## 5. Password Policy

| Requirement | Standard |
|------------|---------|
| Minimum length | 12 characters |
| Complexity | Must contain: uppercase, lowercase, number, special character |
| Expiry | Every 90 days |
| History | Cannot reuse last 10 passwords |
| Sharing | Strictly prohibited |
| Storage | Use company-approved password manager (1Password) |
| Default passwords | Must be changed immediately upon first login |

### Multi-Factor Authentication (MFA)

MFA is **mandatory** for:
- Corporate email (Microsoft 365)
- VPN access
- HR Portal
- All cloud services and SaaS applications
- Remote Desktop and admin tools

---

## 6. Device Security

### 6.1 Screen Lock

| Scenario | Requirement |
|---------|------------|
| Leaving desk temporarily | Lock screen immediately (`Windows+L` / `Cmd+Control+Q`) |
| Auto-lock timeout | Maximum 5 minutes of inactivity |
| Laptop in public | Never leave laptop unattended |

### 6.2 Encryption

- All company laptops must have **BitLocker** (Windows) or **FileVault** (macOS) encryption enabled.
- Encryption is auto-enabled on company devices. Do not disable it.
- External storage devices (USB drives) used for company data must be encrypted.

### 6.3 Antivirus & EDR

- **Microsoft Defender** is the standard endpoint security solution.
- Do not disable or modify antivirus settings.
- Endpoint Detection & Response (EDR) is deployed on all devices — security team monitors alerts.
- Report any antivirus alert or warning to IT Security immediately.

### 6.4 Software Updates

- All operating system and application updates must be applied within **7 days** of release.
- Critical security patches must be applied within **48 hours**.
- Company devices are managed via Microsoft Intune — patches are pushed automatically.

---

## 7. Network Security

### 7.1 Wi-Fi Usage

| Network | Policy |
|---------|-------|
| Office Wi-Fi (Corp-Net) | Fully secured — use for all work |
| Guest Wi-Fi (Guest-Net) | For visitors only — do not use for work |
| Public Wi-Fi (cafes, airports, hotels) | Use only with VPN connected |
| Personal mobile hotspot | Permitted for work — no restriction |

### 7.2 VPN

- VPN is mandatory when accessing company resources from outside the office.
- Always connect to VPN before accessing internal systems, file servers, or databases.
- Refer to the VPN Setup SOP (IT-SOP-002) for configuration instructions.

---

## 8. Data Security

### 8.1 Data Storage

| Data Type | Approved Storage |
|----------|----------------|
| Work documents and files | OneDrive for Business / SharePoint |
| Code / repositories | GitHub Enterprise (company account) |
| Database data | Company-approved cloud/on-prem databases |
| Emails and calendar | Microsoft 365 Exchange Online |

**Prohibited Storage:**
- Personal Dropbox, Google Drive, iCloud for company data
- USB drives (unless encrypted and IT-approved)
- Personal laptop hard drives

### 8.2 Data Sharing

- Do not share confidential data with external parties without manager approval.
- Use secure file-sharing links (SharePoint / OneDrive with expiry) for external sharing.
- NDAs must be signed before sharing confidential information with vendors.

### 8.3 Data Retention

| Data Category | Retention Period |
|--------------|----------------|
| Employee records | 7 years after departure |
| Financial records | 7 years |
| Project documents | 5 years after project closure |
| Email correspondence | 2 years (archived automatically) |
| Security logs | 1 year |

---

## 9. Incident Response

### What Constitutes a Security Incident?

- Unauthorized access to any company system or data
- Lost or stolen device (laptop, phone, access card)
- Malware or ransomware infection
- Phishing email clicked or credentials submitted
- Suspected data breach or data leak
- Unauthorized software installation
- Unusual system behavior

### Reporting a Security Incident

**Immediately report ALL security incidents:**

```
🚨 Priority 1 — Data Breach / Active Attack:
   → Call IT Security: Ext. 1200 (24/7)
   → Email: security-incident@company.com (auto-escalates to CISO)

🔔 Priority 2 — Lost Device / Suspicious Activity:
   → Email: security@company.com
   → Raise ticket: helpdesk.company.com → Security → Incident Report

📋 Priority 3 — Policy Violation / Minor Incident:
   → Raise ticket: helpdesk.company.com → Security → Policy Violation
```

> **Remember:** Reporting an incident quickly can prevent greater damage. There is no penalty for good-faith reporting. Concealing an incident is a policy violation.

---

## 10. Physical Security

- Never allow unauthorized individuals (including family/friends) to use your company device.
- Do not remove confidential documents from the office without authorization.
- Shred sensitive printed documents — use the cross-cut shredders available on each floor.
- Visitor badges must be surrendered at the reception on departure.
- If you see a suspicious person or unattended bag on company premises, notify security immediately: Ext. 1000.
- Clean desk policy: Lock away sensitive materials and clear your desk at end of day.

---

## 11. Bring Your Own Device (BYOD)

- Personal devices may only be used for Microsoft Outlook mobile, Teams, and Authenticator.
- BYOD devices must be enrolled in Microsoft Intune (company MDM).
- Company data must not be stored locally on personal devices.
- IT has the right to wipe company data from enrolled personal devices upon resignation/termination.

---

## 12. Third-Party & Vendor Access

- All vendor access to company systems must be pre-approved by IT Security and the relevant business owner.
- Vendor access must be time-limited and reviewed quarterly.
- All vendors must sign the company's Third-Party Security Agreement before access is granted.
- Vendor access must use multi-factor authentication.

---

## 13. Compliance & Audits

- The IT Security team conducts **quarterly security audits** on user accounts, device compliance, and access rights.
- Employees may be required to demonstrate policy compliance during audits.
- Penetration tests are conducted annually by an external security firm.
- Non-compliant devices are automatically quarantined via Microsoft Intune.

---

## 14. Violations & Consequences

| Severity | Examples | Consequence |
|---------|---------|------------|
| Minor | First-time policy oversight, non-malicious | Formal warning + retraining |
| Moderate | Repeat violation, data mishandling | Written warning + access restriction |
| Major | Intentional policy violation, unauthorized access | Suspension / Termination |
| Critical | Data breach, corporate espionage | Termination + Legal action |

---

## 15. FAQs

**Q: Can I use my personal USB drive on my company laptop?**  
A: Only IT-approved, encrypted USB drives are permitted. Personal USB drives that are not encrypted may be auto-blocked by the endpoint security solution. Request an approved USB drive from IT if needed.

**Q: I received a suspicious email. What should I do?**  
A: Do not click any links or open attachments. Forward the email to `phishing@company.com` and delete it. If you accidentally clicked, immediately disconnect from the network and call IT Security at Ext. 1200.

**Q: My laptop was stolen. What's the first thing I should do?**  
A: Call IT Security at Ext. 1200 immediately so they can remotely wipe the device and revoke access tokens. Then file a police complaint within 24 hours.

**Q: Can I install a VPN app (like NordVPN) on my company laptop?**  
A: No. Third-party VPN software is prohibited on company devices. Use only the company-approved Cisco AnyConnect VPN.

**Q: How do I know if a file or email is classified as Confidential?**  
A: Confidential documents are typically labeled in the header/footer. When in doubt, treat all company data as Internal. Contact your manager or IT Security if unsure.

---

*For security concerns, contact IT Security at security@company.com or Ext. 1200.*  
*For urgent incidents (active threat, data breach), call 24/7 hotline: Ext. 1200.*
