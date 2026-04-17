[Setup]
AppName=DemoApp
AppVersion=1.0
DefaultDirName={autopf}\DemoApp-Trastevere
DefaultGroupName=DemoApp-Trastevere
OutputDir=.
OutputBaseFilename=DemoAppInstaller
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: ".\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\DemoApp"; Filename: "{app}\run_app.bat"
Name: "{commondesktop}\DemoApp"; Filename: "{app}\run_app.bat"

[Run]
Filename: "{app}\run_app.bat"; Description: "Launch Demo"; Flags: postinstall shellexec nowait
