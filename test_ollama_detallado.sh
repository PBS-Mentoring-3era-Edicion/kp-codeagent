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
TOTAL_MEM=$(free -g | awk '/^Mem:/{print $2}')
echo "   RAM total: ${TOTAL_MEM}GB"
echo "   RAM libre: ${FREE_MEM}GB"
if [ "$FREE_MEM" -lt 2 ]; then
    echo "   ⚠️  ADVERTENCIA: Poca memoria libre (necesitas 2-4GB)"
fi
echo ""

# Test 5
echo "5️⃣ Probando generación simple con CLI (timeout 30s)..."
echo "   Modelo: phi:latest"
echo "   Prompt: 'Say hi'"
START=$(date +%s)
timeout 30 ollama run phi:latest "Say hi" > /tmp/ollama_test.txt 2>&1
EXIT_CODE=$?
END=$(date +%s)
DURATION=$((END - START))

if [ $EXIT_CODE -eq 0 ]; then
    echo "   ✅ Respuesta recibida en ${DURATION}s"
    echo "   📝 Respuesta: $(cat /tmp/ollama_test.txt | head -3)"
elif [ $EXIT_CODE -eq 124 ]; then
    echo "   ⏱️  TIMEOUT después de 30s"
    echo "   ❌ El modelo está demasiado lento"
else
    echo "   ❌ Error (code: $EXIT_CODE)"
fi
echo ""

# Test 6
echo "6️⃣ Probando API directamente (timeout 40s)..."
echo "   Usando stream=false para respuesta completa"
START=$(date +%s)
timeout 40 curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "phi:latest", "prompt": "Hi", "stream": false}' \
  > /tmp/ollama_api_test.txt 2>&1
API_EXIT_CODE=$?
END=$(date +%s)
API_DURATION=$((END - START))

if [ $API_EXIT_CODE -eq 0 ]; then
    echo "   ✅ API respondió en ${API_DURATION}s"
    RESPONSE=$(cat /tmp/ollama_api_test.txt | python3 -c "import sys, json; print(json.load(sys.stdin).get('response', 'N/A')[:50])" 2>/dev/null)
    echo "   📝 Respuesta: $RESPONSE..."
elif [ $API_EXIT_CODE -eq 124 ]; then
    echo "   ⏱️  TIMEOUT después de 40s"
    echo "   ❌ API está demasiado lenta"
else
    echo "   ❌ Error en API (code: $API_EXIT_CODE)"
    echo "   📄 Detalles: $(cat /tmp/ollama_api_test.txt | head -5)"
fi
echo ""

# Test 7
echo "7️⃣ Verificando uso de CPU/RAM de Ollama..."
OLLAMA_PID=$(pgrep ollama | head -1)
if [ -n "$OLLAMA_PID" ]; then
    ps -p $OLLAMA_PID -o pid,ppid,%cpu,%mem,cmd | tail -1
fi
echo ""

# Resumen
echo "=================================="
echo "📊 RESUMEN DEL DIAGNÓSTICO"
echo "=================================="
echo ""

OVERALL_SUCCESS=0

if [ $API_EXIT_CODE -eq 0 ] && [ $API_DURATION -lt 15 ]; then
    echo "✅ TODO FUNCIONA PERFECTAMENTE"
    echo "   - API responde en ${API_DURATION}s (< 15s)"
    echo "   - kp-codeagent debería funcionar sin problemas"
    OVERALL_SUCCESS=1
elif [ $API_EXIT_CODE -eq 0 ] && [ $API_DURATION -lt 45 ]; then
    echo "⚠️  FUNCIONA PERO LENTO"
    echo "   - API responde en ${API_DURATION}s (lento pero usable)"
    echo "   - kp-codeagent funcionará pero tardará"
    echo ""
    echo "   💡 Para mejorar velocidad:"
    echo "   - Cierra otros programas para liberar RAM"
    echo "   - Usa modelo más pequeño: ollama pull tinyllama"
    OVERALL_SUCCESS=1
elif [ $API_EXIT_CODE -eq 124 ]; then
    echo "❌ TIMEOUT - DEMASIADO LENTO"
    echo "   - API no respondió en 40 segundos"
    echo "   - kp-codeagent NO funcionará correctamente"
    echo ""
    echo "   🔍 Causas probables:"
    echo "   1. Poca RAM disponible (tienes ${FREE_MEM}GB libre)"
    echo "   2. CPU lenta o sobrecargada"
    echo "   3. Modelo demasiado grande para tu hardware"
    echo ""
    echo "   💡 Soluciones:"
    echo "   1. Reinicia Ollama: sudo systemctl restart ollama"
    echo "   2. Cierra navegadores y programas pesados"
    echo "   3. Intenta modelo tiny: ollama pull tinyllama"
    echo "   4. Usa modo demo: python3 demo_sin_ia.py"
else
    echo "❌ ERROR EN LA CONEXIÓN"
    echo "   - Revisa los errores arriba"
    echo "   - Puede que Ollama necesite reiniciarse"
fi

echo ""
echo "=================================="
echo ""

# Sugerencia final
if [ $OVERALL_SUCCESS -eq 1 ]; then
    echo "🎉 Puedes intentar kp-codeagent ahora:"
    echo "   cd kp-codeagent"
    echo "   kp-codeagent --model phi:latest run \"crea hola.py\""
else
    echo "🛠️  Necesitas arreglar los problemas primero"
    echo "   Lee las sugerencias arriba"
    echo ""
    echo "   O usa el modo demo mientras tanto:"
    echo "   python3 demo_sin_ia.py"
fi

# Cleanup
rm -f /tmp/ollama_test.txt /tmp/ollama_api_test.txt

exit 0
