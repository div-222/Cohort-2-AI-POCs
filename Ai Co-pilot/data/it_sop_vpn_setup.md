# IT SOP: VPN Setup & Configuration
**Document Type:** IT Standard Operating Procedure  
**Category:** Remote Access  
**SOP ID:** IT-SOP-002  
**Version:** 1.8  
**Effective Date:** January 1, 2026  
**Owner:** IT Department  

---

## 1. Overview

This SOP provides step-by-step instructions for setting up and using the company VPN (Virtual Private Network). The VPN is mandatory for accessing internal systems and company resources when working remotely or from outside the office network.

**VPN Software:** Cisco AnyConnect Secure Mobility Client  
**VPN Server:** `vpn.company.com`

---

## 2. Prerequisites

Before setting up VPN, ensure you have:

- [ ] A company-issued laptop or an approved personal device
- [ ] Your corporate email address (`yourname@company.com`)
- [ ] Your current Active Directory / Microsoft 365 password
- [ ] Microsoft Authenticator app installed on your mobile phone
- [ ] Multi-Factor Authentication (MFA) set up on your account (done during onboarding)

---

## 3. VPN Installation

### 3.1 Windows — Install Cisco AnyConnect

```
Option A — From IT Software Portal (Recommended):
  1. Open browser → Go to software.company.com
  2. Log in with your corporate email
  3. Search for "Cisco AnyConnect"
  4. Click "Install" → Follow the installer wizard
  5. Restart your laptop if prompted

Option B — From IT Help Desk (if software portal is inaccessible):
  1. Raise a helpdesk ticket: helpdesk.company.com
  2. Category: "Software Installation" → "Cisco AnyConnect"
  3. IT will push the software remotely or assist you on-site
```

### 3.2 macOS — Install Cisco AnyConnect

```
1. Go to software.company.com
2. Log in with your corporate email
3. Search for "Cisco AnyConnect macOS"
4. Download the .pkg installer
5. Open the downloaded file → Follow installation wizard
6. Allow required system permissions in:
   System Preferences → Security & Privacy → Allow Cisco Systems
7. Restart your Mac if prompted
```

### 3.3 Mobile Devices (iOS / Android)

```
iOS:
  1. Open App Store → Search "Cisco AnyConnect"
  2. Install the app (Publisher: Cisco Systems)
  3. Open app → Add VPN connection (see Section 4)

Android:
  1. Open Google Play Store → Search "Cisco AnyConnect"
  2. Install the app (Publisher: Cisco Systems)
  3. Open app → Add VPN connection (see Section 4)
```

> **Note:** Mobile VPN is available for employees who have received approval for mobile access. Contact IT for access provisioning.

---

## 4. VPN Connection Setup

### 4.1 Initial Configuration (First-Time Setup)

```
1. Open Cisco AnyConnect from Start Menu / Applications
2. In the connection field, enter:
      vpn.company.com
3. Click "Connect"
4. Username: Enter your full corporate email (user@company.com)
5. Password: Enter your current Microsoft 365 password
6. Group: Select "Remote-Employees" from the dropdown
7. Click "OK"
8. A Microsoft Authenticator push notification will appear on your phone
9. Approve the notification on your phone
10. VPN connected successfully ✅
```

### 4.2 Connection Screen Reference

```
┌─────────────────────────────────────────┐
│  Cisco AnyConnect                       │
│                                         │
│  Connect to: [ vpn.company.com        ] │
│                                         │
│  [ Connect ]                            │
└─────────────────────────────────────────┘

After clicking Connect:
┌─────────────────────────────────────────┐
│  Username: user@company.com             │
│  Password: ••••••••••••                 │
│  Group: [Remote-Employees ▼]           │
│  [ OK ]                                 │
└─────────────────────────────────────────┘
```

---

## 5. Connecting and Disconnecting

### Connect to VPN

```
1. Open Cisco AnyConnect (system tray icon on Windows)
2. Select "vpn.company.com" (saved from first setup)
3. Click Connect
4. Enter password if prompted (usually remembered)
5. Approve MFA notification on your phone
6. VPN icon turns green — connected ✅
```

