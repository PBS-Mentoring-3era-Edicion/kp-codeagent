# 🪟 Guía Oficial de Instalación de Ollama en Windows

## ℹ️ Información Oficial

Basado en la documentación oficial de Ollama: https://github.com/ollama/ollama/blob/main/docs/windows.md

---

## 📋 Requisitos del Sistema

- **Windows 10 versión 22H2 o superior** (Home o Pro)
- **8 GB de RAM mínimo** (para modelos 7B como phi)
- **Para aceleración GPU**:
  - NVIDIA: Drivers 452.39+
  - AMD: Radeon drivers actualizados
- **Espacio en disco**: 2-10 GB por modelo

---

## 🚀 Instalación en Windows (Nativo)

### Paso 1: Descargar el Instalador

1. Ve a: https://ollama.com/download
2. Descarga `OllamaSetup.exe`
3. Ejecuta el instalador

**Nota importante**:
- ✅ Ollama se instala **nativamente en Windows**
- ❌ **NO necesitas WSL** para usar Ollama
- ✅ Se instala en tu cuenta de usuario (no requiere permisos de admin)
- ✅ Se actualiza automáticamente

### Paso 2: Verificar la Instalación

Después de instalar, abre **PowerShell** o **Command Prompt** (Windows nativo, NO WSL):

```powershell
# Verificar que Ollama está instalado
ollama --version
```

**Resultado esperado**:
```
ollama version is 0.X.X
```

### Paso 3: Verificar que el Servicio Está Corriendo

```powershell
# En Windows, el servicio debería iniciar automáticamente
# Verifica con:
curl http://localhost:11434/api/version
```

**Resultado esperado**:
```json
{"version":"0.X.X"}
```

**Si NO funciona**:
- Busca "Ollama" en el menú de inicio y ejecútalo
- O abre PowerShell y ejecuta: `ollama serve`

---

## 📦 Instalar Modelos

### Descargar phi (Modelo Pequeño y Rápido)

```powershell
# En PowerShell/CMD de Windows (no WSL)
ollama pull phi
```

**Proceso**:
```
pulling manifest
pulling 1e67dff39209... 100% ▕████████████▏ 1.6 GB
pulling 2931454c2cd4... 100% ▕████████████▏  122 B
pulling c71d239df917... 100% ▕████████████▏   10 KB
pulling 31df454bc2c5... 100% ▕████████████▏  485 B
verifying sha256 digest
writing manifest
success
```

⏱️ **Tiempo estimado**: 3-10 minutos (depende de tu conexión a internet)

### Listar Modelos Instalados

```powershell
ollama list
```

**Resultado esperado**:
```
NAME            ID              SIZE      MODIFIED
phi:latest      e2fd6321a5fe    1.6 GB    X minutes ago
```

---

## 🧪 Probar que Funciona

### Prueba Básica

```powershell
ollama run phi "Say hello in one word"
```

**Primera vez (carga el modelo)**:
- ⏱️ Tarda 10-20 segundos la primera vez
- 💾 Carga el modelo en memoria

**Resultado esperado**:
```
Hello
```

**Siguientes veces**:
- ⚡ Responde en 2-5 segundos
- Modelo ya está en memoria

### Prueba Interactiva

```powershell
ollama run phi
```

Esto abre un chat interactivo:
```
>>> Hello!
Hi! How can I help you today?

>>> /bye
```

---

## 🔍 Verificación Completa Paso a Paso

### 1. Ollama está instalado
```powershell
ollama --version
```
✅ Debe mostrar: `ollama version is 0.X.X`

### 2. Servicio está corriendo
```powershell
curl http://localhost:11434/api/version
```
✅ Debe mostrar: `{"version":"0.X.X"}`

### 3. Modelo descargado
```powershell
ollama list
```
✅ Debe mostrar phi en la lista

### 4. Modelo funciona
```powershell
ollama run phi "test"
```
✅ Debe responder en menos de 20 segundos

---

## 🐛 Problemas Comunes y Soluciones

### ❌ "command not found: ollama"

**Causa**: Ollama no está instalado o no está en el PATH

**Solución**:
1. Reinstala desde https://ollama.com/download
2. Cierra y abre PowerShell de nuevo
3. Si persiste, reinicia Windows

### ❌ "Connection refused" al hacer curl

**Causa**: El servicio de Ollama no está corriendo

**Solución**:
```powershell
# Opción 1: Busca "Ollama" en el menú inicio y ejecútalo

# Opción 2: Desde PowerShell
ollama serve
```

Deja esa ventana abierta y abre otra PowerShell para ejecutar comandos.

### ❌ Responde muy lento (>60 segundos)

