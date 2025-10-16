# 🔍 Diagnóstico de Ollama - Guía Paso a Paso

## Paso 1: Verificar que Ollama esté instalado y corriendo

```bash
# Ver si el proceso está activo
ps aux | grep ollama | grep -v grep

# Ver versión de Ollama
ollama --version

# Ver estado del servicio
curl http://localhost:11434/api/version
```

**✅ Esperado:** Deberías ver el proceso corriendo y una versión como `{"version":"0.x.x"}`

---

## Paso 2: Ver qué modelos tienes disponibles

```bash
# Listar modelos instalados
ollama list

# O usando la API
curl http://localhost:11434/api/tags
```

**✅ Esperado:** Deberías ver `codellama:7b` y `phi:latest` en la lista

---

## Paso 3: Prueba simple con el CLI de Ollama

```bash
# Prueba interactiva con phi (modelo pequeño y rápido)
ollama run phi:latest "Di hola en una palabra"
```

**⏱️ Tiempo esperado:** 3-15 segundos
**❌ Si tarda más de 30 segundos:** Hay un problema de recursos

---

## Paso 4: Prueba con la API directamente (sin streaming)

```bash
# Prueba simple sin streaming
time curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "phi:latest",
    "prompt": "Say hello",
    "stream": false
  }'
```

**⏱️ Tiempo esperado:** 5-20 segundos
**✅ Esperado:** Deberías recibir un JSON con la respuesta

---

## Paso 5: Prueba con streaming (como usa kp-codeagent)

```bash
# Con streaming para ver respuesta en tiempo real
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "phi:latest",
    "prompt": "Count to 3",
    "stream": true
  }'
```

**✅ Esperado:** Deberías ver múltiples líneas JSON apareciendo progresivamente

---

## Paso 6: Revisar logs de Ollama

```bash
# Ver logs si Ollama corre como servicio
sudo journalctl -u ollama -f

# O si lo iniciaste manualmente, verifica la terminal donde corre
```

**🔍 Busca:** Mensajes de error, warnings sobre memoria, o "loading model"

---

## Paso 7: Verificar uso de recursos

```bash
# Ver uso de RAM y CPU mientras Ollama trabaja
top -p $(pgrep ollama)

# O más detallado
htop -p $(pgrep ollama)

# Ver memoria disponible
free -h
```

**⚠️ Problema común:**
- `phi:latest` necesita ~2-3 GB de RAM
- `codellama:7b` necesita ~4-6 GB de RAM
- Si tienes menos RAM libre, el sistema usará swap (muy lento)

---

## Paso 8: Probar descargar modelo más pequeño

```bash
# Tiny model para testing (solo ~600MB)
ollama pull tinyllama

# Probar con él
ollama run tinyllama "Hello"
```

**⏱️ Si tinyllama responde rápido:** El problema es falta de RAM para modelos grandes

---

## Paso 9: Reiniciar Ollama limpiamente

```bash
# Detener Ollama
sudo systemctl stop ollama
# O si corre manualmente:
pkill ollama

# Esperar 5 segundos
sleep 5

# Iniciar de nuevo
sudo systemctl start ollama
# O manualmente:
ollama serve

# Esperar 10 segundos a que inicie
sleep 10

# Probar de nuevo
ollama run phi:latest "test"
```

---

## Paso 10: Script automático de diagnóstico

Guarda este script como `test_ollama_detallado.sh`:

