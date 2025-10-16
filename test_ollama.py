#!/usr/bin/env python3
"""Script rápido para probar Ollama directamente."""

import requests
import time
import sys

def test_ollama():
    print("🔍 Probando conexión con Ollama...\n")

    # Test 1: ¿Está corriendo?
    print("1. Verificando que Ollama esté corriendo...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("   ✅ Ollama está corriendo")
            models = response.json().get('models', [])
            print(f"   📦 Modelos disponibles: {[m['name'] for m in models]}")
        else:
            print(f"   ❌ Error: status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

    # Test 2: Prueba simple con phi (más rápido)
    print("\n2. Probando generación con phi:latest (modelo pequeño)...")
    print("   ⏳ Esperando respuesta (máximo 60 segundos)...\n")

    start_time = time.time()
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi:latest",
                "prompt": "Di 'hola' en una palabra",
                "stream": False
            },
            timeout=60
        )

        elapsed = time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Respuesta recibida en {elapsed:.1f} segundos")
            print(f"   💬 Respuesta: {result.get('response', 'N/A')[:100]}")
            return True
        else:
            print(f"   ❌ Error: status {response.status_code}")
            return False

    except requests.exceptions.Timeout:
        elapsed = time.time() - start_time
        print(f"   ⏱️  TIMEOUT después de {elapsed:.1f} segundos")
        print("\n💡 Sugerencias:")
        print("   - Tu sistema puede estar lento o con poca RAM")
        print("   - Intenta cerrar otros programas")
        print("   - Considera usar un modelo aún más pequeño")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  Test de Diagnóstico de Ollama")
    print("=" * 60 + "\n")

    success = test_ollama()

    print("\n" + "=" * 60)
    if success:
        print("✅ TODO FUNCIONA - Puedes usar kp-codeagent")
    else:
        print("❌ HAY PROBLEMAS - Revisa los errores arriba")
    print("=" * 60)

    sys.exit(0 if success else 1)
