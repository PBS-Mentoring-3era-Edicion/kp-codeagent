#!/bin/bash

# Script de prueba rápida de Groq con tu API key

echo "======================================="
echo "🧪 TEST RÁPIDO DE GROQ"
echo "======================================="
echo ""

# Pedir API key si no está configurada
if [ -z "$GROQ_API_KEY" ]; then
    echo "📝 Ingresa tu GROQ_API_KEY:"
    echo "(Obtén una gratis en: https://console.groq.com/keys)"
    echo ""
    read -p "API Key: " GROQ_API_KEY
    export GROQ_API_KEY
    echo ""
fi

echo "✅ API Key configurada: ${GROQ_API_KEY:0:10}...${GROQ_API_KEY: -4}"
echo ""

# Probar con curl directo
echo "🔌 Probando conexión directa con Groq..."
echo ""

RESPONSE=$(curl -s -X POST https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.1-70b-versatile",
    "messages": [{"role": "user", "content": "Say hello in one word"}],
    "temperature": 0.7,
    "max_tokens": 50
  }')

# Verificar si hay error
if echo "$RESPONSE" | grep -q "error"; then
    echo "❌ Error en la respuesta:"
    echo "$RESPONSE" | jq '.error'
    echo ""
    echo "💡 Verifica:"
    echo "   1. Que la API key sea correcta"
    echo "   2. Que tengas conexión a internet"
    echo "   3. Que la API key esté activa en console.groq.com"
    exit 1
fi

# Extraer y mostrar respuesta
ANSWER=$(echo "$RESPONSE" | jq -r '.choices[0].message.content')
echo "✅ Respuesta de Groq: $ANSWER"
echo ""

# Calcular tiempo aproximado
USAGE=$(echo "$RESPONSE" | jq '.usage')
echo "📊 Estadísticas:"
echo "$USAGE" | jq '.'
echo ""

echo "======================================="
echo "✅ GROQ FUNCIONA CORRECTAMENTE"
echo "======================================="
echo ""
echo "💡 Ahora puedes usar kp-codeagent:"
echo ""
echo "   export GROQ_API_KEY=\"$GROQ_API_KEY\""
echo "   cd kp-codeagent"
echo "   kp-codeagent --backend groq run \"create fibonacci function\""
echo ""
