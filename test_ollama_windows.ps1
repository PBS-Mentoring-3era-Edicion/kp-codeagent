# Script de Verificación de Ollama para Windows
# Ejecutar en PowerShell: .\test_ollama_windows.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VERIFICACIÓN DE OLLAMA EN WINDOWS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allPassed = $true

# Test 1: Ollama instalado
Write-Host "1. Verificando instalación de Ollama..." -ForegroundColor Yellow
try {
    $version = ollama --version 2>&1
    if ($version -match "ollama version") {
        Write-Host "   ✓ Ollama instalado: $version" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Ollama no encontrado" -ForegroundColor Red
        Write-Host "   Descarga desde: https://ollama.com/download" -ForegroundColor Yellow
        $allPassed = $false
    }
} catch {
    Write-Host "   ✗ Ollama no está instalado" -ForegroundColor Red
    Write-Host "   Descarga desde: https://ollama.com/download" -ForegroundColor Yellow
    $allPassed = $false
}
Write-Host ""

# Test 2: Servicio corriendo
Write-Host "2. Verificando servicio de Ollama..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/version" -TimeoutSec 3
    Write-Host "   ✓ Servicio activo - Versión: $($response.version)" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Servicio no responde" -ForegroundColor Red
    Write-Host "   Solución: Busca 'Ollama' en el menú inicio y ejecútalo" -ForegroundColor Yellow
    Write-Host "   O ejecuta: ollama serve" -ForegroundColor Yellow
    $allPassed = $false
}
Write-Host ""

# Test 3: Modelos disponibles
Write-Host "3. Listando modelos instalados..." -ForegroundColor Yellow
try {
    $models = ollama list 2>&1
    Write-Host $models

    if ($models -match "phi") {
        Write-Host "   ✓ Modelo 'phi' encontrado" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ Modelo 'phi' no encontrado" -ForegroundColor Yellow
        Write-Host "   Ejecuta: ollama pull phi" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ✗ Error listando modelos" -ForegroundColor Red
    $allPassed = $false
}
Write-Host ""

# Test 4: Memoria disponible
Write-Host "4. Verificando memoria del sistema..." -ForegroundColor Yellow
$os = Get-CimInstance Win32_OperatingSystem
$freeGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
$totalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
Write-Host "   RAM Total: $totalGB GB" -ForegroundColor Cyan
Write-Host "   RAM Libre: $freeGB GB" -ForegroundColor Cyan

if ($freeGB -lt 2) {
    Write-Host "   ⚠ Advertencia: Poca memoria disponible (mínimo 2 GB)" -ForegroundColor Yellow
} else {
    Write-Host "   ✓ Memoria suficiente" -ForegroundColor Green
}
Write-Host ""

# Test 5: Prueba de generación (solo si servicio funciona)
Write-Host "5. Probando generación con phi (timeout 30s)..." -ForegroundColor Yellow
Write-Host "   Enviando prompt: 'Say hi'" -ForegroundColor Cyan

try {
    $startTime = Get-Date

    # Crear job para ejecutar con timeout
    $job = Start-Job -ScriptBlock {
        ollama run phi "Say hi" 2>&1
    }

    # Esperar máximo 30 segundos
    $completed = Wait-Job -Job $job -Timeout 30

    if ($completed) {
        $result = Receive-Job -Job $job
        $endTime = Get-Date
        $duration = ($endTime - $startTime).TotalSeconds

        Write-Host "   ✓ Respuesta recibida en $([math]::Round($duration, 1))s" -ForegroundColor Green
        Write-Host "   Respuesta: $($result -join ' ')" -ForegroundColor Cyan

        if ($duration -gt 20) {
            Write-Host "   ⚠ Respuesta lenta (>20s)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ⏱ TIMEOUT después de 30s" -ForegroundColor Red
        Write-Host "   El modelo está demasiado lento" -ForegroundColor Red
        $allPassed = $false
        Stop-Job -Job $job
    }

    Remove-Job -Job $job -Force

} catch {
    Write-Host "   ✗ Error en la prueba: $_" -ForegroundColor Red
    $allPassed = $false
}
Write-Host ""

# Resumen
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RESUMEN" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($allPassed) {
    Write-Host "✓ TODO FUNCIONA CORRECTAMENTE" -ForegroundColor Green
    Write-Host ""
    Write-Host "Puedes usar kp-codeagent ahora:" -ForegroundColor Cyan
    Write-Host "  cd kp-codeagent" -ForegroundColor White
    Write-Host "  kp-codeagent check" -ForegroundColor White
    Write-Host "  kp-codeagent --model phi run 'create hello.py'" -ForegroundColor White
} else {
    Write-Host "✗ HAY PROBLEMAS" -ForegroundColor Red
    Write-Host ""
    Write-Host "Pasos para solucionar:" -ForegroundColor Yellow
    Write-Host "  1. Instala Ollama desde: https://ollama.com/download" -ForegroundColor White
    Write-Host "  2. Ejecuta 'ollama serve' en otra PowerShell" -ForegroundColor White
    Write-Host "  3. Ejecuta 'ollama pull phi' para descargar el modelo" -ForegroundColor White
    Write-Host "  4. Vuelve a ejecutar este script" -ForegroundColor White
    Write-Host ""
    Write-Host "Si persiste, revisa logs en:" -ForegroundColor Yellow
    Write-Host "  $env:LOCALAPPDATA\Ollama\logs" -ForegroundColor White
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
