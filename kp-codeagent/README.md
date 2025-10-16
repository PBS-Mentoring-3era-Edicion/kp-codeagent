# 🤖 KP Code Agent

**A Local AI Coding Assistant for Students**

**English** | [Español](README_ES.md)

KP Code Agent is a terminal-based coding assistant that runs locally on your machine using CodeLlama. It helps students complete coding tasks, learn best practices, and improve their programming skills - all from the command line!

## 🌍 Language Support / Soporte de Idiomas

KP Code Agent supports **English** and **Spanish**!

- **English**: `kp-codeagent "your task"`
- **Español**: `kp-codeagent --lang es "tu tarea"`

The AI will respond in your selected language and provide educational explanations in that language.

## ✨ Features

- 🚀 **Fast Local Execution** - No internet required after setup
- 🎓 **Educational Focus** - Explains code and teaches best practices
- 🔒 **Private & Secure** - All code stays on your machine
- 💬 **Interactive** - Confirms changes before modifying files
- 🎨 **Beautiful Terminal UI** - Syntax highlighting and formatted output
- 🔄 **Safe File Operations** - Automatic backups before modifications

## 📋 Requirements

- **Operating System**: Windows 10/11, macOS, or Linux (including WSL)
- **Python**: 3.10 or higher
- **RAM**: 8GB minimum (16GB recommended for 13B model)
- **Disk Space**: ~6GB for installation and model
- **Ollama**: Local LLM runtime (auto-installed by setup script)

**Note for WSL Users**: Ollama may run 2-3x slower in WSL. Consider:
- Installing Ollama natively in Windows
- Using smaller models (`tinyllama` or `phi:latest`)
- Using the included demo mode for development/testing

## ⚡ NEW: Ultra-Fast Cloud Backend (Groq) - **RECOMMENDED for WSL**

**WSL Users**: If Ollama is slow (>30s), use **Groq** instead - it's **20x faster** and **100% FREE**!

```bash
# 1. Install Groq support
pip install groq

# 2. Get FREE API key from https://console.groq.com/keys

# 3. Configure
export GROQ_API_KEY="gsk_your_key_here"

# 4. Use it (0.7-2 seconds vs 30-90s with Ollama!)
kp-codeagent --backend groq run "create fibonacci function"
```

**Why Groq?**
- ⚡ **20x faster** than Ollama in WSL (0.7s vs 47s)
- 🆓 **100% FREE** (30 requests/min, 14,400/day)
- 💾 **0 RAM usage** (runs in cloud)
- 🎯 **Better code quality** (Llama 3.3 70B model)
- ✅ **Works perfectly in WSL**

📖 **Full guide**: See `GUIA_GROQ.md` | **Guía en español**: `GUIA_GROQ.md`

---

## 🚀 Quick Start

### Installation - Choose Your Backend

#### ⚡ Option 1: Groq (Recommended - Fast & Easy)

**Best for**: WSL, low-RAM systems, quick setup

```bash
# 1. Download the repository
git clone https://github.com/kp-codeagent/kp-codeagent.git
cd kp-codeagent/kp-codeagent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install KP Code Agent
pip install -e .

# 4. Get FREE Groq API key from https://console.groq.com/keys

# 5. Configure
export GROQ_API_KEY="gsk_your_key_here"

# 6. You're ready! Test it:
kp-codeagent --backend groq run "create a hello world function"
```

**Setup time**: ~2 minutes
**First response**: 0.7-2 seconds ⚡

---

#### 🔒 Option 2: Ollama (Local & Private)

**Best for**: Privacy-focused users, no internet after setup

```bash
# 1. Download the repository
git clone https://github.com/kp-codeagent/kp-codeagent.git
cd kp-codeagent

# 2. Run installer
# Windows:
installer\install.bat

# Linux/macOS/WSL:
chmod +x installer/install.sh
./installer/install.sh

# 3. Or manual installation:
pip install -r requirements.txt
# Install Ollama from https://ollama.ai/download
ollama pull codellama:7b
pip install -e .
```

**Setup time**: ~5-10 minutes
**First response**: 10-60 seconds (faster after first load)

### First Use

#### ⚡ With Groq (Recommended)

