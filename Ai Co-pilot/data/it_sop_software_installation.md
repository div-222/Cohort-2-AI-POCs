# IT SOP: Software Installation Process
**Document Type:** IT Standard Operating Procedure  
**Category:** Software Asset Management  
**SOP ID:** IT-SOP-004  
**Version:** 1.3  
**Effective Date:** January 1, 2026  
**Owner:** IT Department  

---

## 1. Overview

This SOP defines the process for requesting, approving, and installing software on company-issued devices. All software installations must be sanctioned by IT to ensure license compliance, security, and system stability.

---

## 2. Software Categories

### 2.1 Pre-Approved Software (No Approval Needed)

The following software is pre-approved and can be installed by the employee via the **IT Software Portal** (`software.company.com`):

| Category | Software |
|---------|---------|
| Productivity | Microsoft 365 (Word, Excel, PowerPoint, Teams, Outlook) |
| Communication | Slack, Zoom |
| Development | VS Code, Git, Node.js, Python, IntelliJ IDEA Community |
| Browsers | Google Chrome, Mozilla Firefox, Microsoft Edge |
| Security | 1Password, Microsoft Authenticator |
| Remote Access | Cisco AnyConnect VPN, Remote Desktop |
| Cloud CLI | AWS CLI, Azure CLI, GCP SDK |
| Containers | Docker Desktop, Kubernetes CLI (kubectl) |
| Design | Figma (web), draw.io |
| Database | DBeaver, PostgreSQL client, MySQL Workbench |

---

### 2.2 Manager-Approved Software

Requires manager approval via helpdesk ticket before installation:

| Software | Use Case |
|---------|---------|
| Adobe Creative Suite | Design / marketing roles |
| Tableau / Power BI Desktop | Data analytics roles |
| JetBrains IDEs (IntelliJ Ultimate, PyCharm Professional) | Developer roles |
| Postman (Pro) | API testing |
| Datadog / Grafana Agent | Monitoring / DevOps roles |
| GitHub Copilot | Developer productivity (license required) |
| Camtasia / Loom | Video recording / documentation |

---

### 2.3 IT & Management Approved Software

Requires both manager and IT Head approval:

| Software | Reason for Elevated Approval |
|---------|------------------------------|
| VirtualBox / VMware | Performance and security implications |
| Wireshark / network analyzers | Security-sensitive tool |
| Remote admin tools (AnyDesk, TeamViewer) | Remote access security risk |
| Custom / third-party scripts | Security review required |
| Software not in the IT catalog | Requires vendor evaluation |

---

## 3. Software Request Process

### 3.1 Install Pre-Approved Software (Self-Service)

```
1. Open browser on your company laptop
2. Go to: software.company.com
3. Log in with your corporate email (SSO)
4. Browse or search for the required software
5. Click "Install"
6. The installation runs silently in the background
7. Software is ready in 10–15 minutes
8. Check Start Menu / Applications for the installed software
```

---

### 3.2 Request Manager-Approved or Non-Catalog Software

```
Step 1: Go to helpdesk.company.com
Step 2: Click "New Request" → Category: "Software" → Sub-category: "Software Installation Request"
Step 3: Fill in the form:
        - Software name and version
        - Business justification
        - Vendor website / download link (if applicable)
        - Number of licenses needed
        - Urgency level
Step 4: Submit request
Step 5: Notification sent to your manager for approval
Step 6: Manager approves / rejects within 2 working days
Step 7: For elevated-approval software → IT Head reviews additionally
Step 8: Upon full approval, IT installs the software remotely (SCCM / Intune)
        → Employee notified via email when installation is complete
        → Standard installation time: 1–3 working days after approval
```

---

## 4. Prohibited Software

The following categories of software are **strictly prohibited** on company devices:

| Category | Examples |
|---------|---------|
| Unauthorized remote access tools | AnyDesk, TeamViewer (without IT approval) |
| Peer-to-peer / torrent clients | BitTorrent, uTorrent |
| Gaming software | Steam, Epic Games, etc. |
| Cryptocurrency mining software | Any mining application |
| Hacking / penetration tools | Nmap, Metasploit (unless explicitly approved for security team) |
| Unlicensed / cracked software | Any pirated application |
| Personal VPN software | NordVPN, ExpressVPN (conflicts with company VPN) |
| Unauthorized storage / sync tools | Personal Dropbox, Google Drive (unless role-approved) |

> Violation of this policy may result in disciplinary action including device quarantine, formal warning, or termination depending on the severity.

---

## 5. License Compliance

- All software must be used in compliance with the vendor's license agreement.
- Sharing of software licenses between employees is not permitted.
- License assignments are tracked in the IT Asset Management system.
- If a licensed software is no longer required, notify IT to release the license for reuse.

---

## 6. Software Uninstallation

If you no longer need a software and want to free up disk space or release a license:

```
1. Go to helpdesk.company.com → New Request → Software → Uninstall Request
2. Specify the software and reason
3. IT remotely uninstalls within 1 working day
```

Alternatively, for self-service installed software, you can uninstall via:
- **Windows:** Settings → Apps → Installed Apps → Select software → Uninstall
- **macOS:** Finder → Applications → Drag to Trash

---

## 7. Bring Your Own Device (BYOD) Policy

- **Company data must not be stored on personal devices** unless explicitly authorized by IT.
- BYOD is permitted only for Microsoft Teams, Outlook (mobile), and Authenticator app.
- Employees using personal devices for company work must enroll them in Microsoft Intune for device compliance.

---

## 8. SLA for Software Requests

| Request Type | SLA |
|-------------|-----|
| Pre-approved (self-service) | Immediate (15–30 minutes) |
| Manager-approved software | 1–3 working days after approval |
| Non-catalog / elevated approval | 5–10 working days (includes evaluation) |
| Emergency installation (P1 business impact) | Same day with manager + IT Head verbal approval |

---

## 9. FAQs

**Q: How do I install VS Code on my company laptop?**  
A: Go to `software.company.com`, search for "VS Code", and click Install. No approval needed.

**Q: Can I install Tableau Desktop on my laptop?**  
A: Tableau Desktop requires manager approval. Raise a ticket at `helpdesk.company.com` → Software → Software Installation Request with your business justification.

**Q: Can I use a personal Dropbox account to store work files?**  
A: No. Personal storage services are not permitted for company data. Use OneDrive or SharePoint for file storage.

**Q: I need a software that isn't in the IT catalog. How do I request it?**  
A: Raise a helpdesk ticket with the software name, vendor link, and business justification. IT will evaluate and add it to the catalog if approved.

**Q: I accidentally installed unauthorized software. What should I do?**  
A: Self-disclose to IT immediately by raising a ticket. IT will help you uninstall it. Proactive disclosure is treated with leniency; concealment is not.

---

*For software requests, contact IT Help Desk at helpdesk.company.com or Ext. 1100.*
