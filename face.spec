# -*- mode: python -*-

block_cipher = None


a = Analysis(['face.py'],
             pathex=['E:\\42\\Dev\\QA\\OnT_QA\\OnT_Files'],
             binaries=[],
             datas=[("ReferenceSource_MASTER/*.json", "ReferenceSource"), ("ReferenceSource_MASTER/apple.ico", "ReferenceSource")],
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
          exclude_binaries=True,
          name='OnT',
          debug=False,
          strip=False,
          upx=True,
          console=False, 
          icon='e:\\42\\dev\\qa\\ont_qa\\ont_files\\referencesource_master\\apple.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='OnTrack')
