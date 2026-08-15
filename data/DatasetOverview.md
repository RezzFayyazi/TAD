# Reference Events Report - Attack Timeline

## Overview

| Metric | Value |
|--------|-------|
| **Total Windows** | 10 |
| **Total Reference Events (Attacks)** | 20 |
| **Total Extracted Logs** | 587 |
| **Timeline** | 2025-10-10 18:51 to 2025-10-11 20:48 |
---

## Attack Categories Summary

| Attack Type | Count |
|-------------|-------|
| Pass-the-Hash (NTLM Remote Logon) | 9 |
| Malicious Service Creation (PowerShell Payload) | 2 |
| PSEXESVC Service Installation | 2 |
| Registry Modification (BAM - Malicious Tool Execution) | 4 |
| Credential Brute Force (Logon Failure) | 1 |
| Interactive Logon Success with Compromised Credentials | 1 |
| Registry Value Integrity Change | 1 |

---

## Window Timeline Summary

| Window | Start Time | End Time | Duration | Reference Events | Extracted Logs |
|--------|------------|----------|----------|------------------|----------------|
| 1 | `2025-10-10T18:51:21.254Z` | `2025-10-10T18:52:16.427Z` | ~55 sec | 3 | 71 |
| 2 | `2025-10-10T18:56:59.032Z` | `2025-10-10T18:57:45.889Z` | ~47 sec | 1 | 48 |
| 3 | `2025-10-10T19:02:21.246Z` | `2025-10-10T19:03:40.978Z` | ~80 sec | 2 | 48 |
| 4 | `2025-10-10T19:09:46.700Z` | `2025-10-10T19:11:17.700Z` | ~91 sec | 4 | 50 |
| 5 | `2025-10-10T19:54:49.621Z` | `2025-10-10T19:55:47.495Z` | ~58 sec | 3 | 46 |
| 6 | `2025-10-10T20:00:00.416Z` | `2025-10-10T20:01:41.837Z` | ~101 sec | 3 | 59 |
| 7 | `2025-10-11T03:35:51.185Z` | `2025-10-11T03:37:51.264Z` | ~120 sec | 1 | 81 |
| 8 | `2025-10-11T06:56:27.952Z` | `2025-10-11T06:57:05.931Z` | ~38 sec | 1 | 47 |
| 9 | `2025-10-11T18:56:41.583Z` | `2025-10-11T18:57:26.003Z` | ~44 sec | 1 | 50 |
| 10 | `2025-10-11T20:48:45.455Z` | `2025-10-11T20:48:46.901Z` | ~1 sec | 1 | 87 |

---

## Detailed Timeline

### Window 1

**Time Range:** `2025-10-10T18:51:21.254000Z` → `2025-10-10T18:52:16.427000Z`

**Reference Events:** 3 | **Surrounding Logs:** 71

| # | Timestamp | Target | Agent | Attack Type | Description |
|---|-----------|--------|-------|-------------|-------------|
| 1 | `2025-10-10T18:51:51.588Z` | robb.stark | npc-petyerbaeli (192.168.56.154) | **Credential Brute Force** | Logon Failure - Unknown user or bad password |
| 2 | `2025-10-10T18:52:02.711Z` | robb.stark | npc-petyerbaeli (192.168.56.154) | **Interactive Logon Success** | Windows Workstation Logon Success - Type 2 logon with elevated token |
| 3 | `2025-10-10T18:52:04.033Z` | robb.stark | winterfell (192.168.56.11) | **Pass-the-Hash Attack** | Successful Remote Logon Detected - NTLM auth from NPC-PETYERBAELI |

---

### Window 2

**Time Range:** `2025-10-10T18:56:59.032000Z` → `2025-10-10T18:57:45.889000Z`

**Reference Events:** 1 | **Surrounding Logs:** 48

| # | Timestamp | Target | Agent | Attack Type | Description |
|---|-----------|--------|-------|-------------|-------------|
| 1 | `2025-10-10T18:57:20.490Z` | robb.stark | winterfell (192.168.56.11) | **Pass-the-Hash Attack** | Successful Remote Logon Detected - NTLM auth from NPC-PETYERBAELI |

