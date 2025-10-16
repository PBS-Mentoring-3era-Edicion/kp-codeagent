# 🤖 KP Code Agent

**Tu Asistente de Código con IA para Estudiantes**

[English](README.md) | **Español**

KP Code Agent es un asistente de programación basado en terminal que ayuda a estudiantes a completar tareas de programación, aprender mejores prácticas y mejorar sus habilidades - ¡todo desde la línea de comandos!

## ⚡ NUEVO: Backend en la Nube Ultra-Rápido (Groq) - **RECOMENDADO para WSL**

**Usuarios de WSL**: Si Ollama es lento (>30s), usa **Groq** en su lugar - ¡es **20x más rápido** y **100% GRATIS**!

```bash
# 1. Instala soporte para Groq
pip install groq

# 2. Obtén API key GRATIS en https://console.groq.com/keys

# 3. Configura
export GROQ_API_KEY="gsk_tu_key_aqui"

# 4. Úsalo (0.7-2 segundos vs 30-90s con Ollama!)
kp-codeagent --backend groq --lang es run "crea función fibonacci"
```

**¿Por qué Groq?**
- ⚡ **20x más rápido** que Ollama en WSL (0.7s vs 47s)
- 🆓 **100% GRATIS** (30 requests/min, 14,400/día)
- 💾 **0 uso de RAM** (corre en la nube)
- 🎯 **Mejor calidad de código** (modelo Llama 3.3 70B)
- ✅ **Funciona perfectamente en WSL**

📖 **Guía completa**: Ver `GUIA_GROQ.md`

---

## ✨ Características

- 🚀 **Súper Rápido** - 0.7-2s con Groq, sin internet después con Ollama
- 🎓 **Enfoque Educativo** - Explica el código y enseña mejores prácticas
- 🔒 **Privado y Seguro** - Opción local con Ollama o nube con Groq
- 💬 **Interactivo** - Confirma cambios antes de modificar archivos
- 🎨 **Interfaz de Terminal Hermosa** - Resaltado de sintaxis y salida formateada
- 🔄 **Operaciones de Archivo Seguras** - Respaldos automáticos antes de modificaciones
- 🌍 **Bilingüe** - Soporte completo en Español e Inglés

## 📋 Requisitos

- **Sistema Operativo**: Windows 10/11, macOS, o Linux (incluyendo WSL)
- **Python**: 3.10 o superior
- **Backend**: Elige uno:
  - **Groq** (recomendado para WSL): 0 MB RAM, requiere internet
  - **Ollama** (privado): 4-6GB RAM, sin internet

## 🚀 Inicio Rápido

### Instalación - Elige tu Backend

#### ⚡ Opción 1: Groq (Recomendado - Rápido y Fácil)

**Mejor para**: WSL, sistemas con poca RAM, configuración rápida

```bash
# 1. Descarga el repositorio
git clone https://github.com/kp-codeagent/kp-codeagent.git
cd kp-codeagent/kp-codeagent

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Instala KP Code Agent
pip install -e .

# 4. Obtén tu API key GRATIS de https://console.groq.com/keys

# 5. Configura
export GROQ_API_KEY="gsk_tu_key_aqui"

# 6. ¡Listo! Pruébalo:
kp-codeagent --backend groq --lang es run "crea una función hello world"
```

**Tiempo de instalación**: ~2 minutos
**Primera respuesta**: 0.7-2 segundos ⚡

---

#### 🔒 Opción 2: Ollama (Local y Privado)

**Mejor para**: Usuarios enfocados en privacidad, sin internet después de la instalación

```bash
# 1. Descarga el repositorio
git clone https://github.com/kp-codeagent/kp-codeagent.git
cd kp-codeagent

# 2. Ejecuta el instalador
# Windows:
installer\install.bat

# Linux/macOS/WSL:
chmod +x installer/install.sh
./installer/install.sh

# 3. O instalación manual:
pip install -r requirements.txt
# Instala Ollama desde https://ollama.ai/download
ollama pull codellama:7b
pip install -e .
```

**Tiempo de instalación**: ~5-10 minutos
**Primera respuesta**: 10-60 segundos (más rápido después de la primera carga)

### Primer Uso

#### ⚡ Con Groq (Recomendado)

1. **Configura tu API key**:
   ```bash
   export GROQ_API_KEY="gsk_tu_key_aqui"

   # Hacerla permanente (opcional):
   echo 'export GROQ_API_KEY="gsk_tu_key"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Prueba que funciona**:
   ```bash
   python3 test_groq.py
   ```

   Esperado: ✅ Respuesta en ~0.7 segundos

3. **Ejecuta tu primera tarea**:
   ```bash
   kp-codeagent --backend groq --lang es run "crea una función Python para calcular números fibonacci"
   ```

4. **Revisa y confirma** los cambios cuando se te solicite

**Rendimiento**:
- ⚡ Primera respuesta: 0.7-2 segundos
- 🆓 Completamente GRATIS (30 req/min, 14,400/día)
- 💾 0 uso de RAM en tu máquina

---

#### 🔒 Con Ollama (Alternativa)

##### Para Usuarios de Windows (PowerShell):

1. **Verifica que Ollama esté instalado y ejecutándose**:
   ```powershell
   ollama --version
   ollama list
   ```

2. **Descarga un modelo** (si no lo hiciste aún):
   ```powershell
   ollama pull codellama:7b
   ```

3. **Ejecuta kp-codeagent**:
   ```powershell
   kp-codeagent check
   kp-codeagent --lang es run "crea una función Python para calcular números fibonacci"
   ```

##### Para Usuarios de Linux/macOS/WSL:

1. **Verifica si todo está listo**:
   ```bash
   kp-codeagent check
   ```

2. **Ejecuta tu primera tarea**:
   ```bash
   kp-codeagent --lang es run "crea una función Python para calcular números fibonacci"
   ```

**Rendimiento**:
- ⏱️ Primera ejecución puede tardar 20-60 segundos mientras el modelo carga en memoria
- 🪟 Usuarios de Windows: Ejecuta Ollama **nativamente en Windows**, no en WSL para mejor rendimiento
- 📖 Ver `GUIA_INSTALACION_OLLAMA_WINDOWS.md` para instalación detallada en Windows

---

💡 **Consejo**: Si Ollama es lento en WSL, cambia a Groq para obtener ¡un rendimiento 20x más rápido!

## 📖 Uso

### Comando Básico

```bash
# Con Groq (recomendado - súper rápido)
kp-codeagent --backend groq --lang es run "tu descripción de tarea aquí"

