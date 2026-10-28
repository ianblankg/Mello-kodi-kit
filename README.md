# Mello Kodi Kit

A personal Kodi 21 (Omega) profile kit: skin, menus, widgets, a tuned
streaming addon, and favorites — packaged on the home PC and installed
onto other devices (built for Xbox Series X) by one small installer
addon.

The installer downloads the kit from this repo's **kit-v1 release**
by default. That published kit is the full setup with one deliberate
difference: it carries **no account links** — the Premiumize and Trakt
tokens were stripped before publishing, so after installing from
GitHub you re-link those two accounts once, in Red Light's settings.
The home PC also serves the original kit (accounts already linked)
on the LAN for installs at home.

## Install on the target device (Xbox)

1. In Kodi: Settings → File Manager → Add source →
   `https://raw.githubusercontent.com/ianblankg/Mello-kodi-kit/main/repository.mello-1.0.0.zip`
   (name it `mello`).
2. Settings → Add-ons → Install from zip file → `mello` →
   `repository.mello-1.0.0.zip`. The Mello Repository is now installed.
3. Install from repository → Mello Repository → Program add-ons →
   **Mello Kit Installer** → Install.
4. Open the Mello Kit Installer from Program add-ons, confirm, and leave
   the URL as offered (the GitHub kit). It downloads the kit, replaces
   the current profile, and closes Kodi. Reopen Kodi — it boots into
   the kit.
5. **Re-link your accounts:** open Red Light → Settings and sign in to
   Premiumize and Trakt. Everything else — skin, menus, widgets,
   favorites, addon settings — is already in place.

At home you can instead point the installer's URL at the PC's kit
(`http://192.168.1.150:8899/kit.zip`, PC must be on); that copy keeps
the account links, so step 5 is unnecessary.

## Layout

- `repository.mello-1.0.0.zip` — the Kodi repository addon (installs step 2).
- `zips/` — the repository datadir Kodi reads after that (`addons.xml`,
  checksum, and the installer zip under its addon-id folder).
- `src/` — the plain source of both addons, for reading and rebuilding.
- Release `kit-v1` — `mello-kit.zip`, the token-stripped kit the
  installer downloads by default.
