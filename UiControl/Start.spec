# -*- mode: python -*-

block_cipher = None


a = Analysis(['Start.py'],
             pathex=['E:\\WorkPlace\\PyCham\\DtuTools\\UiControl'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas +=[('.\\Res\\on.png','E:\\WorkPlace\\PyCham\\DtuTools\\Res\\on.png','DATA'),
('.\\Res\\off.png','E:\\WorkPlace\\PyCham\\DtuTools\\Res\\off.png','DATA'),
('.\\Res\\head.jpg','E:\\WorkPlace\\PyCham\\DtuTools\\Res\\head.jpg','DATA'),
('.\\Res\\icon.png','E:\\WorkPlace\\PyCham\\DtuTools\\Res\\icon.png','DATA'),
('.\\Res\\title.png','E:\\WorkPlace\\PyCham\\DtuTools\\Res\\title.png','DATA')]
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Start',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='..\\Res\\icon.ico')
