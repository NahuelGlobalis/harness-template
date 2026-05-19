# Find virtual environment python executable
$venvPath = ""
if (Test-Path ".venv\Scripts\python.exe") {
    $venvPath = ".venv\Scripts\python.exe"
} elseif (Test-Path "venv\Scripts\python.exe") {
    $venvPath = "venv\Scripts\python.exe"
}

if ($venvPath -ne "") {
    & $venvPath scripts/validate_harness.py $args
} else {
    python scripts/validate_harness.py $args
}
exit $LASTEXITCODE
