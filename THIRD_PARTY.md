# Third-party components shipped with Mucify

| Component | Where | Licence |
|---|---|---|
| **sldl** (slsk-batchdl, tested build) | `tools/sldl/` | GNU AGPL-3.0 (`tools/sldl/LICENSE.txt`) |
| **rsgain** 3.7 | `tools/rsgain/` | BSD-2-Clause (`tools/rsgain/LICENSE.txt`, `LICENSE-CRCpp.txt`); Microsoft VC++ runtime DLLs bundled alongside |
| Flask, Requests, Mutagen, pywebview, PyInstaller | Python dependencies | BSD / Apache-2.0 / LGPL-2.1+ (Mutagen) / MIT as published by each project |

**AGPL note:** sldl is AGPL-3.0. If the bundled `sldl.exe` is a modified build ("fixed version"), the AGPL requires you to make the corresponding source of that build available to the people you distribute it to. Keep a link to the source (e.g. your fork) here and in the repository before sharing installers publicly.
