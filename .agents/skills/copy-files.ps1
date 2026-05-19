# Script para copiar archivos del template a la raíz del repositorio

$templatePath = Join-Path $PSScriptRoot "harness-onboarding\template"
$repoRoot = (Get-Item $PSScriptRoot).Parent.Parent.FullName

Write-Host "Copiando archivos del template a la raíz del repo..." -ForegroundColor Cyan
Write-Host "Template: $templatePath" -ForegroundColor Gray
Write-Host "Destino: $repoRoot" -ForegroundColor Gray

# Copiar todo el contenido del template a la raíz del repo
Get-ChildItem -Path $templatePath -Recurse | ForEach-Object {
    $relativePath = $_.FullName.Substring($templatePath.Length + 1)
    $destinationPath = Join-Path $repoRoot $relativePath

    if ($_.PSIsContainer) {
        # Crear directorio si no existe
        if (-not (Test-Path $destinationPath)) {
            New-Item -ItemType Directory -Path $destinationPath -Force | Out-Null
            Write-Host "  [DIR] $relativePath" -ForegroundColor Green
        }
    } else {
        # Asegurar que el directorio destino existe
        $destDir = Split-Path $destinationPath -Parent
        if (-not (Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        # Copiar archivo
        Copy-Item -Path $_.FullName -Destination $destinationPath -Force
        Write-Host "  [FILE] $relativePath" -ForegroundColor Yellow
    }
}

Write-Host "Copia completada exitosamente." -ForegroundColor Green