---

### Window 3

**Time Range:** `2025-10-10T19:02:21.246000Z` → `2025-10-10T19:03:40.978000Z`

**Reference Events:** 2 | **Surrounding Logs:** 48

| # | Timestamp | Target | Agent | Attack Type | Description |
|---|-----------|--------|-------|-------------|-------------|
| 1 | `2025-10-10T19:03:00.869Z` | robb.stark | winterfell (192.168.56.11) | **Pass-the-Hash Attack** | Successful Remote Logon Detected - NTLM auth from WORKSTATION |
| 2 | `2025-10-10T19:03:03.934Z` | N/A | winterfell (192.168.56.11) | **Malicious Service Installation** | PowerShell payload service "fVgzEnyJxkWfxKXW" created |

---

### Window 4

**Time Range:** `2025-10-10T19:09:46.700000Z` → `2025-10-10T19:11:17.700000Z`

**Reference Events:** 4 | **Surrounding Logs:** 50

| # | Timestamp | Target | Agent | Attack Type | Description |
|---|-----------|--------|-------|-------------|-------------|
| 1 | `2025-10-10T19:10:19.446Z` | robb.stark | kingslanding (192.168.56.10) | **Pass-the-Hash Attack** | Successful Remote Logon Detected - NTLM auth from WORKSTATION |
| 2 | `2025-10-10T19:10:21.685Z` | robb.stark | winterfell (192.168.56.11) | **Pass-the-Hash Attack** | Successful Remote Logon Detected - NTLM auth from WORKSTATION |
| 3 | `2025-10-10T19:10:24.735Z` | N/A | winterfell (192.168.56.11) | **Malicious Service Installation** | PowerShell payload service "BMydrzyUmFzhXhKl" created |
| 4 | `2025-10-10T19:10:43.194Z` | robb.stark | meereen (192.168.56.12) | **Pass-the-Hash Attack** | Successful Remote Logon Detected - NTLM auth from WORKSTATION |

---

### Window 5

**Time Range:** `2025-10-10T19:54:49.621000Z` → `2025-10-10T19:55:47.495000Z`

**Reference Events:** 3 | **Surrounding Logs:** 46

| # | Timestamp | Target | Agent | Attack Type | Description |
|---|-----------|--------|-------|-------------|-------------|
| 1 | `2025-10-10T19:55:25.254Z` | robb.stark | winterfell (192.168.56.11) | **Pass-the-Hash Attack** | Successful Remote Logon Detected - NTLM auth from NPC-PETYERBAELI |
| 2 | `2025-10-10T19:55:26.521Z` | N/A | winterfell (192.168.56.11) | **PSEXESVC Installation** | PsExec service deployed from Windows root path |
| 3 | `2025-10-10T19:55:26.566Z` | robb.stark | winterfell (192.168.56.11) | **Pass-the-Hash Attack** | Successful Remote Logon Detected - NTLM auth from NPC-PETYERBAELI |

---

### Window 6

**Time Range:** `2025-10-10T20:00:00.416000Z` → `2025-10-10T20:01:41.837000Z`

**Reference Events:** 3 | **Surrounding Logs:** 59

| # | Timestamp | Target | Agent | Attack Type | Description |
|---|-----------|--------|-------|-------------|-------------|
| 1 | `2025-10-10T20:00:28.740Z` | robb.stark | kingslanding (192.168.56.10) | **Pass-the-Hash Attack** | Successful Remote Logon Detected - NTLM auth from NPC-PETYERBAELI |
| 2 | `2025-10-10T20:01:06.369Z` | N/A | winterfell (192.168.56.11) | **PSEXESVC Installation** | PsExec service (%SystemRoot%\PSEXESVC.exe) deployed |
| 3 | `2025-10-10T20:01:06.575Z` | robb.stark | winterfell (192.168.56.11) | **Pass-the-Hash Attack** | Successful Remote Logon Detected - NTLM auth from NPC-PETYERBAELI |

