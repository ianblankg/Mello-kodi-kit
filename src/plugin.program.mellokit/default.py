import os
import shutil
import urllib.request
import zipfile

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
DEFAULT_URL = ('https://github.com/ianblankg/Mello-kodi-kit/releases/'
               'download/kit-v1/mello-kit.zip')
LAN_URL = 'http://192.168.1.150:8899/kit.zip'

ENABLE_AFTER = [
    'metadata.album.universal', 'metadata.artists.universal',
    'metadata.common.fanart.tv', 'metadata.generic.albums',
    'metadata.generic.artists', 'metadata.themoviedb.org.python',
    'metadata.tvshows.themoviedb.org.python', 'plugin.video.redlight',
    'plugin.video.themoviedb.helper', 'repository.cocoscrapers',
    'repository.redwizard', 'resource.images.moviecountryicons.maps',
    'resource.images.moviegenreicons.transparent',
    'resource.images.studios.white', 'resource.images.weathericons.white',
    'script.embuary.helper', 'script.embuary.info', 'script.globalsearch',
    'script.image.resource.select', 'script.module.addon.signals',
    'script.module.arrow', 'script.module.beautifulsoup4',
    'script.module.certifi', 'script.module.chardet',
    'script.module.cocoscrapers', 'script.module.dateutil',
    'script.module.dropbox', 'script.module.future', 'script.module.idna',
    'script.module.infotagger', 'script.module.jurialmunkey',
    'script.module.pyqrcode', 'script.module.qrcode',
    'script.module.requests', 'script.module.routing',
    'script.module.simplecache', 'script.module.simpleeval',
    'script.module.six', 'script.module.soupsieve',
    'script.module.typing_extensions', 'script.module.unidecode',
    'script.module.urllib3', 'script.skinhelper', 'script.skinshortcuts',
    'script.skinvariables', 'script.xbmcbackup',
    'skin.arctic.zephyr.2.resurrection.mod', 'skin.arctic.zephyr.mod',
]
DISABLE_AFTER = ['service.xbmc.versioncheck']


def log(msg):
    xbmc.log('MELLOKIT ' + msg, xbmc.LOGINFO)


def rpc(method, params):
    import json
    req = {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}
    return xbmc.executeJSONRPC(json.dumps(req))


def wipe_contents(path, keep=()):
    if not os.path.isdir(path):
        return
    for name in os.listdir(path):
        if name in keep:
            continue
        p = os.path.join(path, name)
        try:
            if os.path.isdir(p) and not os.path.islink(p):
                shutil.rmtree(p, ignore_errors=True)
            else:
                os.remove(p)
        except Exception as exc:
            log('wipe failed %s: %s' % (p, exc))


def main():
    dlg = xbmcgui.Dialog()
    if not dlg.yesno(
            'Mello Kit Installer',
            'This replaces the Kodi profile on this device with the Mello Kit.'
            '[CR]The current build, its addons and settings will be removed.'
            '[CR][CR]Continue?'):
        return
    url = dlg.input(
        'Kit file URL (GitHub by default; for the home-PC kit, use '
        + LAN_URL + ')', DEFAULT_URL)
    if not url:
        return
    home = xbmcvfs.translatePath('special://home/')
    tmp = xbmcvfs.translatePath('special://temp/mello-kit.zip')

    dp = xbmcgui.DialogProgress()
    dp.create('Mello Kit Installer', 'Downloading the kit...')

    def hook(blocks, bsize, total):
        if dp.iscanceled():
            raise Exception('download canceled')
        if total and total > 0:
            pct = min(100, int(blocks * bsize * 100 / total))
            dp.update(pct, 'Downloading the kit... %d%%' % pct)

    try:
        urllib.request.urlretrieve(url, tmp, hook)
    except Exception as exc:
        dp.close()
        dlg.ok('Mello Kit Installer', 'Download failed: %s' % exc)
        return
    dp.update(0, 'Installing...')

    try:
        wipe_contents(os.path.join(home, 'addons'), keep=(ADDON_ID,))
        wipe_contents(os.path.join(home, 'userdata'))
        failures = []
        with zipfile.ZipFile(tmp) as zf:
            infos = zf.infolist()
            total = len(infos)
            for i, info in enumerate(infos):
                parts = [p for p in info.filename.split('/') if p]
                if len(parts) < 3:
                    continue
                top, rest = parts[1], parts[2:]
                # Backup layout: addons/ sits beside the userdata pieces
                # (addon_data/, database/, thumbnails/, config/ = the
                # userdata root files). Map each to its real home.
                if top == 'addons':
                    rel = os.path.join('addons', *rest)
                elif top == 'userdata':
                    rel = os.path.join('userdata', *rest)
                elif top == 'config':
                    rel = os.path.join('userdata', *rest)
                elif top == 'addon_data':
                    rel = os.path.join('userdata', 'addon_data', *rest)
                elif top == 'database':
                    rel = os.path.join('userdata', 'Database', *rest)
                elif top == 'thumbnails':
                    rel = os.path.join('userdata', 'Thumbnails', *rest)
                else:
                    continue
                target = os.path.join(home, rel)
                if info.is_dir():
                    os.makedirs(target, exist_ok=True)
                    continue
                os.makedirs(os.path.dirname(target), exist_ok=True)
                try:
                    with zf.open(info) as src, open(target, 'wb') as dst:
                        shutil.copyfileobj(src, dst, 1024 * 256)
                except Exception as exc:
                    failures.append('%s (%s)' % (rel, exc))
                if i % 25 == 0:
                    dp.update(int(i * 100 / max(1, total)),
                              'Installing... %d/%d files' % (i, total))
        dp.close()
        log('extract done, failures: %d' % len(failures))
    except Exception as exc:
        dp.close()
        dlg.ok('Mello Kit Installer', 'Install failed: %s' % exc)
        return

    xbmc.executebuiltin('UpdateLocalAddons')
    xbmc.sleep(3000)
    for addon_id in ENABLE_AFTER:
        rpc('Addons.SetAddonEnabled', {'addonid': addon_id, 'enabled': True})
    for addon_id in DISABLE_AFTER:
        rpc('Addons.SetAddonEnabled', {'addonid': addon_id, 'enabled': False})

    msg = ('Kit installed. Kodi will close now - reopen it to boot '
           'into the kit.')
    if 'github' in url.lower():
        msg += ('[CR][CR]The GitHub kit carries no account links. After '
                'reboot, open Red Light -> Settings and re-link '
                'Premiumize and Trakt.')
    if failures:
        msg += '[CR][CR]%d files could not be written (first: %s)' % (
            len(failures), failures[0])
    dlg.ok('Mello Kit Installer', msg)
    os._exit(1)


main()