```bash
#!/bin/bash

echo "=================================="
echo "🔍 DIAGNÓSTICO COMPLETO DE OLLAMA"
echo "=================================="
echo ""

# Test 1
echo "1️⃣ Verificando proceso Ollama..."
if pgrep -x ollama > /dev/null; then
    echo "   ✅ Ollama está corriendo (PID: $(pgrep ollama))"
else
    echo "   ❌ Ollama NO está corriendo"
    exit 1
fi
echo ""

# Test 2
echo "2️⃣ Verificando API..."
if curl -s http://localhost:11434/api/version > /dev/null; then
    VERSION=$(curl -s http://localhost:11434/api/version | grep -o '"version":"[^"]*"')
    echo "   ✅ API responde: $VERSION"
else
    echo "   ❌ API no responde"
    exit 1
fi
echo ""

# Test 3
echo "3️⃣ Listando modelos..."
ollama list
echo ""

# Test 4
echo "4️⃣ Verificando memoria disponible..."
FREE_MEM=$(free -g | awk '/^Mem:/{print $7}')
echo "   RAM libre: ${FREE_MEM}GB"
if [ "$FREE_MEM" -lt 2 ]; then
    echo "   ⚠️  ADVERTENCIA: Poca memoria libre (necesitas 2-4GB)"
fi
echo ""

# Test 5
echo "5️⃣ Probando generación simple (timeout 30s)..."
echo "   Prompt: 'Say hi'"
START=$(date +%s)
timeout 30 ollama run phi:latest "Say hi" > /tmp/ollama_test.txt 2>&1
EXIT_CODE=$?
END=$(date +%s)
DURATION=$((END - START))

if [ $EXIT_CODE -eq 0 ]; then
    echo "   ✅ Respuesta recibida en ${DURATION}s"
    echo "   📝 Respuesta: $(cat /tmp/ollama_test.txt)"
elif [ $EXIT_CODE -eq 124 ]; then
    echo "   ⏱️  TIMEOUT después de 30s"
    echo "   ❌ El modelo está demasiado lento"
else
    echo "   ❌ Error (code: $EXIT_CODE)"
fi
echo ""

# Test 6
echo "6️⃣ Probando API con timeout..."
START=$(date +%s)
timeout 30 curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "phi:latest", "prompt": "Hi", "stream": false}' \
  > /tmp/ollama_api_test.txt 2>&1
EXIT_CODE=$?
END=$(date +%s)
DURATION=$((END - START))

if [ $EXIT_CODE -eq 0 ]; then
    echo "   ✅ API respondió en ${DURATION}s"
    RESPONSE=$(cat /tmp/ollama_api_test.txt | grep -o '"response":"[^"]*"' | head -1)
    echo "   📝 Respuesta: $RESPONSE"
elif [ $EXIT_CODE -eq 124 ]; then
    echo "   ⏱️  TIMEOUT después de 30s"
    echo "   ❌ API está demasiado lenta"
else
    echo "   ❌ Error en API (code: $EXIT_CODE)"
fi
echo ""

# Resumen
echo "=================================="
echo "📊 RESUMEN"
echo "=================================="
if [ $EXIT_CODE -eq 0 ] && [ $DURATION -lt 15 ]; then
    echo "✅ TODO BIEN - Ollama funciona correctamente"
    echo "   El problema puede estar en kp-codeagent"
elif [ $EXIT_CODE -eq 124 ] || [ $DURATION -gt 20 ]; then
    echo "⚠️  RENDIMIENTO BAJO"
    echo "   Causas posibles:"
    echo "   - Poca RAM disponible"
    echo "   - CPU lenta"
    echo "   - Modelo muy grande para tu hardware"
    echo ""
    echo "   💡 Soluciones:"
    echo "   - Cierra otros programas"
    echo "   - Usa 'tinyllama' en lugar de phi"
    echo "   - Aumenta RAM del sistema"
else
    echo "❌ HAY ERRORES - Revisa los logs arriba"
fi
echo "=================================="

# Cleanup
rm -f /tmp/ollama_test.txt /tmp/ollama_api_test.txt
```

**Para ejecutar:**
```bash
chmod +x test_ollama_detallado.sh
./test_ollama_detallado.sh
```

---

## 🔧 Soluciones Comunes

### Problema: "Timeout después de 30s"
**Causa:** Falta de RAM o CPU lenta
**Solución:**
1. Cierra navegadores y otros programas
2. Reinicia Ollama: `sudo systemctl restart ollama`
3. Prueba modelo más pequeño: `ollama pull tinyllama`

### Problema: "Model not found"
**Solución:**
```bash
ollama pull phi:latest
# Espera a que termine (puede tardar varios minutos)
ollama list  # Verifica que aparezca
```

### Problema: "Connection refused"
**Causa:** Ollama no está corriendo
**Solución:**
```bash
# Si está instalado como servicio
sudo systemctl start ollama

# Si no, inícialo manualmente en otra terminal
ollama serve
```

### Problema: Uso excesivo de memoria
**Solución:**
```bash
# Descargar modelo más pequeño
ollama pull tinyllama

# Usar en kp-codeagent:
kp-codeagent --model tinyllama run "tu tarea"
```

---

## 📊 Tabla de Requisitos por Modelo

| Modelo | Tamaño | RAM Necesaria | Velocidad | Calidad Código |
|--------|--------|---------------|-----------|----------------|
| tinyllama | 600MB | 1-2 GB | ⚡⚡⚡ Rápido | ⭐⭐ Básica |
| phi:latest | 1.6GB | 2-3 GB | ⚡⚡ Medio | ⭐⭐⭐ Buena |
| codellama:7b | 3.8GB | 4-6 GB | ⚡ Lento | ⭐⭐⭐⭐ Excelente |
| codellama:13b | 7.4GB | 8-12 GB | 🐌 Muy lento | ⭐⭐⭐⭐⭐ Profesional |

---

## ✅ Checklist Final

- [ ] Ollama está corriendo
- [ ] API responde en menos de 5 segundos
- [ ] Modelo responde en menos de 30 segundos
- [ ] Tienes al menos 3GB de RAM libre
- [ ] No hay errores en los logs

Si todos están ✅, entonces kp-codeagent debería funcionar.
Si alguno falla ❌, ese es tu problema.

---

## 🆘 Si Nada Funciona

**Opción 1: Usar modo demo**
```bash
python3 demo_sin_ia.py  # Ya lo creamos antes
```

**Opción 2: Documentar el problema**
Para tu portafolio, puedes documentar:
- El problema encontrado
- Los pasos de diagnóstico
- Las soluciones intentadas
- Alternativas implementadas (modo demo)

Esto demuestra **habilidades de debugging** y **resolución de problemas reales**.
