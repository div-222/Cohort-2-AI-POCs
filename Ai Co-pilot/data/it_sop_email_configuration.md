# IT SOP: Email Configuration Guide (Outlook / Microsoft 365)
**Document Type:** IT Standard Operating Procedure  
**Category:** Communication & Collaboration  
**SOP ID:** IT-SOP-005  
**Version:** 1.4  
**Effective Date:** January 1, 2026  
**Owner:** IT Department  

---

## 1. Overview

This SOP provides instructions for configuring company email (Microsoft 365 / Outlook) on desktop, laptop, and mobile devices. It also covers common troubleshooting steps and best practices for secure email use.

**Email Domain:** `@company.com`  
**Email Service:** Microsoft 365 (Exchange Online)  
**Web Access (OWA):** `https://outlook.office.com`

---

## 2. Email Access Methods

| Method | Platform | Best For |
|--------|---------|---------|
| Outlook Desktop App | Windows / macOS | Primary work computer |
| Outlook Web App (OWA) | Browser (any OS) | Secondary/guest access |
| Outlook Mobile App | iOS / Android | Mobile access |
| Microsoft Teams (integrated) | All platforms | Team communication |

---

## 3. Setting Up Outlook on Desktop (Windows)

### 3.1 Outlook is Pre-Installed on Company Laptops

Company laptops have Outlook pre-installed and pre-configured. If you face issues:

```
1. Open Outlook from the Start Menu
2. It should auto-configure using your Windows login
3. If prompted, enter: yourname@company.com
4. Click "Connect" — Outlook will auto-detect the Microsoft 365 settings
5. Complete MFA verification if prompted
6. Click "Done" — your inbox will load
```

### 3.2 Manual Configuration (If Auto-Setup Fails)

```
1. Open Outlook → File → Add Account
2. Enter your corporate email: yourname@company.com
3. Click Connect
4. Select "Microsoft 365" as the account type
5. You will be redirected to the Microsoft login page
6. Enter your corporate email and password
7. Approve the MFA notification on your phone
8. Outlook will configure automatically
9. Click "Done"
```

---

## 4. Setting Up Outlook on macOS

```
1. Open Outlook (pre-installed on company Macs)
   OR download from: https://aka.ms/outlookmacdownload
2. Click "Add Account" (or File → Add Account)
3. Enter: yourname@company.com
4. Click "Continue"
5. You are redirected to Microsoft login — enter password
6. Approve MFA notification
7. Click "Done" — inbox loads
```

---

## 5. Setting Up Outlook on Mobile (iOS / Android)

### iOS Setup

```
1. Download "Microsoft Outlook" from the App Store
   (Publisher: Microsoft Corporation)
2. Open the app → "Add Account"
3. Enter: yourname@company.com → Tap "Continue"
4. Enter your Microsoft 365 password
5. Approve MFA notification
6. Optional: Enable Touch ID / Face ID for the app
7. Inbox synced ✅
```

### Android Setup

```
1. Download "Microsoft Outlook" from Google Play Store
   (Publisher: Microsoft Corporation)
2. Open app → "Add Account" → "Add Email Account"
3. Enter: yourname@company.com → Tap "Continue"
4. Enter your Microsoft 365 password
5. Approve MFA notification
6. Optional: Enable biometric unlock for the app
7. Inbox synced ✅
```

> **Security Note:** Company IT policy requires Outlook mobile to be enrolled in Microsoft Intune for compliance. You will be prompted to enroll during first login — accept and complete enrollment.

---

## 6. Outlook Web App (OWA)

Use OWA when you are on a non-company device or for quick browser-based access:

```
1. Open browser → Go to: https://outlook.office.com
2. Enter: yourname@company.com
3. Enter your Microsoft 365 password
4. Complete MFA verification
5. Your inbox loads in the browser
```

> **Note:** Do not save passwords on public / shared computers. Always click "Sign Out" when done on shared devices.

---

## 7. Email Signature Setup

All employees are required to use the standard company email signature.

### Standard Signature Format

```
Full Name
Job Title | Department
Company Name
📞 +91-XX-XXXX-XXXX (Ext. XXXX)
📧 yourname@company.com
🌐 www.company.com

[Company Logo]
```