---

### Window 7

**Time Range:** `2025-10-11T03:35:51.185000Z` → `2025-10-11T03:37:51.264000Z`

**Reference Events:** 1 | **Surrounding Logs:** 81

| # | Timestamp | Target | Agent | Attack Type | Description |
|---|-----------|--------|-------|-------------|-------------|
| 1 | `2025-10-11T03:36:16.781Z` | N/A | castelblack (192.168.56.22) | **Registry Persistence/Modification** | COLIncrease.exe execution tracked via BAM registry |

---

### Window 8

**Time Range:** `2025-10-11T06:56:27.952000Z` → `2025-10-11T06:57:05.931000Z`

**Reference Events:** 1 | **Surrounding Logs:** 47

| # | Timestamp | Target | Agent | Attack Type | Description |
|---|-----------|--------|-------|-------------|-------------|
| 1 | `2025-10-11T06:57:04.447Z` | N/A | npc-petyerbaeli (192.168.56.154) | **Registry Persistence/Modification** | PsExec64.exe execution tracked via BAM registry |

---

### Window 9

**Time Range:** `2025-10-11T18:56:41.583000Z` → `2025-10-11T18:57:26.003000Z`

**Reference Events:** 1 | **Surrounding Logs:** 50

| # | Timestamp | Target | Agent | Attack Type | Description |
|---|-----------|--------|-------|-------------|-------------|
| 1 | `2025-10-11T18:57:24.178Z` | N/A | npc-petyerbaeli (192.168.56.154) | **Registry Integrity Change** | COLIncrease.exe binary modified (hash changed) |

---

### Window 10

**Time Range:** `2025-10-11T20:48:45.455000Z` → `2025-10-11T20:48:46.901000Z`

**Reference Events:** 1 | **Surrounding Logs:** 87

| # | Timestamp | Target | Agent | Attack Type | Description |
|---|-----------|--------|-------|-------------|-------------|
| 1 | `2025-10-11T20:48:46.461Z` | N/A | vdi-samwell-tar (192.168.56.111) | **Registry Persistence/Modification** | DefenderRemover.exe execution tracked via BAM registry |

---

## Reference Events Detail

Below are the full details of each reference event grouped by attack type.

### Pass-the-Hash / NTLM Remote Logon Attacks

These events indicate successful remote logons using NTLM authentication, which is a common indicator of pass-the-hash attacks where attackers use stolen password hashes to authenticate.

| Window | Timestamp | Victim User | Source Workstation | Target Host |
|--------|-----------|-------------|-------------------|-------------|
| 1 | `2025-10-10T18:52:04.033Z` | robb.stark | NPC-PETYERBAELI | winterfell |
| 2 | `2025-10-10T18:57:20.490Z` | robb.stark | NPC-PETYERBAELI | winterfell |
| 3 | `2025-10-10T19:03:00.869Z` | robb.stark | WORKSTATION | winterfell |
| 4 | `2025-10-10T19:10:19.446Z` | robb.stark | WORKSTATION | kingslanding |
| 4 | `2025-10-10T19:10:21.685Z` | robb.stark | WORKSTATION | winterfell |
| 4 | `2025-10-10T19:10:43.194Z` | robb.stark | WORKSTATION | meereen |
| 5 | `2025-10-10T19:55:25.254Z` | robb.stark | NPC-PETYERBAELI | winterfell |
| 5 | `2025-10-10T19:55:26.566Z` | robb.stark | NPC-PETYERBAELI | winterfell |
| 6 | `2025-10-10T20:00:28.740Z` | robb.stark | NPC-PETYERBAELI | kingslanding |
| 6 | `2025-10-10T20:01:06.575Z` | robb.stark | NPC-PETYERBAELI | winterfell |

### Credential Brute Force Attempt

Initial failed logon attempt before successful compromise.

