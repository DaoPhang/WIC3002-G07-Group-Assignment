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