### Disconnect from VPN

```
1. Click the Cisco AnyConnect icon in the system tray
2. Click "Disconnect"
3. VPN is now disconnected
```

> **Best Practice:** Disconnect VPN when not using company resources to optimize your internet speed for personal use.

---

## 6. Multi-Factor Authentication (MFA) for VPN

VPN access requires MFA. The company uses **Microsoft Authenticator** for MFA.

### Setting Up Microsoft Authenticator (First Time)

```
1. On your phone: Download "Microsoft Authenticator" from App Store / Play Store
2. On your laptop: Go to aka.ms/mfasetup
3. Log in with your corporate email
4. Follow the setup wizard:
   - Click "Add account" in the Authenticator app
   - Select "Work or School account"
   - Scan the QR code displayed on your laptop screen
5. Test the setup: Approve a test notification
6. MFA setup complete ✅
```

---

## 7. Accessing Internal Resources Over VPN

Once connected to VPN, you can access:

| Resource | URL / Path |
|---------|-----------|
| Internal HR Portal | portal.company.com |
| IT Help Desk | helpdesk.company.com |
| JIRA | jira.company.com |
| Confluence | confluence.company.com |
| Internal file shares | \\fileserver\shares\ |
| Internal applications | As provided by your team |
| Dev/staging environments | As per project runbook |

---

## 8. Split Tunnel Policy

The company VPN uses **split tunneling**:
- **Company traffic** (internal systems, internal URLs) → Routes through VPN.
- **General internet traffic** (browsing, YouTube, Netflix) → Direct internet (not through VPN).

This ensures optimal performance while maintaining security for internal resources.

---

## 9. Troubleshooting

### VPN Won't Connect

| Problem | Solution |
|---------|---------|
| Incorrect username/password | Reset password via `passwordreset.microsoftonline.com` |
| MFA notification not received | Check phone internet, resend notification, or use TOTP code from Authenticator app |
| AnyConnect says "Unable to contact VPN server" | Check your internet connection; try mobile hotspot to rule out local network issues |
| Account locked | Call IT Help Desk: Ext. 1100 |
| VPN connects but internal sites don't load | Try disconnecting and reconnecting; raise helpdesk ticket if issue persists |

### Slow VPN Performance

- Disconnect and reconnect to switch to a different VPN gateway.
- Ensure no large background downloads are running.
- Switch to a wired connection (Ethernet) if on Wi-Fi.

---

## 10. VPN Security Guidelines

- Never share your VPN credentials with anyone, including IT staff.
- Do not connect to VPN from public/unsecured Wi-Fi without additional protection.
- Always lock your screen (`Windows+L`) when stepping away from a VPN-connected device.
- Report any suspicious VPN activity to security@company.com immediately.
- VPN logs are monitored. Misuse may lead to disciplinary action.

---

## 11. FAQs

**Q: How do I set up VPN on my company laptop?**  
A: Install Cisco AnyConnect from the software portal at `software.company.com`. Enter `vpn.company.com` as the server, then log in with your corporate email and password, and approve the MFA prompt.

**Q: Does resetting my email password affect my VPN login?**  
A: Yes. Your VPN password is the same as your Microsoft 365 password. After a password reset, reconnect VPN with the new password.

**Q: I'm getting "Authentication failed" on VPN. What should I do?**  
A: First, try resetting your password at `passwordreset.microsoftonline.com`. If the issue persists, call IT Help Desk at Ext. 1100.

**Q: Can I access company resources without VPN?**  
A: Some tools like Outlook Web Access, SharePoint, and Teams are accessible without VPN. Internal tools, file servers, and databases require VPN.

**Q: Is VPN available 24/7?**  
A: Yes. VPN is available 24/7 for all authorized employees. For VPN outages or critical access issues outside business hours, contact on-call IT support at Ext. 1199.

---

*For VPN-related issues, raise a helpdesk ticket at `helpdesk.company.com` or call IT Help Desk at Ext. 1100.*