| Window | Timestamp | Target User | Agent | Source |
|--------|-----------|-------------|-------|--------|
| 1 | `2025-10-10T18:51:51.588Z` | robb.stark | npc-petyerbaeli | 127.0.0.1 (local) |

### Interactive Logon Success with Compromised Credentials

Local (Logon Type 2) logon success on the attacker-controlled workstation, 11 seconds after the failed attempt. The session is created with an **elevated token**, giving the attacker an administrative `robb.stark` context on NPC-PETYERBAELI that is used to launch the remote NTLM authentications that follow.

| Window | Timestamp | Account | Agent | Logon Type | Details |
|--------|-----------|---------|-------|------------|---------|
| 1 | `2025-10-10T18:52:02.711Z` | robb.stark (NORTH) | npc-petyerbaeli | 2 (Interactive) | Elevated Token: Yes, Logon ID `0xA1BD3B8`, Source 127.0.0.1, Process `svchost.exe` |

### Malicious Service Creation (PowerShell Payload)

These events indicate the creation of Windows services containing obfuscated PowerShell payloads designed to bypass AMSI (Antimalware Scan Interface) and script block logging. The payloads include Base64-encoded GZip-compressed scripts.

| Window | Timestamp | Agent | Service Name | Payload Type |
|--------|-----------|-------|--------------|--------------|
| 3 | `2025-10-10T19:03:03.934Z` | winterfell | **fVgzEnyJxkWfxKXW** | Obfuscated PowerShell with AMSI bypass |
| 4 | `2025-10-10T19:10:24.735Z` | winterfell | **BMydrzyUmFzhXhKl** | Obfuscated PowerShell with AMSI bypass |

#### Malicious Service Characteristics

Both services share the following characteristics:
- **Service File Name:** `%COMSPEC% /b /c start /b /min powershell.exe -nop -w hidden -noni -c ...`
- **Service Type:** user mode service
- **Service Start Type:** demand start
- **Service Account:** LocalSystem

The PowerShell payloads contain:
- AMSI bypass techniques (setting `amsiInitFailed` to true)
- Script Block Logging bypass
- Base64-encoded, GZip-compressed secondary payload
- Process creation in hidden window mode

### PSEXESVC Service Installation

These events indicate deployment of PsExec's service component, commonly used for lateral movement and remote execution.

| Window | Timestamp | Agent | Service Details |
|--------|-----------|-------|-----------------|
| 5 | `2025-10-10T19:55:26.521Z` | winterfell | PSEXESVC installed |
| 6 | `2025-10-10T20:01:06.369Z` | winterfell | PSEXESVC installed from %SystemRoot%\PSEXESVC.exe |

**Service Characteristics:**
- **Service Name:** PSEXESVC
- **Service File Name:** %SystemRoot%\PSEXESVC.exe
- **Service Type:** user mode service
- **Service Start Type:** demand start
- **Service Account:** LocalSystem

### Registry Modifications (Malicious Tool Execution)

These events indicate registry modifications tracking malicious executable activity via the Background Activity Moderator (BAM) registry key, which records program execution history.

| Window | Timestamp | Agent | Executable | User Context | Action |
|--------|-----------|-------|------------|--------------|--------|
| 7 | `2025-10-11T03:36:16.781Z` | castelblack | **COLIncrease.exe** | robb.stark | Added |
| 8 | `2025-10-11T06:57:04.447Z` | npc-petyerbaeli | **PsExec64.exe** | robb.stark | Added |
| 9 | `2025-10-11T18:57:24.178Z` | npc-petyerbaeli | **COLIncrease.exe** | petyer.baelish | Modified (hash changed) |
| 10 | `2025-10-11T20:48:46.461Z` | vdi-samwell-tar | **DefenderRemover.exe** | nightwatchguard | Added |

#### Malicious Executables Detail

