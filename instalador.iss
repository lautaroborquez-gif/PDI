[Setup]
AppName=Reproductor de Video
AppVersion=1.0
DefaultDirName={autopf}\Reproductor de Video
DefaultGroupName=Reproductor de Video
UninstallDisplayIcon={app}\app.exe
OutputDir=.
OutputBaseFilename=Instalador_ReproductorVideo
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "D:\PDI-proyecto\MiVideoPlayer\dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Reproductor de Video"; Filename: "{app}\app.exe"
Name: "{commondesktop}\Reproductor de Video"; Filename: "{app}\app.exe"

[Run]
Filename: "{app}\app.exe"; Description: "Ejecutar Reproductor de Video"; Flags: nowait postinstall skipifsilent
