# -*- mode: python -*-

block_cipher = None


a = Analysis(['installer.py'],
             pathex=['PATH\\TO\\INSTALLER\\FILES'],
             binaries=[],
             datas=[("OnTrack_zipped.zip", ".")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='OnTrack_Installer',
          debug=False,
          strip=False,
          upx=True,
          console=False, 
          icon='PATH\\TO\\APPLE\\ICON\\apple.ico')
