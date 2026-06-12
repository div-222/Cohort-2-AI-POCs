# IT SOP: Password Reset Procedure
**Document Type:** IT Standard Operating Procedure  
**Category:** Access Management  
**SOP ID:** IT-SOP-001  
**Version:** 2.3  
**Effective Date:** January 1, 2026  
**Owner:** IT Department  

---

## 1. Overview

This SOP outlines the procedures for resetting passwords for all company systems. It covers self-service resets as well as IT-assisted resets for cases where the self-service option is unavailable.

---

## 2. Systems Covered

| System | Self-Service Reset Available | IT-Assisted Reset |
|--------|------------------------------|-------------------|
| Corporate Email (Outlook / Microsoft 365) | Yes | Yes |
| Windows Laptop / Desktop Login | Yes (via SSPR) | Yes |
| VPN (Cisco AnyConnect) | No | Yes |
| HR Portal | Yes | Yes |
| JIRA / Confluence | Yes | Yes |
| GitHub / GitLab | Yes | No (contact IT) |
| ServiceNow | Yes | Yes |

---

## 3. Self-Service Password Reset (SSPR)

### 3.1 Microsoft 365 / Corporate Email Password Reset

Use this method if you can still access your registered mobile number or backup email.

```
Step 1: Go to https://passwordreset.microsoftonline.com
Step 2: Enter your corporate email address (user@company.com)
Step 3: Complete the CAPTCHA verification
Step 4: Choose verification method:
         - Text/SMS to registered mobile
         - Authenticator App notification
         - Backup email OTP
Step 5: Enter the OTP / approve the notification
Step 6: Enter your new password
         - Minimum 12 characters
         - Must include: UPPERCASE, lowercase, number, special character (!@#$%)
         - Cannot reuse last 10 passwords
Step 7: Click "Finish" — password reset successful
Step 8: Log in to Outlook and all connected Microsoft 365 services with the new password
```

> **Note:** Your Windows laptop login and most Microsoft-connected apps will automatically update to the new password.

---

### 3.2 Windows Laptop Login — Self-Service (On-Network)

If you are connected to the office Wi-Fi or VPN and your account is locked:

```
Step 1: On the Windows login screen, click "I forgot my PIN" or press Ctrl+Alt+Del
Step 2: Select "Reset Password"
Step 3: Verify identity via Microsoft Authenticator app
Step 4: Set a new password following the complexity requirements
Step 5: Log in with the new password
```

---

### 3.3 HR Portal Password Reset

```
Step 1: Go to portal.company.com
Step 2: Click "Forgot Password?"
Step 3: Enter your Employee ID
Step 4: OTP sent to your registered mobile number
Step 5: Enter OTP → Set new password
Step 6: Log in with the new password
```

---

## 4. IT-Assisted Password Reset

Use this process when:
- Self-service reset is not working
- Your mobile number is no longer accessible
- Your account is locked after multiple failed attempts
- You are locked out of your laptop offline

### 4.1 Raise an IT Help Desk Ticket

```
Method 1 — Helpdesk Portal (if you have access):
  1. Go to helpdesk.company.com
  2. Login → New Ticket → Category: "Access & Password"
  3. Sub-category: "Password Reset"
  4. Describe the issue and the system affected
  5. Submit → Ticket number assigned

Method 2 — Phone (for urgent / lockout cases):
  Call IT Help Desk: Ext. 1100 (or +91-80-XXXX-1100 from mobile)
  Working hours: Mon–Fri, 8 AM – 8 PM IST
  After-hours: Ext. 1199 (on-call support)

Method 3 — Walk-in:
  IT Help Desk Counter — Floor 2
  Mon–Fri: 9 AM – 6 PM IST
```

### 4.2 Identity Verification (IT-Assisted Reset)

Before IT performs a password reset, the employee must complete identity verification:

| Verification Method | Details |
|--------------------|---------|
| Employee ID badge | Physical ID badge shown at IT counter |
| Manager verification | Manager confirms identity via IT ticket / email |
| Video call verification | For remote employees (via Microsoft Teams) |

> **Security Notice:** IT will never ask for your current password. Do not share passwords over email, phone, or Slack.

---

## 5. VPN Password Reset

VPN credentials are tied to your Microsoft 365 / Active Directory credentials. Resetting your Microsoft 365 password will automatically update your VPN password.

```
After resetting your M365 password:
1. Open Cisco AnyConnect VPN client
2. Enter: vpn.company.com as the server address
3. Enter your updated corporate email and new password
4. Click Connect
```

If VPN still doesn't connect after the password reset, raise an IT helpdesk ticket with Category: "VPN Access Issues".

---

## 6. Password Best Practices

| Rule | Requirement |
|------|------------|
| Minimum Length | 12 characters |
| Complexity | Uppercase + lowercase + number + special character |
| Reuse | Cannot reuse last 10 passwords |
| Expiry | Password expires every 90 days (reminder sent at 14 days) |
| Sharing | Strictly prohibited — violation leads to disciplinary action |
| Storage | Use the approved password manager: **1Password** |

### Approved Password Manager

Employees are strongly encouraged to use **1Password** (company-licensed) to securely store and manage passwords.
- Access: `1password.com` (sign in with your corporate email via SSO)
- 1Password browser extension is pre-installed on company laptops.

---

## 7. SLA for Password Reset Tickets

| Priority | Scenario | Resolution Time |
|----------|----------|----------------|
| Critical | Executive locked out of all systems | 30 minutes |
| High | Employee completely locked out during business hours | 2 hours |
| Medium | Non-urgent password reset request | 4 hours |
| Low | Password reset for rarely used system | 8 hours |

---

## 8. FAQs

**Q: How do I reset my corporate email password?**  
A: Go to `https://passwordreset.microsoftonline.com` and follow the self-service steps. You'll need access to your registered mobile or backup email for OTP verification.

**Q: My laptop is locked and I can't connect to VPN. What do I do?**  
A: Call the IT Help Desk at Ext. 1100 or walk in to the IT counter on Floor 2. IT will verify your identity and unlock your account remotely or assist you on-site.

**Q: Does resetting my email password also reset my VPN password?**  
A: Yes. Your VPN credentials are linked to your Microsoft 365 account. Resetting your email password will update the VPN credentials as well.

**Q: How often do I need to change my password?**  
A: Passwords expire every 90 days. You will receive an email reminder 14 days before expiry.

**Q: Can I use the same password I used before?**  
A: No. The system prevents reuse of the last 10 passwords.

---

*For urgent password issues outside business hours, call the on-call IT support line: Ext. 1199.*
