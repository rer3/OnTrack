# -*- mode: python -*-

block_cipher = None


a = Analysis(['e:\\42\\dev\\qa\\ont_installer\\installer.py'],
             pathex=['E:\\42\\Dev\\QA\\OnT_Installer'],
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
          icon='e:\\42\\dev\\qa\\ont_installer\\apple.ico')
