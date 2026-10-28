# Mello Kodi Kit

A personal Kodi 21 (Omega) profile kit: skin, menus, widgets, a tuned
streaming addon, favorites, and account links — packaged on the home PC and
installed onto other devices (built for Xbox Series X) by one small installer
addon.

This repository contains **code only** — the installer and its Kodi
repository. The kit data itself never leaves the home network: the installer
downloads it from the PC on the same LAN.

## Install on the target device (Xbox)

1. In Kodi: Settings → File Manager → Add source →
   `https://raw.githubusercontent.com/ianblankg/Mello-kodi-kit/main/repository.mello-1.0.0.zip`
   (name it `mello`).
2. Settings → Add-ons → Install from zip file → `mello` →
   `repository.mello-1.0.0.zip`. The Mello Repository is now installed.
3. Install from repository → Mello Repository → Program add-ons →
   **Mello Kit Installer** → Install.
4. Make sure the home PC is on (it serves the kit file on the LAN).
5. Open the Mello Kit Installer from Program add-ons, confirm, and leave the
   URL as offered. It downloads the kit, replaces the current profile, and
   closes Kodi. Reopen Kodi — it boots into the kit.

## Layout

- `repository.mello-1.0.0.zip` — the Kodi repository addon (installs step 2).
- `zips/` — the repository datadir Kodi reads after that (`addons.xml`,
  checksum, and the installer zip under its addon-id folder).
- `src/` — the plain source of both addons, for reading and rebuilding.
