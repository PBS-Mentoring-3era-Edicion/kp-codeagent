# 🤖 KP Code Agent

**Tu Asistente de Código Local con IA para Estudiantes**

[English](README.md) | **Español**

KP Code Agent es un asistente de programación basado en terminal que se ejecuta localmente en tu máquina usando CodeLlama. Ayuda a los estudiantes a completar tareas de programación, aprender mejores prácticas y mejorar sus habilidades de programación - ¡todo desde la línea de comandos!

## ✨ Características

- 🚀 **Ejecución Local Rápida** - No requiere internet después de la configuración
- 🎓 **Enfoque Educativo** - Explica el código y enseña mejores prácticas
- 🔒 **Privado y Seguro** - Todo el código permanece en tu máquina
- 💬 **Interactivo** - Confirma cambios antes de modificar archivos
- 🎨 **Interfaz de Terminal Hermosa** - Resaltado de sintaxis y salida formateada
- 🔄 **Operaciones de Archivo Seguras** - Respaldos automáticos antes de modificaciones

## 📋 Requisitos

- **Sistema Operativo**: Windows 10/11, macOS, o Linux (incluyendo WSL)
- **Python**: 3.10 o superior
- **RAM**: 8GB mínimo (16GB recomendado para modelo 13B)
- **Espacio en Disco**: ~6GB para instalación y modelo
- **Ollama**: Runtime de LLM local (auto-instalado por script de configuración)

## 🚀 Inicio Rápido

### Instalación (5 minutos)

#### Windows
```bash
# Descarga el repositorio
git clone https://github.com/kp-codeagent/kp-codeagent.git
cd kp-codeagent

# Ejecuta el instalador
installer\install.bat
```

#### Linux / macOS / WSL
```bash
# Descarga el repositorio
git clone https://github.com/kp-codeagent/kp-codeagent.git
cd kp-codeagent

# Ejecuta el instalador
chmod +x installer/install.sh
./installer/install.sh
```

#### Instalación Manual
```bash
# Instala dependencias de Python
pip install -r requirements.txt

# Instala e inicia Ollama
# Visita: https://ollama.ai/download

# Descarga el modelo CodeLlama
ollama pull codellama:7b

# Instala KP Code Agent
pip install -e .
```

### Primer Uso

1. **Verifica si todo está listo**:
   ```bash
   kp-codeagent check
   ```

2. **Ejecuta tu primera tarea en español**:
   ```bash
   kp-codeagent --lang es "crea una función Python para calcular números fibonacci"
   ```

3. **Revisa y confirma los cambios** cuando se te solicite

## 📖 Uso

### Comando Básico
```bash
kp-codeagent --lang es "tu descripción de tarea aquí"
```

### Ejemplos

**Crear código nuevo**:
```bash
kp-codeagent --lang es "crea una función Python que valide direcciones de correo electrónico"
```

**Modificar código existente**:
```bash
kp-codeagent --lang es "agrega manejo de errores a la función de login en auth.py"
```

**Corregir errores**:
```bash
kp-codeagent --lang es "corrige el error de puntero nulo en main.java"
```

**Agregar funcionalidades**:
```bash
kp-codeagent --lang es "agrega un botón de modo oscuro a la página de configuración"
```

**Refactorizar código**:
```bash
kp-codeagent --lang es "refactoriza el código de conexión a base de datos para usar connection pooling"
```

### Opciones Avanzadas

```bash
# Usar un modelo diferente
kp-codeagent --lang es --model codellama:13b "tu tarea"

# Ajustar creatividad (0.0 = enfocado, 1.0 = creativo)
kp-codeagent --lang es --temperature 0.3 "tu tarea"

# Habilitar modo verboso para depuración
kp-codeagent --lang es --verbose "tu tarea"

# Modificar un archivo específico
kp-codeagent --lang es modify ruta/al/archivo.py "agrega validación de entrada"
```

### Comandos Disponibles

```bash
kp-codeagent --help                    # Mostrar ayuda
kp-codeagent check                     # Verificar configuración
kp-codeagent setup                     # Descargar/configurar modelos
kp-codeagent modify ARCHIVO TAREA      # Modificar archivo específico
```

