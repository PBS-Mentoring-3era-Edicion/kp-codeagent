#!/usr/bin/env python3
"""Script de prueba para verificar que Groq funcione correctamente."""

import os
import sys
import time

def test_groq_basic():
    """Prueba básica de conectividad con Groq."""
    print("=" * 70)
    print("🧪 TEST DE GROQ - KP Code Agent")
    print("=" * 70)
    print()

    # Verificar que tenemos la API key
    print("1️⃣ Verificando configuración...")
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("   ❌ GROQ_API_KEY no está configurada")
        print()
        print("💡 Para configurarla:")
        print("   1. Visita: https://console.groq.com/keys")
        print("   2. Crea una cuenta (gratis)")
        print("   3. Genera una API key")
        print("   4. Ejecuta: export GROQ_API_KEY='tu_key_aqui'")
        print()
        return False

    print(f"   ✅ API key encontrada: {api_key[:10]}...{api_key[-4:]}")
    print()

    # Verificar que groq esté instalado
    print("2️⃣ Verificando instalación de groq...")
    try:
        from groq import Groq
        print("   ✅ Librería groq instalada correctamente")
    except ImportError:
        print("   ❌ Librería groq no instalada")
        print()
        print("💡 Para instalarla:")
        print("   pip install groq")
        print()
        return False
    print()

    # Probar conexión
    print("3️⃣ Probando conexión con Groq...")
    try:
        client = Groq(api_key=api_key)
        print("   ✅ Cliente creado correctamente")
    except Exception as e:
        print(f"   ❌ Error al crear cliente: {e}")
        return False
    print()

    # Probar generación simple
    print("4️⃣ Probando generación de texto...")
    print("   Prompt: 'Say hello in one word'")
    print("   ⏳ Esperando respuesta...\n")

    start_time = time.time()

    try:
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say hello in one word"}],
            temperature=0.7,
            max_tokens=50,
            stream=True
        )

        print("   📝 Respuesta: ", end="", flush=True)
        response_started = False
        full_response = ""

        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content

                if not response_started:
                    first_token_time = time.time() - start_time
                    response_started = True

        print()  # Nueva línea

        elapsed = time.time() - start_time

        print()
        print(f"   ⏱️  Tiempo total: {elapsed:.2f}s")
        if response_started:
            print(f"   ⚡ Primer token: {first_token_time:.2f}s")
        print(f"   ✅ Generación exitosa!")

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

    print()
    print("=" * 70)
    print("✅ TODAS LAS PRUEBAS PASARON")
    print("=" * 70)
    print()
    print("💡 Ahora puedes usar kp-codeagent con Groq:")
    print("   kp-codeagent --backend groq run 'create fibonacci function'")
    print()
    print("⚡ Groq es ~20x más rápido que Ollama en WSL")
    print()

    return True


def test_groq_code_generation():
    """Prueba generación de código con Groq."""
    print("=" * 70)
    print("🧪 TEST DE GENERACIÓN DE CÓDIGO")
    print("=" * 70)
    print()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY no configurada")
        return False

    try:
        from groq import Groq
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    print("Prompt: 'Write a Python function to check if a number is prime'")
    print("⏳ Generando código...\n")

    start_time = time.time()

    try:
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "system",
                "content": "You are a helpful coding assistant. Provide concise, working code."
            }, {
                "role": "user",
                "content": "Write a Python function to check if a number is prime. Include docstring and comments."
            }],
            temperature=0.5,
            max_tokens=500,
            stream=True
        )

        print("📝 Código generado:\n")
        print("-" * 70)

        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)

        print()
        print("-" * 70)

        elapsed = time.time() - start_time
        print(f"\n⏱️  Tiempo: {elapsed:.2f}s")
        print("✅ Código generado exitosamente!")

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    return True


if __name__ == "__main__":
    print("\n")

    # Test 1: Conexión básica
    if not test_groq_basic():
        sys.exit(1)

    # Test 2: Generación de código
    print("\n")
    input("Presiona Enter para probar generación de código... ")
    print()

    if not test_groq_code_generation():
        sys.exit(1)

    print()
    print("=" * 70)
    print("🎉 ¡TODO FUNCIONA PERFECTAMENTE!")
    print("=" * 70)
    print()

    sys.exit(0)
