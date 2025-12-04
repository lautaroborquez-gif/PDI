[Setup]
AppName=Reproductor de Video
AppVersion=1.0
DefaultDirName={autopf}\Reproductor de Video
DefaultGroupName=Reproductor de Video
UninstallDisplayIcon={app}\Reproductor_de_Video.exe
OutputDir=.
OutputBaseFilename=Reproductor_de_Video.exe
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "D:\PDI-proyecto\MiVideoPlayer\dist\Reproductor_de_Video.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Reproductor de Video"; Filename: "{app}\Reproductor_de_Video.exe"
Name: "{commondesktop}\Reproductor de Video"; Filename: "{app}\Reproductor_de_Video.exe"

[Run]
Filename: "{app}\Reproductor_de_Video.exe"; Description: "Ejecutar Reproductor de Video"; Flags: nowait postinstall skipifsilent