**Causa**: Falta de RAM, CPU lenta, o antivirus bloqueando

**Solución**:
1. Cierra otros programas (navegadores, etc.)
2. Prueba con modelo aún más pequeño:
   ```powershell
   ollama pull tinyllama
   ollama run tinyllama "test"
   ```
3. Desactiva temporalmente el antivirus (solo para probar)
4. Revisa logs en: `%LOCALAPPDATA%\Ollama\logs`

### ❌ "Error loading model"

**Causa**: Descarga incompleta o corrupta

**Solución**:
```powershell
# Volver a descargar el modelo
ollama pull phi
```

---

## 🔧 Ubicaciones Importantes

### Logs
```
%LOCALAPPDATA%\Ollama\logs
```

En PowerShell:
```powershell
explorer $env:LOCALAPPDATA\Ollama\logs
```

### Modelos descargados
```
%USERPROFILE%\.ollama\models
```

En PowerShell:
```powershell
explorer $env:USERPROFILE\.ollama\models
```

---

## 🎯 Usando Ollama desde WSL

Si tienes Ollama instalado en **Windows** y quieres usarlo desde **WSL**:

### Paso 1: Obtén la IP de Windows

En **PowerShell** (Windows):
```powershell
ipconfig
```

Busca la IP de "vEthernet (WSL)" o similar, ejemplo: `172.X.X.X`

### Paso 2: Conecta desde WSL

En **WSL**:
```bash
# Usa la IP de Windows en lugar de localhost
curl http://172.X.X.X:11434/api/version
```

### Paso 3: Configura kp-codeagent en WSL

Edita el código para usar la IP de Windows en lugar de `localhost`:

```python
# En kp_codeagent/ollama_client.py
def __init__(self, base_url: str = "http://172.X.X.X:11434", ...):
```

**O mejor**: Usa variable de entorno:
```bash
export OLLAMA_HOST="http://172.X.X.X:11434"
```

---

## ✅ Checklist de Instalación Exitosa

Marca cada paso cuando lo completes:

- [ ] OllamaSetup.exe descargado e instalado
- [ ] `ollama --version` funciona en PowerShell
- [ ] `curl http://localhost:11434/api/version` responde
- [ ] `ollama pull phi` completado exitosamente
- [ ] `ollama list` muestra phi
- [ ] `ollama run phi "test"` responde en menos de 30s
- [ ] (Opcional) Conexión desde WSL funciona

---

## 📊 Tiempos Esperados (Windows Nativo)

| Operación | Primera Vez | Subsecuente |
|-----------|-------------|-------------|
| Cargar modelo phi | 10-20s | Instantáneo |
| Respuesta simple | 3-8s | 2-5s |
| Respuesta compleja | 10-30s | 5-15s |

**Nota**: Estos son tiempos en Windows nativo. WSL puede ser 2-5x más lento.

---

## 🆘 Si Nada Funciona

### Opción 1: Reinstalación Limpia

```powershell
# 1. Desinstalar Ollama
# Ve a: Configuración > Aplicaciones > Ollama > Desinstalar

# 2. Eliminar datos residuales
Remove-Item -Recurse -Force $env:LOCALAPPDATA\Ollama
Remove-Item -Recurse -Force $env:USERPROFILE\.ollama

# 3. Reinicia Windows

# 4. Reinstala desde ollama.com/download
```

### Opción 2: Reportar el Problema

1. Revisa los logs:
   ```powershell
   notepad $env:LOCALAPPDATA\Ollama\logs\server.log
   ```

2. Reporta en: https://github.com/ollama/ollama/issues

3. Incluye:
   - Versión de Windows
   - Versión de Ollama
   - Contenido de los logs
   - Qué comando falla

---

## 📚 Recursos Oficiales

- **Página oficial**: https://ollama.com
- **Documentación**: https://github.com/ollama/ollama
- **Windows docs**: https://github.com/ollama/ollama/blob/main/docs/windows.md
- **Modelos disponibles**: https://ollama.com/library
- **Issues**: https://github.com/ollama/ollama/issues

---

## 💡 Próximos Pasos

Una vez que Ollama funcione correctamente:

1. **Probar con kp-codeagent**:
   ```powershell
   cd kp-codeagent
   kp-codeagent check
   kp-codeagent --model phi run "create hello.py"
   ```

2. **Descargar más modelos**:
   ```powershell
   ollama pull codellama    # Mejor para código
   ollama pull llama3       # Modelo general potente
   ```

3. **Explorar la API**:
   ```powershell
   curl http://localhost:11434/api/tags
   ```

---

**Última actualización**: 2025-10-13
**Basado en**: Ollama v0.12.3 Windows documentation
