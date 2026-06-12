Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

npx skills add OthmanAdi/planning-with-files --skill planning-with-files
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