### Setting Up Signature in Outlook (Desktop)

```
1. Open Outlook → File → Options → Mail → Signatures
2. Click "New" → Name the signature (e.g., "Standard")
3. Paste or type the signature in the editor
4. Set it as default for New messages and Replies
5. Click OK
```

### Setting Up Signature in OWA

```
1. Open OWA → Settings (gear icon, top right)
2. Search "Email Signature"
3. Type or paste the signature
4. Check "Automatically include signature on new messages"
5. Click Save
```

---

## 8. Common Email Troubleshooting

| Issue | Solution |
|-------|---------|
| "Cannot connect to server" | Check internet / VPN connection; restart Outlook |
| Emails not sending | Check Outbox folder; verify recipient email address |
| Outlook keeps asking for password | Clear cached credentials: Control Panel → Credential Manager → Windows Credentials → Remove Microsoft Office entries → Restart Outlook |
| "Your mailbox is full" | Delete old emails / empty Deleted Items; contact IT if over-quota |
| Missing emails | Check Junk / Spam and Clutter folders; check filters/rules |
| Cannot access OWA | Try a different browser; clear browser cache; check VPN not blocking |
| Calendar not syncing | In Outlook, right-click calendar → Refresh; or restart Outlook |

---

## 9. Email Mailbox Limits

| Parameter | Limit |
|-----------|-------|
| Mailbox size | 100 GB |
| Maximum attachment size | 25 MB |
| Archive mailbox | Auto-enabled (unlimited archive) |
| Sent items retention | 2 years (auto-archived) |

> If you need to send files larger than 25 MB, upload to SharePoint or OneDrive and share the link instead.

---

## 10. Email Security Guidelines

| Practice | Required |
|----------|---------|
| Enable MFA for all email logins | Yes (mandatory) |
| Do not share email password | Yes (mandatory) |
| Do not click suspicious links | Yes |
| Verify sender before opening attachments | Yes |
| Report phishing emails | Yes — forward to phishing@company.com |
| Do not auto-forward email to personal accounts | Prohibited |
| Do not send confidential data to personal email | Prohibited |
| Encrypt sensitive emails | Required for financial / legal / HR data |

### Reporting Phishing

```
Method 1 — Report Button (Outlook Desktop):
  Select suspicious email → Click "Report" → "Report Phishing"

Method 2 — Forward:
  Forward the suspicious email to: phishing@company.com

Method 3 — Microsoft Junk Filter:
  Right-click email → Junk → Report as Phishing
```

---

## 11. Distribution Lists & Shared Mailboxes

### Requesting a New Distribution List (DL)

```
1. Go to helpdesk.company.com
2. New Request → Email → Distribution List Request
3. Provide: DL name, members, owner, purpose
4. IT creates and shares the DL details within 2 working days
```

### Requesting Access to a Shared Mailbox

```
1. Go to helpdesk.company.com
2. New Request → Email → Shared Mailbox Access
3. Provide: Shared mailbox address, your employee ID, manager approval
4. Access granted within 1 working day after manager approval
```

---

## 12. FAQs

**Q: My Outlook is not working. What should I do?**  
A: First, restart Outlook. If that doesn't help, check your internet connection and try OWA at `outlook.office.com`. If OWA works but Outlook doesn't, repair Outlook from Control Panel → Apps → Microsoft 365 → Modify → Quick Repair. If still not working, raise an IT helpdesk ticket.

**Q: How do I configure email on my personal phone?**  
A: Download the Microsoft Outlook app from App Store / Play Store, add your corporate email, and complete MFA setup. You will be prompted to enroll the device in company mobile management (Intune).

**Q: How do I access my email when I'm traveling abroad?**  
A: Use OWA at `https://outlook.office.com` or the Outlook mobile app. Both work worldwide without VPN.

**Q: I received a suspicious email. What should I do?**  
A: Do not click any links or download attachments. Forward the email to `phishing@company.com` and delete it. Report to IT if you accidentally clicked a link.

**Q: How do I send a file larger than 25MB?**  
A: Upload the file to OneDrive or SharePoint and share the link via email instead of attaching the file directly.

---

*For email issues, contact IT Help Desk at helpdesk.company.com or call Ext. 1100.*
