# Mucify

Turn a Spotify playlist export into a high-quality FLAC library: **dedupe → Qobuz quality lookup → Soulseek download → ReplayGain**, in a normal Windows desktop app.

## For users

1. Download **Mucify-Setup-x.y.z.exe** (from the repository's *Actions* run or *Releases* page) and run it.
2. Click through the installer. It adds Start Menu and (optionally) Desktop shortcuts and installs the Microsoft Edge WebView2 runtime if your PC doesn't have it yet.
3. Open **Mucify**. The first-run setup walks you through:
   - **Soulseek login**: a random username and password are filled in for you (🎲 re-rolls either one). Press *Test connection* to check them. If the username is new, Soulseek creates the account on first login.
   - **Qobuz** *(optional)*: *Connect Qobuz* opens a login window; Mucify picks up the connection automatically. Or press *Skip for now*. Without Qobuz, tracks default to 24-bit / 48 kHz.
   - **Folders**: created for you: `Music\Mucify` (library) and `%APPDATA%\Mucify\Working` (CSVs, reports). Change them any time in **Settings**.
4. Pipeline: **Playlist Manager** (optional dedupe) → **Qobuz Enrich** → **Downloader** → **Post-Processing (ReplayGain)**. A starting CSV comes from [chosic.com/spotify-playlist-exporter](https://www.chosic.com/spotify-playlist-exporter/).

### Where your files go
Each playlist gets its own folder inside the working folder (`%APPDATA%\Mucify\Working` by default), filled in automatically:

| File | What it holds |
|---|---|
| `1_to_download.csv` | Tracks you don't have yet (after the Playlist Manager compare) |
| `2_enriched.csv` | The same tracks with Qobuz quality info |
| `3_skipped.csv` | **Everything that was not downloaded** (no match, slow peers, failed, never attempted). Feed it back into the Downloader to retry only these |
| `4_successful.csv` | Everything that was downloaded |

A small card at the bottom-right of each step offers the file the previous step just produced; tap it to use it. The Playlist Manager's library has a **Backup** button that saves the whole library as one CSV. The Downloader tries up to 15 times per track and never accepts lower FLAC quality than the first pick.

### Settings you may want
- **Background music:** under *Settings → Background music* pick your own MP3/FLAC **file** (it loops) or a whole **folder** (every MP3/FLAC inside, sub-folders included, is shuffled and reshuffled when the list ends; *Next track* skips). Switch it on/off or change the volume any time.
- **Reset Mucify:** clears all settings, logins and app data and shows the first-run setup again.
- **Uninstall Mucify:** removes all saved data (and optionally your playlist lists and the default `Music\Mucify` library), then opens the Windows uninstaller. Your music is only deleted if you tick that box, and only Mucify's own default music folder is ever deleted.

### Where Mucify keeps its data
`%APPDATA%\Mucify` (that is `C:\Users\<you>\AppData\Roaming\Mucify`; AppData is a hidden folder). Settings, logins and the first-run flag live there, which is why a reinstall alone keeps your settings. Use *Reset* / *Uninstall* in Settings, or answer **Yes** when the uninstaller asks to delete settings.

### Qobuz tips
- **Sign in with an email and password.** Google, Apple and Facebook sign-in don't work inside Mucify's window. Create your account at [qobuz.com/signin](https://qobuz.com/signin) in your browser, then sign in inside Mucify with those details.
- **VPN:** if Qobuz isn't available in your region, use a VPN (for example the Windscribe Chrome extension) **only while creating the account** in your browser. Signing in inside Mucify normally doesn't need it. A browser extension doesn't cover Mucify's own window; a system-wide VPN does.
- **Token expired?** A red banner appears with a **Reconnect** button, and Qobuz Enrich stops instead of guessing. Reconnect and run again.
- **Manual option:** *Paste the token manually* is always available under the Connect button, with the steps shown in the app.

### Troubleshooting
- *"Windows protected your PC"*: the installer isn't code-signed. Choose **More info → Run anyway**.
- *Mucify won't open*: details are saved to `%APPDATA%\Mucify\logs\crash.log`.
- Settings and data live in `%APPDATA%\Mucify`. Uninstalling asks whether to remove them; your music is never deleted.

---

## For developers

### Build (GitHub Actions)
Push the repository to GitHub. The workflow in `.github/workflows/build-windows.yml` runs on every push / PR / manual dispatch:

`tests → PyInstaller (dist\Mucify\Mucify.exe) → packaged-app self-test → Inno Setup installer`

Download **Mucify-Setup-x.y.z** (and a portable zip) from the run's *Artifacts*. Pushing a tag like `v1.0.1` also attaches both files to a GitHub Release and uses the tag as the version.

### Build locally (Windows, Python 3.11 x64, Inno Setup 6)
```powershell
./build.ps1              # tests, exe, self-test, installer -> installer\Output\
./build.ps1 -SkipInstaller
```
Run from source for development: `pip install -r requirements.txt` then `python -m mucify` (needs Windows + WebView2 for the window).

### Layout
| Path | Purpose |
|---|---|
| `mucify/app.py` | Flask backend: the original pipeline plus first-run, Soulseek test, Qobuz connect endpoints |
| `mucify/main.py` | Desktop launcher (private local server + native pywebview window), `--selftest` for CI |
| `mucify/qobuz_auth.py` | In-app Qobuz login window + token capture (`PROBE_JS`) |
| `mucify/soulseek.py` | Random credentials + direct Soulseek login test |
| `mucify/paths.py` | AppData / Music folders, bundled-tool staging |
| `tools/sldl`, `tools/rsgain` | **Tested** binaries shipped as-is. Never auto-updated; Mucify never downloads tools |
| `mucify.spec`, `build.ps1`, `installer/mucify.iss` | Packaging |
| `tests/` | `python -m unittest discover -s tests -t .` (or `pytest`) |

### Updating the bundled tools (deliberate, manual)
Replace the files under `tools/` yourself after re-testing the pipeline with the new version, then push. Mucify copies `sldl.exe` into `%APPDATA%\Mucify\tools\sldl` on first run (it needs a writable folder for `sldl.conf`) and refreshes that copy when the app version or file size changes.

### If automatic Qobuz detection stops working
Only `PROBE_JS` and `_candidates()` in `mucify/qobuz_auth.py` need changing (where the web player keeps the token), plus `validate_token()` if Qobuz changes the check endpoint. The manual-token path is independent of both. `tests/probe_sim.js` simulates the probe in Node.

### Security notes
- **Never commit `sldl.conf` or any file containing your Soulseek login.** Mucify writes it at runtime to `%APPDATA%`; the repo's `.gitignore` excludes it.
- The local backend only accepts requests from Mucify's own window (Host check + required header).
- Third-party licences: see `THIRD_PARTY.md`.