1. **Set your API key**:
   ```bash
   export GROQ_API_KEY="gsk_your_key_here"

   # Make it permanent (optional):
   echo 'export GROQ_API_KEY="gsk_your_key"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Test it works**:
   ```bash
   python3 test_groq.py
   ```

   Expected: ✅ Response in ~0.7 seconds

3. **Run your first task**:
   ```bash
   kp-codeagent --backend groq run "create a Python function to calculate fibonacci numbers"
   ```

4. **Review and confirm** the changes when prompted

**Performance**:
- ⚡ First response: 0.7-2 seconds
- 🆓 Completely FREE (30 req/min, 14,400/day)
- 💾 0 RAM usage on your machine

---

#### 🔒 With Ollama (Alternative)

##### For Windows Users (PowerShell):

1. **Verify Ollama is installed and running**:
   ```powershell
   ollama --version
   ollama list
   ```

2. **Download a model** (if not already done):
   ```powershell
   ollama pull codellama:7b
   ```

3. **Run kp-codeagent**:
   ```powershell
   kp-codeagent check
   kp-codeagent run "create a Python function to calculate fibonacci numbers"
   ```

##### For Linux/macOS/WSL Users:

1. **Check if everything is ready**:
   ```bash
   kp-codeagent check
   ```

2. **Run your first task**:
   ```bash
   kp-codeagent run "create a Python function to calculate fibonacci numbers"
   ```

**Performance**:
- ⏱️ First run may take 20-60 seconds while model loads into memory
- 🪟 Windows users: Run Ollama **natively in Windows**, not in WSL for best performance
- 📖 See `GUIA_INSTALACION_OLLAMA_WINDOWS.md` for detailed Windows setup

---

💡 **Tip**: If Ollama is slow in WSL, switch to Groq for 20x faster performance!

## 📖 Usage

### Basic Command
```bash
kp-codeagent run "your task description here"
```

### Examples

**Create new code**:
```bash
kp-codeagent run "create a Python function that validates email addresses"
```

**Modify existing code**:
```bash
kp-codeagent run "add error handling to the login function in auth.py"
```

**Fix bugs**:
```bash
kp-codeagent run "fix the null pointer error in main.java"
```

**Add features**:
```bash
kp-codeagent run "add a dark mode toggle to the settings page"
```

**Refactor code**:
```bash
kp-codeagent run "refactor the database connection code to use connection pooling"
```

### Advanced Options

```bash
# 🌟 RECOMMENDED: Use Groq backend (fast, cloud-based, FREE)
kp-codeagent --backend groq run "your task"

# Use different Groq models
kp-codeagent --backend groq --model llama-3.3-70b-versatile run "task"     # Default
kp-codeagent --backend groq --model llama-3.1-8b-instant run "quick task"  # Faster
kp-codeagent --backend groq --model openai/gpt-oss-120b run "complex"      # Most powerful

# Use OpenAI backend (best quality, paid)
kp-codeagent --backend openai --api-key sk-... run "your task"

# Use Ollama backend (local, private)
kp-codeagent --backend ollama --model codellama:13b run "your task"

# Auto-detect best available backend (tries Groq → OpenAI → Ollama)
kp-codeagent --backend auto run "your task"

# Adjust creativity (0.0 = focused, 1.0 = creative)
kp-codeagent --temperature 0.3 run "your task"

# Enable verbose mode for debugging
kp-codeagent --verbose run "your task"

# Use Spanish language
kp-codeagent --lang es run "tu tarea"

# Combine Groq with Spanish
kp-codeagent --backend groq --lang es run "crea función factorial"

# Modify a specific file
kp-codeagent --backend groq modify path/to/file.py "add input validation"
```

### Available Commands

```bash
kp-codeagent --help              # Show help
kp-codeagent check               # Verify setup
kp-codeagent setup               # Download/setup models
kp-codeagent modify FILE TASK    # Modify specific file
```

## 🎓 How It Works

1. **Analyze**: Scans your project to understand the context
2. **Plan**: Creates a step-by-step implementation plan
3. **Implement**: Generates clean, well-documented code
4. **Verify**: Shows you the changes with syntax highlighting
5. **Confirm**: Asks for your approval before making changes
6. **Execute**: Applies changes with automatic backups

## 🔒 Safety Features

- ✅ **Automatic Backups** - Files backed up before modification
- ✅ **Confirmation Prompts** - You approve all changes
- ✅ **Preview Changes** - See diffs before applying
- ✅ **Restore from Backup** - Easy rollback if needed
- ✅ **Permission Checks** - Validates write access
- ✅ **No Remote Calls** - Everything runs locally

## 🎯 Best Practices

### Writing Good Task Descriptions

**Good** ✅:
- "Create a function to validate credit card numbers using the Luhn algorithm"
- "Add rate limiting to the API endpoints in server.py"
- "Fix the memory leak in the image processing pipeline"

**Too Vague** ❌:
- "Make it better"
- "Fix bugs"
- "Update the code"

### Tips for Best Results

1. **Be Specific**: Clearly describe what you want
2. **Provide Context**: Mention file names or function names when relevant
3. **One Task at a Time**: Break complex tasks into smaller steps
4. **Review Changes**: Always review the code before accepting
5. **Learn from Explanations**: KP Code Agent explains its decisions

## 🛠️ Configuration

### Change Default Model

Edit your command or use the flag:
```bash
kp-codeagent --model codellama:13b "your task"
```

Available models:
- `codellama:7b` - Faster, uses less RAM (default)
- `codellama:13b` - More capable, requires 16GB RAM
- `codellama:34b` - Most capable, requires 32GB RAM

### Adjust Temperature

Temperature controls creativity (0.0 - 1.0):
- `0.0-0.3`: Focused, deterministic (good for bug fixes)
- `0.4-0.7`: Balanced (default: 0.7)
- `0.8-1.0`: Creative (good for brainstorming)

```bash
kp-codeagent --temperature 0.3 "fix syntax error in main.py"
```

## 🐛 Troubleshooting

### Quick Diagnostics

Run the diagnostic script to check your setup:
```bash
# Test if Ollama is working correctly
python3 test_ollama.py

