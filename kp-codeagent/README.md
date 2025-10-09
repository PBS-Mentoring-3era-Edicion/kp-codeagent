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

## 🚀 Quick Start

### Installation (5 minutes)

#### Windows
```bash
# Download the repository
git clone https://github.com/kp-codeagent/kp-codeagent.git
cd kp-codeagent

# Run installer
installer\install.bat
```

#### Linux / macOS / WSL
```bash
# Download the repository
git clone https://github.com/kp-codeagent/kp-codeagent.git
cd kp-codeagent

# Run installer
chmod +x installer/install.sh
./installer/install.sh
```

#### Manual Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install and start Ollama
# Visit: https://ollama.ai/download

# Download CodeLlama model
ollama pull codellama:7b

# Install KP Code Agent
pip install -e .
```

### First Use

1. **Check if everything is ready**:
   ```bash
   kp-codeagent check
   ```

2. **Run your first task**:
   ```bash
   kp-codeagent "create a Python function to calculate fibonacci numbers"
   ```

3. **Review and confirm the changes** when prompted

## 📖 Usage

### Basic Command
```bash
kp-codeagent "your task description here"
```

### Examples

**Create new code**:
```bash
kp-codeagent "create a Python function that validates email addresses"
```

**Modify existing code**:
```bash
kp-codeagent "add error handling to the login function in auth.py"
```

**Fix bugs**:
```bash
kp-codeagent "fix the null pointer error in main.java"
```

**Add features**:
```bash
kp-codeagent "add a dark mode toggle to the settings page"
```

**Refactor code**:
```bash
kp-codeagent "refactor the database connection code to use connection pooling"
```

### Advanced Options

```bash
# Use a different model
kp-codeagent --model codellama:13b "your task"

# Adjust creativity (0.0 = focused, 1.0 = creative)
kp-codeagent --temperature 0.3 "your task"

# Enable verbose mode for debugging
kp-codeagent --verbose "your task"

# Modify a specific file
kp-codeagent modify path/to/file.py "add input validation"
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

### Ollama Not Running
```bash
# Check Ollama status
curl http://localhost:11434

# Start Ollama (Linux/macOS)
ollama serve

# Start Ollama (Windows)
# Run Ollama from Start Menu
```

### Model Not Found
```bash
# Download the model
ollama pull codellama:7b

# Verify it's available
ollama list
```

### Python Not Found
```bash
# Verify Python installation
python --version  # or python3 --version

# Should show Python 3.10+
```

### Permission Errors
```bash
# Linux/macOS: Use sudo if needed
sudo pip install -r requirements.txt

# Windows: Run terminal as Administrator
```

### Installation Issues
```bash
# Clear pip cache
pip cache purge

# Reinstall
pip install -r requirements.txt --force-reinstall
```

## 📚 Project Structure

```
kp-codeagent/
├── src/
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # Command-line interface
│   ├── agent.py              # Core agent logic
│   ├── ollama_client.py      # Ollama API wrapper
│   ├── file_handler.py       # Safe file operations
│   ├── context_builder.py    # Project context analysis
│   ├── prompts.py            # System prompts
│   └── utils.py              # Utility functions
├── installer/
│   ├── install.bat           # Windows installer
│   └── install.sh            # Linux/macOS installer
├── tests/                    # Test suite
├── pyproject.toml            # Project configuration
├── requirements.txt          # Python dependencies
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
