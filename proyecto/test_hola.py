#!/usr/bin/env python3
"""Pruebas para hola.py"""

import subprocess
import sys

def test_hola_mundo():
    """Prueba que el script se ejecute correctamente."""
    print("🧪 Ejecutando prueba...")

    result = subprocess.run(
        [sys.executable, "hola.py"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("   ✅ El script se ejecutó correctamente")
        print(f"   📤 Salida:\n{result.stdout}")
        return True
    else:
        print("   ❌ El script falló")
        print(f"   ⚠️  Error:\n{result.stderr}")
        return False

if __name__ == "__main__":
    success = test_hola_mundo()
    sys.exit(0 if success else 1)
