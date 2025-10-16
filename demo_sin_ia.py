#!/usr/bin/env python3
"""Demo del sistema sin necesitar IA - para probar la funcionalidad."""

import os
from pathlib import Path

def crear_hola_mundo():
    """Crea un proyecto simple de prueba."""

    print("🚀 Creando proyecto de prueba...\n")

    # 1. Crear carpeta
    print("📁 Paso 1: Creando carpeta 'proyecto'...")
    project_dir = Path("proyecto")
    project_dir.mkdir(exist_ok=True)
    print("   ✅ Carpeta creada\n")

    # 2. Crear archivo hola.py
    print("📝 Paso 2: Creando archivo hola.py...")
    hola_file = project_dir / "hola.py"
    codigo = '''#!/usr/bin/env python3
"""
Script simple de Hola Mundo
Creado como demostración
"""

def main():
    """Función principal."""
    mensaje = "¡Hola Mundo!"
    print(mensaje)
    print("=" * len(mensaje))
    print("Este es un programa de prueba")
    return 0

if __name__ == "__main__":
    exit(main())
'''
    hola_file.write_text(codigo)
    print("   ✅ Archivo hola.py creado\n")

    # 3. Crear archivo de prueba
    print("🧪 Paso 3: Creando test_hola.py...")
    test_file = project_dir / "test_hola.py"
    test_codigo = '''#!/usr/bin/env python3
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
        print(f"   📤 Salida:\\n{result.stdout}")
        return True
    else:
        print("   ❌ El script falló")
        print(f"   ⚠️  Error:\\n{result.stderr}")
        return False

if __name__ == "__main__":
    success = test_hola_mundo()
    sys.exit(0 if success else 1)
'''
    test_file.write_text(test_codigo)
    print("   ✅ Archivo test_hola.py creado\n")

    # 4. Ejecutar el programa
    print("▶️  Paso 4: Ejecutando hola.py...")
    os.system(f"cd {project_dir} && python3 hola.py")
    print()

    # 5. Ejecutar prueba
    print("🧪 Paso 5: Ejecutando pruebas...")
    os.system(f"cd {project_dir} && python3 test_hola.py")
    print()

    # Resumen
    print("=" * 60)
    print("✅ ¡PROYECTO CREADO EXITOSAMENTE!")
    print("=" * 60)
    print(f"\n📂 Archivos creados en: {project_dir.absolute()}")
    print("   - hola.py (programa principal)")
    print("   - test_hola.py (pruebas)")
    print("\n💡 Para ejecutar manualmente:")
    print(f"   cd {project_dir}")
    print("   python3 hola.py")
    print("   python3 test_hola.py")

if __name__ == "__main__":
    crear_hola_mundo()
