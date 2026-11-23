# WIC3002 G07 - Ed25519: Signing an Official Digital Notice

> M3 will later replace this file with the full runbook.

## Shared interface

File names and commands are fixed after 25 Nov.

| File | Owner | Command | Result |
|---|---|---|---|
| keygen.py | M2 | `python keygen.py` | creates `faculty_private.pem` and `faculty_public.pem` |
| sign.py | M2 | `python sign.py notice.txt faculty_private.pem` | creates `notice.sig` |
| verify.py | M4 | `python verify.py notice.txt notice.sig faculty_public.pem` | prints `VALID` or `INVALID` |
| attacker.py | M1 | `python attacker.py notice_edited.txt` | creates `attacker_private.pem`, `attacker_public.pem` and `attacker.sig` |
| fingerprint.py | M1 | `python fingerprint.py faculty_public.pem` | prints a short SHA-256 fingerprint |

M3 owns `notice.txt`, `requirements.txt` and the README runbook.

## What this project shows

The faculty signs `notice.txt` with its Ed25519 private key, and anyone holding `faculty_public.pem` can check that the notice is genuine and unchanged. An attacker who edits the notice can sign the edited copy with their own key, but that signature only verifies under the attacker's public key, never under the faculty key. So the signature is only as trustworthy as the public key you check it with, which is why `fingerprint.py` exists: it lets you confirm you are holding the genuine faculty key.

## Setup

You need Python 3.8 or newer.

Create and activate a virtual environment in the repo folder.

Windows (PowerShell):

```
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows (Command Prompt): run `.venv\Scripts\activate.bat` instead of the second line.

macOS / Linux:

```
python3 -m venv .venv
source .venv/bin/activate
```

Then install the only dependency:

```
pip install cryptography
```

`requirements.txt` (pending, owner: M3) will replace this step with `pip install -r requirements.txt`.

## Attack demo (M1)

Before you start you need `notice.txt` (pending, owner: M3) and `faculty_public.pem` from `keygen.py` (pending, owner: M2). The `verify.py` steps also need `verify.py` (pending, owner: M4).

1. Make the attacker's copy of the notice. Change only the date and save it.

   ```
   copy notice.txt notice_edited.txt      (Windows)
   cp notice.txt notice_edited.txt        (macOS / Linux)
   ```

2. Sign the edited notice with a fresh attacker key:

   ```
   python attacker.py notice_edited.txt
   ```

   Sample output (your values will differ):

   ```
   Attacker key pair generated (Ed25519)

   Notice signed:   notice_edited.txt (<n> bytes)
   Private key:     attacker_private.pem  (kept secret, not shown)
   Public key:      attacker_public.pem
   Signature file:  attacker.sig
   Signature size:  64 bytes
   Signature (hex): 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
   Note: running this again creates a NEW attacker key pair and overwrites these files.
   ```

   This creates `attacker_private.pem`, `attacker_public.pem` and `attacker.sig` (the raw 64-byte signature) in the current folder.

3. Compare the fingerprints of the two public keys:

   ```
   python fingerprint.py faculty_public.pem
   python fingerprint.py attacker_public.pem
   ```

   Sample output (placeholder values):

   ```
   File:        faculty_public.pem
   Raw key:     32 bytes
   Fingerprint: 1111 2222 3333 4444
   SHA-256:     1111222233334444555566667777888811112222333344445555666677778888
   ```

   ```
   File:        attacker_public.pem
   Raw key:     32 bytes
   Fingerprint: aaaa bbbb cccc dddd
   SHA-256:     aaaabbbbccccddddeeeeffff00009999aaaabbbbccccddddeeeeffff00009999
   ```

   The fingerprint is the first 16 hex characters of the SHA-256 of the raw 32-byte key. The same key always gives the same fingerprint, and the two keys give completely different ones. That is how a reader spots that they were handed the wrong key.

4. Verify the edited notice under each key (`verify.py` pending, owner: M4):

   ```
   python verify.py notice_edited.txt attacker.sig attacker_public.pem
   python verify.py notice_edited.txt attacker.sig faculty_public.pem
   ```

   Expected results:

   - `attacker_public.pem`: `VALID`
   - `faculty_public.pem`: `INVALID`

If something goes wrong, both scripts print a one-line message and exit, for example:

```
Usage: python attacker.py <notice_file>
Error: notice file 'notice_edited.txt' not found.
Usage: python fingerprint.py <public_key.pem>
Error: cannot read key file 'faculty_public.pem'.
Error: 'faculty_public.pem' is not a valid PEM public key.
```

## Gotchas

- Each run of `attacker.py` creates a NEW key pair and overwrites `attacker_private.pem`, `attacker_public.pem` and `attacker.sig`, so the attacker fingerprint changes every time. Run it once, then record the demo.
- Do not edit or re-save `notice_edited.txt` after signing it. Any byte change, even an editor adding a newline or changing line endings, makes verification fail.
- Never print, paste or share any `*_private.pem` file. The scripts only ever show the private key's file name, not its contents.

## Line endings

A signature covers the exact bytes of the file, so a CRLF (Windows) vs LF (macOS/Linux) difference is enough to break verification. The repo's `.gitattributes` marks `notice*.txt` and `*.pem` as `-text` and `*.sig` as `binary`, so Git never converts them between CRLF and LF. A notice signed on Windows therefore still verifies after a teammate pulls it on macOS or Linux. `attacker.py` and `fingerprint.py` also read files in binary mode for the same reason.

## Before you commit

- Stage specific files with `git add <file1> <file2>`. Never use `git add .`.
- Run `git status` and check that only the files you meant to change are staged.
- No `.pem` or `.sig` files in commits. `.gitignore` already ignores `*.pem`, `*.sig` and `notice_edited.txt`, but check anyway.