| Executable | Purpose | Locations Found |
|------------|---------|-----------------|
| **COLIncrease.exe** | Likely privilege escalation or persistence tool | `C:\Users\robb.stark\Desktop\`, `C:\Users\petyer.baelish\Downloads\` |
| **PsExec64.exe** | Sysinternals remote execution tool (commonly abused for lateral movement) | `C:\Users\robb.stark\Downloads\` |
| **DefenderRemover.exe** | Windows Defender disabling tool (defense evasion) | `C:\Users\NIGHTW~1\AppData\Local\Temp\` |

#### COLIncrease.exe Hash Changes (Window 9)

The COLIncrease.exe binary was modified on petyer.baelish's system, indicating potential recompilation or variant deployment:

| Hash Type | Old Value | New Value |
|-----------|-----------|-----------|
| MD5 | `f3778c11e4b80745924b35245c5602de` | `64bab0e9c9e7785a09b965bc2800de54` |
| SHA1 | `d4f20c2e78c006df9c04b446e493b580cf42d51e` | `4d8d56ef9ee07677a58694f52ed78137f5e58cc3` |
| SHA256 | `d49fc07b04324f97391cf249227de13630e99c2b563324346812de9d6b8f0d83` | `4269a7295ad8e0735e45306f41371532ff80bfa1d7e0e172167005dfc77f9fed` |

---

## Attack Progression Summary

1. **Initial Access & Credential Validation (Window 1, Oct 10 ~18:51-18:52):** Failed logon attempt against `robb.stark` on attacker workstation NPC-PETYERBAELI, followed 11 seconds later by a successful interactive (Type 2) logon with an elevated token on the same host, and 1.3 seconds after that by a successful pass-the-hash attack on winterfell.

2. **Lateral Movement Phase 1 (Window 2-4, Oct 10 ~18:57-19:10):** Continued pass-the-hash attacks targeting `robb.stark` account with NTLM authentication. Foothold established on winterfell, kingslanding, and meereen — the Window 4 sweep hits all three from consecutive source ports (49814-49816). Malicious PowerShell services deployed with AMSI bypass capabilities, each preceded by an NTLM logon to the same host.

3. **Lateral Movement Phase 2 (Window 5-6, Oct 10 ~19:55-20:01):** Deployment of PsExec (PSEXESVC) for remote execution capabilities. Additional pass-the-hash attacks from NPC-PETYERBAELI.

4. **Tool Deployment & Defense Evasion (Window 7-10, Oct 11 ~03:35-20:48):**
   - **Window 7:** `COLIncrease.exe` executed on castelblack under robb.stark context
   - **Window 8:** `PsExec64.exe` deployed on attacker workstation for remote execution capabilities
   - **Window 9:** `COLIncrease.exe` modified/recompiled on petyer.baelish's system (hash changed)
   - **Window 10:** `DefenderRemover.exe` executed to disable Windows Defender on vdi-samwell-tar

---

## Key Indicators of Compromise (IOCs)

### Network

- **Attacker Workstation:** `NPC-PETYERBAELI` (192.168.56.154)
- **Source IPs:** 192.168.56.154
- **Target Hosts:**
  - winterfell (192.168.56.11)
  - kingslanding (192.168.56.10)
  - meereen (192.168.56.12)
  - castelblack (192.168.56.22)
  - vdi-samwell-tar (192.168.56.111)

### Malicious Files

| File | MD5 | SHA256 |
|------|-----|--------|
| **COLIncrease.exe** (v1) | `f3778c11e4b80745924b35245c5602de` | `d49fc07b04324f97391cf249227de13630e99c2b563324346812de9d6b8f0d83` |
| **COLIncrease.exe** (v2) | `64bab0e9c9e7785a09b965bc2800de54` | `4269a7295ad8e0735e45306f41371532ff80bfa1d7e0e172167005dfc77f9fed` |
| **PsExec64.exe** | - | - |
| **DefenderRemover.exe** | - | - |

### Malicious Service Names

| Service Name | Type |
|--------------|------|
| `fVgzEnyJxkWfxKXW` | Randomized name - PowerShell payload |
| `BMydrzyUmFzhXhKl` | Randomized name - PowerShell payload |
| `PSEXESVC` | PsExec service |

---