# Or run detailed diagnostics
bash test_ollama_detallado.sh
```

### Ollama Not Running
```bash
# Check Ollama status
curl http://localhost:11434/api/version

# Check if process is running
ps aux | grep ollama

# Start Ollama (Linux/macOS)
ollama serve

# Start Ollama (Windows)
# Run Ollama from Start Menu
```

### Ollama Timeout / Very Slow Responses

**Symptoms**: Commands hang, timeouts after 30-60 seconds

**Common Causes**:
1. **Model not loaded in memory** - First request loads model (20-40s)
2. **WSL performance issues** - Ollama runs slower in WSL
3. **CPU/RAM limitations** - System lacks resources

**Solutions**:

```bash
# 1. Check if model is loaded
curl http://localhost:11434/api/ps

# 2. Try smaller/faster model
ollama pull tinyllama
kp-codeagent --model tinyllama run "test task"

# 3. Pre-load model in memory (wait 30-40s)
ollama run phi:latest "hello"

# 4. Restart Ollama
sudo systemctl restart ollama  # or pkill ollama && ollama serve

# 5. Use demo mode (no AI required)
python3 demo_sin_ia.py
```

**WSL-Specific Issues**:
- Ollama can be 2-3x slower in WSL compared to native Windows/Linux
- Consider installing Ollama in Windows and connecting from WSL
- Or use the demo mode for development/testing

### Model Not Found
```bash
# Download the model
ollama pull codellama:7b

# Verify it's available
ollama list

# Check model is accessible
ollama run codellama:7b "test"
```

### Python Not Found
```bash
# Verify Python installation
python3 --version  # Should show Python 3.10+

# If not found, install
sudo apt install python3 python3-pip  # Debian/Ubuntu
```

### Permission Errors
```bash
# Linux/macOS: Use sudo if needed
sudo pip install -r requirements.txt

# Windows: Run terminal as Administrator

# Or install in user space
pip install --user -r requirements.txt
```

### Installation Issues
```bash
# Clear pip cache
pip cache purge

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version
python3 --version  # Must be 3.10+
```

### Response Times by Model

Expected response times for simple queries:

| Model | First Load | Subsequent | RAM Usage |
|-------|-----------|------------|-----------|
| tinyllama | 15-25s | 3-8s | 1-2 GB |
| phi:latest | 20-40s | 5-15s | 2-3 GB |
| codellama:7b | 30-60s | 10-30s | 4-6 GB |

**Note**: WSL may be 2-3x slower. First request loads model into memory.

## 📚 Project Structure

```
kp-codeagent/
├── kp_codeagent/             # Main package
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # Command-line interface
│   ├── agent.py              # Core agent logic
│   ├── ollama_client.py      # Ollama API wrapper
│   ├── file_handler.py       # Safe file operations
│   ├── context_builder.py    # Project context analysis
│   ├── prompts.py            # System prompts
│   ├── i18n.py               # Internationalization
│   ├── utils.py              # Utility functions
│   └── translations/         # Language files
│       ├── en.json           # English translations
│       └── es.json           # Spanish translations
├── tests/                    # Test suite
│   └── test_basic.py         # Basic tests
├── setup.py                  # Setup configuration
├── requirements.txt          # Python dependencies
├── test_ollama.py            # Quick Ollama diagnostics
├── test_ollama_detallado.sh  # Detailed bash diagnostics
├── demo_sin_ia.py            # Demo mode (no AI needed)
├── diagnostico_ollama.md     # Troubleshooting guide
└── README.md                 # This file
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs**: Open an issue describing the problem
2. **Suggest Features**: Share ideas for new capabilities
3. **Submit PRs**: Fix bugs or add features
4. **Improve Docs**: Help make documentation better

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Ollama** - For making local LLM inference easy
- **Meta AI** - For the CodeLlama model
- **Rich** - For beautiful terminal formatting
- **Click** - For CLI argument parsing

## 💬 Support

- **Documentation**: Check this README and inline help
- **Issues**: https://github.com/kp-codeagent/kp-codeagent/issues
- **Discussions**: https://github.com/kp-codeagent/kp-codeagent/discussions

## 🗺️ Roadmap

- [ ] Multi-turn conversations
- [ ] Automatic test generation
- [ ] Code review mode
- [ ] Git integration
- [ ] Project templates
- [ ] VS Code extension
- [ ] Web UI interface
- [ ] Support for more models (GPT4All, etc.)

## ⚡ Performance Tips

1. **Use 7B model** for faster responses on smaller machines
2. **Close other applications** to free up RAM
3. **Limit project size** by using `.gitignore` properly
4. **Use specific tasks** to reduce context size
5. **Restart Ollama** if responses slow down

---

**Made with ❤️ for students learning to code**

*KP Code Agent - Your local AI coding companion*
