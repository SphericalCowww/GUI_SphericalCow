# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['desktopPetExe.py'],
             pathex=['/Users/tinglin/Documents/Proj/desktopPet/packageEnv'],
             binaries=[],
             datas=[('figures/cowDownLeft.gif', 'figures'), ('figures/cowDownRight.gif', 'figures'),
                    ('figures/cowDownMunchLeft.gif', 'figures'), ('figures/cowDownMunchRight.gif', 'figures'),
                    ('figures/cowFloatLeft.gif', 'figures'), ('figures/cowFloatRight.gif', 'figures'),
                    ('figures/cowIdleLeft.gif', 'figures'), ('figures/cowIdleRight.gif', 'figures'),
                    ('figures/cowMoo1Left.gif', 'figures'), ('figures/cowMoo1Right.gif', 'figures'),
                    ('figures/cowMoo2Left.gif', 'figures'), ('figures/cowMoo2Right.gif', 'figures'),
                    ('figures/cowUpLeft.gif', 'figures'), ('figures/cowUpRight.gif', 'figures'),
                    ('figures/cowUpMunchLeft.gif', 'figures'), ('figures/cowUpMunchRight.gif', 'figures'),
                    ('figures/cowWalkLeft.gif', 'figures'), ('figures/cowWalkRight.gif', 'figures'),
                    ('figures/cowZDisappearingLeft.gif', 'figures'), ('figures/cowZDisappearingRight.gif', 'figures'),
                    ('figures/cowZRotatingLeft.gif', 'figures'), ('figures/cowZRotatingRight.gif', 'figures')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='SphericalCow',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='cowAIcon.icns')
app = BUNDLE(exe,
             name='SphericalCow.app',
             icon='cowAIcon.icns',
             bundle_identifier=None)
