## build_scripts/build.py
import os
import PyInstaller.__main__

def build_exe():
    PyInstaller.__main__.run([
        '../src/youtube_music_app.py',
        '--name=YouTube Music',
        '--icon=../assets/icon.ico',
        '--noconsole',
        '--onefile',
        '--add-data=../assets/icon.ico;assets',
        '--windowed',
        '--version-file=version_info.txt',
        '--uac-admin',
        '--clean',
        '--noupx'
    ])

if __name__ == "__main__":
    version_info = '''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Votre Nom'),
        StringStruct(u'FileDescription', u'YouTube Music Desktop App'),
        StringStruct(u'FileVersion', u'1.0.0'),
        StringStruct(u'InternalName', u'youtube_music'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2025'),
        StringStruct(u'OriginalFilename', u'YouTube Music.exe'),
        StringStruct(u'ProductName', u'YouTube Music Desktop'),
        StringStruct(u'ProductVersion', u'1.0.0')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    with open('version_info.txt', 'w') as f:
        f.write(version_info)
        
    build_exe()
