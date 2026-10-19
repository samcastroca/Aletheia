# Comandos de ManimGX por video. Uso:
#   ./scripts/mgx.ps1 <inspect|draft|final|present> <video> [-Scene X] [-Time "1.5,end"] [-AllowVoiceSpend]
# Mensajes en ASCII: PowerShell 5.1 lee los .ps1 sin BOM como ANSI.
param(
    [Parameter(Mandatory, Position = 0)]
    [ValidateSet('inspect', 'draft', 'final', 'present')]
    [string]$Action,

    [Parameter(Mandatory, Position = 1)]
    [string]$Video,

    [string]$Scene,
    [string]$Time,
    [switch]$AllowVoiceSpend
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$dir = Join-Path $root "videos\$Video"
$file = Join-Path $dir 'scene.py'
if (-not (Test-Path $file)) { throw "No existe $file" }

# Proteccion de coste: con self.say, cualquier comando (inspect incluido) sintetiza
# la voz que falte en voice/ con fal.ai, de pago. Solo detecta la cache vacia:
# una frase nueva o cambiada tambien se cobra.
$speaks = Select-String -Path $file -Pattern 'self\.say\(' -Quiet
$cached = Test-Path (Join-Path $dir 'voice\*.json')
if ($speaks -and -not $cached -and -not $AllowVoiceSpend) {
    throw "La escena usa self.say y voice/ esta vacia: llamaria a fal.ai (de pago). Repite con -AllowVoiceSpend si lo quieres."
}

$verb = if ($Action -in 'draft', 'final') { 'render' } else { $Action }
$cmd = @($verb, $file)
if ($Scene) { $cmd += $Scene }
switch ($Action) {
    'draft' { $cmd += @('-r', '1280x720', '--fps', '30', '-o', (Join-Path $dir 'draft.mp4')) }
}
if ($Time) {
    if ($Action -ne 'inspect') { throw "-Time solo vale para inspect" }
    $cmd += @('-t', $Time)
}

$start = Get-Date
& uv run --project $root manimgx @cmd
$code = $LASTEXITCODE

if ($Action -in 'draft', 'final' -and $code -eq 0) {
    $mp4 = Get-ChildItem $dir -Filter *.mp4 | Where-Object LastWriteTime -ge $start |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($mp4) {
        Write-Host "Video: $($mp4.FullName)"
        Invoke-Item $mp4.FullName
    }
}
exit $code
