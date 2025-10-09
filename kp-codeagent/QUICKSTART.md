# KP Code Agent - Quick Start Guide

**English** | [Español](#guía-rápida-español)

---

## English Quick Start

### 1. Install Dependencies

```bash
cd kp-codeagent
pip install -r requirements.txt
```

### 2. Install Ollama

**Linux/WSL/macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from https://ollama.ai/download

### 3. Download Model

```bash
ollama pull codellama:7b
```

### 4. Install KP Code Agent

```bash
pip install -e .
```

### 5. Test It!

```bash
# Check setup
kp-codeagent check

# Run your first task
kp-codeagent "create a hello world Python script"
```

### Common Commands

```bash
# Execute a task
kp-codeagent "your task description"

# Use Spanish
kp-codeagent --lang es "tu tarea"

# Use different model
kp-codeagent --model codellama:13b "your task"

# Modify a specific file
kp-codeagent modify path/to/file.py "add error handling"

# Get help
kp-codeagent --help
```

---

## Guía Rápida (Español)

### 1. Instalar Dependencias

```bash
cd kp-codeagent
pip install -r requirements.txt
```

### 2. Instalar Ollama

**Linux/WSL/macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Descarga desde https://ollama.ai/download

### 3. Descargar Modelo

```bash
ollama pull codellama:7b
```

### 4. Instalar KP Code Agent

```bash
pip install -e .
```

### 5. ¡Pruébalo!

```bash
# Verificar configuración
kp-codeagent check

# Ejecutar tu primera tarea en español
kp-codeagent --lang es "crea un script de hola mundo en Python"
```

### Comandos Comunes

```bash
# Ejecutar una tarea en español
kp-codeagent --lang es "tu descripción de tarea"

# Usar inglés (predeterminado)
kp-codeagent "your task"

# Usar modelo diferente
kp-codeagent --lang es --model codellama:13b "tu tarea"

# Modificar un archivo específico
kp-codeagent --lang es modify ruta/al/archivo.py "agrega manejo de errores"

# Obtener ayuda
kp-codeagent --help
```

---

## Troubleshooting / Solución de Problemas

### Ollama Not Running / Ollama No Ejecutándose

**English:**
```bash
# Check if Ollama is running
curl http://localhost:11434

# Start Ollama
ollama serve
```

**Español:**
```bash
# Verificar si Ollama está ejecutándose
curl http://localhost:11434

# Iniciar Ollama
ollama serve
```

### Model Not Found / Modelo No Encontrado

```bash
# Download the model
ollama pull codellama:7b

# List available models
ollama list
```

### Python Version Issues / Problemas de Versión de Python

```bash
# Check Python version (should be 3.10+)
python --version

# Or try
python3 --version
```

---

## Examples / Ejemplos

### English Examples

```bash
# Create a function
kp-codeagent "create a function to validate email addresses"

# Fix a bug
kp-codeagent "fix the null pointer error in main.py"

# Add a feature
kp-codeagent "add input validation to the login form"

# Refactor code
kp-codeagent "refactor the database connection to use connection pooling"
```

### Ejemplos en Español

```bash
# Crear una función
kp-codeagent --lang es "crea una función para validar direcciones de correo"

# Corregir un error
kp-codeagent --lang es "corrige el error de puntero nulo en main.py"

# Agregar una funcionalidad
kp-codeagent --lang es "agrega validación de entrada al formulario de login"

# Refactorizar código
kp-codeagent --lang es "refactoriza la conexión a base de datos para usar connection pooling"
```

---

## Environment Variables / Variables de Entorno

Set default language:

```bash
# English (default)
export KP_LANG=en

# Spanish
export KP_LANG=es
```

Then you can use KP Code Agent without the `--lang` flag:

```bash
# Will use KP_LANG environment variable
kp-codeagent "your task"
```

---

## Tips / Consejos

**English:**
- Be specific in your task descriptions
- Review all changes before accepting
- Use `--verbose` flag for debugging
- Start with small tasks to learn how it works

**Español:**
- Sé específico en tus descripciones de tareas
- Revisa todos los cambios antes de aceptar
- Usa la bandera `--verbose` para depuración
- Comienza con tareas pequeñas para aprender cómo funciona

---

**Need more help?** Check the full [README](README.md) or [README_ES](README_ES.md)

**¿Necesitas más ayuda?** Consulta el [README](README.md) completo o [README_ES](README_ES.md)