# Con Ollama (local)
kp-codeagent --lang es run "tu descripción de tarea aquí"
```

### Ejemplos

**Crear código nuevo con Groq**:
```bash
kp-codeagent --backend groq --lang es run "crea una función Python que valide direcciones de correo electrónico"
```

**Modificar código existente**:
```bash
kp-codeagent --backend groq --lang es run "agrega manejo de errores a la función de login en auth.py"
```

**Corregir errores**:
```bash
kp-codeagent --backend groq --lang es run "corrige el error de puntero nulo en main.java"
```

**Agregar funcionalidades**:
```bash
kp-codeagent --backend groq --lang es run "agrega un botón de modo oscuro a la página de configuración"
```

**Refactorizar código**:
```bash
kp-codeagent --backend groq --lang es run "refactoriza el código de conexión a base de datos para usar connection pooling"
```

### Opciones Avanzadas

```bash
# 🌟 RECOMENDADO: Usar backend Groq (rápido, nube, GRATIS)
kp-codeagent --backend groq --lang es run "tu tarea"

# Usar diferentes modelos de Groq
kp-codeagent --backend groq --model llama-3.3-70b-versatile --lang es run "tarea"      # Default
kp-codeagent --backend groq --model llama-3.1-8b-instant --lang es run "tarea rápida" # Más rápido
kp-codeagent --backend groq --model openai/gpt-oss-120b --lang es run "tarea compleja" # Más potente

# Usar backend Ollama (local, privado)
kp-codeagent --backend ollama --model codellama:13b --lang es run "tu tarea"

# Auto-detectar mejor backend disponible (prueba Groq → OpenAI → Ollama)
kp-codeagent --backend auto --lang es run "tu tarea"

# Ajustar creatividad (0.0 = enfocado, 1.0 = creativo)
kp-codeagent --backend groq --lang es --temperature 0.3 run "tu tarea"

# Habilitar modo verboso para depuración
kp-codeagent --backend groq --lang es --verbose run "tu tarea"

# Modificar un archivo específico
kp-codeagent --backend groq --lang es modify ruta/al/archivo.py "agrega validación de entrada"
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

### Backends Disponibles

#### Groq (Recomendado para WSL)
```bash
kp-codeagent --backend groq --lang es run "tu tarea"
```

**Modelos Groq**:
- `llama-3.3-70b-versatile` - Mejor para código (predeterminado)
- `llama-3.1-8b-instant` - Más rápido
- `openai/gpt-oss-120b` - Máxima calidad

**Ventajas**: 20x más rápido, 0 RAM, gratis

#### Ollama (Local y Privado)
```bash
kp-codeagent --backend ollama --model codellama:7b --lang es run "tu tarea"
```

**Modelos Ollama**:
- `codellama:7b` - Más rápido, usa menos RAM
- `codellama:13b` - Más capaz, requiere 16GB RAM
- `codellama:34b` - Más capaz, requiere 32GB RAM

**Ventajas**: 100% privado, sin internet

### Ajustar Temperatura

La temperatura controla la creatividad (0.0 - 1.0):
- `0.0-0.3`: Enfocado, determinista (bueno para corrección de errores)
- `0.4-0.7`: Balanceado (predeterminado: 0.7)
- `0.8-1.0`: Creativo (bueno para lluvia de ideas)

```bash
kp-codeagent --lang es --temperature 0.3 "corrige error de sintaxis en main.py"
```

## 🐛 Solución de Problemas

### Groq es muy lento o da timeout

**Síntoma**: Groq tarda más de 5 segundos

**Solución**:
```bash
# 1. Verifica tu conexión a internet
ping api.groq.com

# 2. Verifica que la API key sea correcta
echo $GROQ_API_KEY

# 3. Prueba con modelo más rápido
kp-codeagent --backend groq --model llama-3.1-8b-instant --lang es run "tarea"
```

### Error: "API key not found"

```bash
# Verifica que la key esté exportada
echo $GROQ_API_KEY

# Si no muestra nada, expórtala
export GROQ_API_KEY="gsk_tu_key_aqui"

# Para que sea permanente, agrégala a .bashrc
echo 'export GROQ_API_KEY="gsk_tu_key"' >> ~/.bashrc
source ~/.bashrc
```

### Ollama No Está Ejecutándose

```bash
# Verifica el estado de Ollama
curl http://localhost:11434/api/tags

# Inicia Ollama (Linux/macOS)
ollama serve

# Inicia Ollama (Windows)
# Ejecuta Ollama desde el Menú Inicio
```

### Modelo de Ollama No Encontrado

```bash
# Descarga el modelo
ollama pull codellama:7b

# Verifica que esté disponible
ollama list
```

### Ollama muy lento en WSL

**Solución**: Usa Groq en su lugar (20x más rápido)
```bash
pip install groq
export GROQ_API_KEY="gsk_tu_key_aqui"
kp-codeagent --backend groq --lang es run "tu tarea"
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