## 🎓 Cómo Funciona

1. **Analizar**: Escanea tu proyecto para entender el contexto
2. **Planear**: Crea un plan de implementación paso a paso
3. **Implementar**: Genera código limpio y bien documentado
4. **Verificar**: Te muestra los cambios con resaltado de sintaxis
5. **Confirmar**: Pide tu aprobación antes de hacer cambios
6. **Ejecutar**: Aplica cambios con respaldos automáticos

## 🔒 Características de Seguridad

- ✅ **Respaldos Automáticos** - Archivos respaldados antes de modificación
- ✅ **Solicitudes de Confirmación** - Apruebas todos los cambios
- ✅ **Previsualizar Cambios** - Ver diferencias antes de aplicar
- ✅ **Restaurar desde Respaldo** - Reversión fácil si es necesario
- ✅ **Verificación de Permisos** - Valida acceso de escritura
- ✅ **Sin Llamadas Remotas** - Todo se ejecuta localmente

## 🎯 Mejores Prácticas

### Escribir Buenas Descripciones de Tareas

**Bueno** ✅:
- "Crea una función para validar números de tarjeta de crédito usando el algoritmo de Luhn"
- "Agrega limitación de tasa a los endpoints de API en server.py"
- "Corrige la fuga de memoria en el pipeline de procesamiento de imágenes"

**Muy Vago** ❌:
- "Hazlo mejor"
- "Corrige errores"
- "Actualiza el código"

### Consejos para Mejores Resultados

1. **Sé Específico**: Describe claramente lo que quieres
2. **Proporciona Contexto**: Menciona nombres de archivos o funciones cuando sea relevante
3. **Una Tarea a la Vez**: Divide tareas complejas en pasos más pequeños
4. **Revisa los Cambios**: Siempre revisa el código antes de aceptar
5. **Aprende de las Explicaciones**: KP Code Agent explica sus decisiones

## 🛠️ Configuración

### Cambiar Modelo Predeterminado

Edita tu comando o usa la bandera:
```bash
kp-codeagent --lang es --model codellama:13b "tu tarea"
```

Modelos disponibles:
- `codellama:7b` - Más rápido, usa menos RAM (predeterminado)
- `codellama:13b` - Más capaz, requiere 16GB RAM
- `codellama:34b` - Más capaz, requiere 32GB RAM

### Ajustar Temperatura

La temperatura controla la creatividad (0.0 - 1.0):
- `0.0-0.3`: Enfocado, determinista (bueno para corrección de errores)
- `0.4-0.7`: Balanceado (predeterminado: 0.7)
- `0.8-1.0`: Creativo (bueno para lluvia de ideas)

```bash
kp-codeagent --lang es --temperature 0.3 "corrige error de sintaxis en main.py"
```

## 🐛 Solución de Problemas

### Ollama No Está Ejecutándose
```bash
# Verifica el estado de Ollama
curl http://localhost:11434

# Inicia Ollama (Linux/macOS)
ollama serve

# Inicia Ollama (Windows)
# Ejecuta Ollama desde el Menú Inicio
```

### Modelo No Encontrado
```bash
# Descarga el modelo
ollama pull codellama:7b

# Verifica que esté disponible
ollama list
```

### Python No Encontrado
```bash
# Verifica la instalación de Python
python --version  # o python3 --version

# Debe mostrar Python 3.10+
```

## 📄 Licencia

Licencia MIT - ver archivo LICENSE para detalles

## 💬 Soporte

- **Documentación**: Consulta este README y ayuda en línea
- **Issues**: https://github.com/kp-codeagent/kp-codeagent/issues
- **Discusiones**: https://github.com/kp-codeagent/kp-codeagent/discussions

## 🗺️ Hoja de Ruta

- [ ] Conversaciones de múltiples turnos
- [ ] Generación automática de pruebas
- [ ] Modo de revisión de código
- [ ] Integración con Git
- [ ] Plantillas de proyecto
- [ ] Extensión de VS Code
- [ ] Interfaz web UI
- [ ] Soporte para más modelos (GPT4All, etc.)

---

**Hecho con ❤️ para estudiantes aprendiendo a programar**

*KP Code Agent - Tu compañero de código local con IA*
