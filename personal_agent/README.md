# Personal Agent

An AI-powered text transformation CLI tool built with Google's Gemini API. Transform your writing with intelligent tone adjustment, humanization, and batch processing.

## Features

✨ **Humanize Text** - Make any text sound more natural and engaging
🎯 **Tone Profiles** - Pre-configured tones for OSHA, LinkedIn, technical docs, executive summaries, and more
📁 **Batch Processing** - Process multiple files at once
📊 **Version Logging** - Track all operations and maintain audit trail
⚡ **CLI-first** - Powerful command-line interface for automation

## Quick Start

### 1. Setup

```bash
cd personal_agent
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure API Key

Edit `.env` and add your Google Gemini API key:

```
GEMINI_API_KEY=your_key_here
```

### 3. Run Commands

```bash
# Humanize text with a specific tone
python cli.py humanize "Your text here" --tone linkedin_casual

# Humanize from a file
python cli.py humanize --file report.txt --tone osha_formal --output humanized.txt

# Batch process all .txt files in a directory
python cli.py batch ./documents --tone osha_formal

# List available tone profiles
python cli.py profiles

# Summarize text
python cli.py summarize "Your text here"
```

## Available Tone Profiles

- **osha_formal** - Professional, safety-focused, regulatory-compliant
- **linkedin_casual** - Engaging, conversational, social-media friendly
- **technical** - Precise, implementation-focused for engineers
- **executive_summary** - Concise, decision-focused for leadership
- **friendly** - Warm, welcoming, human-centered

## Available Commands

### humanize
Transform text using a specified tone profile.

```bash
python cli.py humanize [TEXT] [OPTIONS]

Options:
  --tone, -t TEXT          Tone profile to use (default: friendly)
  --file, -f PATH          Read text from file
  --doc-type, -d TEXT      Document type for auto-profile selection
  --instruction, -i TEXT   Custom instruction to append
  --output, -o PATH        Save output to file
```

### batch
Batch process multiple files in a directory.

```bash
python cli.py batch DIRECTORY [OPTIONS]

Options:
  --tone, -t TEXT          Tone profile to use
  --pattern, -p TEXT       File pattern to match (default: *.txt)
  --output-dir, -o PATH    Directory for output files
  --preserve-names         Preserve original filenames (adds suffix)
```

### profiles
List all available tone profiles.

```bash
python cli.py profiles
```

### types
List document types and their default profiles.

```bash
python cli.py types
```

### summarize
Summarize text to key points.

```bash
python cli.py summarize TEXT
```

### takeaways
Extract key takeaways from text.

```bash
python cli.py takeaways TEXT
```

## File Structure

```
personal_agent/
├── cli.py                  # Main CLI interface
├── config_loader.py        # Configuration management
├── gemini_wrapper.py       # Gemini API wrapper
├── file_handler.py         # File operations & logging
├── config/
│   └── tone_profiles.json  # Tone profile definitions
├── output/                 # Output files directory
├── logs/                   # Logs directory
│   └── operations.jsonl    # Operation history
└── requirements.txt        # Python dependencies
```

## Examples

### Example 1: Humanize an OSHA Report

```bash
python cli.py humanize --file osha_draft.txt --tone osha_formal --output osha_final.txt
```

### Example 2: Convert Draft Emails to Professional

```bash
python cli.py humanize --file draft_email.txt --tone linkedin_casual
```

### Example 3: Batch Process All Reports

```bash
python cli.py batch ./reports --tone osha_formal --preserve-names
```

### Example 4: Get Key Takeaways

```bash
python cli.py takeaways "Your long document text here"
```

## Architecture

The Personal Agent is built on a modular architecture:

1. **CLI Layer** (`cli.py`) - User-facing commands
2. **Config Layer** (`config_loader.py`) - Tone profiles & settings
3. **API Layer** (`gemini_wrapper.py`) - Gemini API integration
4. **File Layer** (`file_handler.py`) - I/O and logging

```
User Input
   ↓
CLI Commands
   ↓
Config Loader (tone profiles, API key)
   ↓
Gemini API Wrapper
   ↓
File Handler (output, logging)
```

## Logging

All operations are logged to `logs/operations.jsonl` for audit trails:

```json
{
  "timestamp": "2024-11-12T10:30:45.123456",
  "operation": "humanize",
  "input_length": 250,
  "output_length": 200,
  "tone_profile": "osha_formal",
  "doc_type": "report"
}
```

## Extending the Agent

### Add a New Tone Profile

Edit `config/tone_profiles.json`:

```json
{
  "profiles": {
    "my_custom_tone": {
      "name": "My Custom Tone",
      "description": "Description of this tone",
      "system_prompt": "System prompt for Gemini...",
      "tone_keywords": ["keyword1", "keyword2"],
      "use_cases": ["Use case 1", "Use case 2"]
    }
  }
}
```

### Add a New CLI Command

Add a new command to `cli.py`:

```python
@cli.command()
@click.argument('text')
def my_command(text):
    """Your command description."""
    agent = PersonalAgent()
    # Your implementation
    pass
```

## Environment Variables

- `GEMINI_API_KEY` - Google Gemini API key (required)
- `LOG_LEVEL` - Logging level (default: INFO)
- `OUTPUT_DIR` - Directory for output files (default: ./output)
- `LOGS_DIR` - Directory for logs (default: ./logs)

## Requirements

- Python 3.8+
- click (CLI framework)
- requests (HTTP client)
- python-dotenv (Environment management)

## Version History

- **v1.0.0** - Initial release with humanize, batch processing, and tone profiles

## Future Enhancements

- [ ] Web dashboard interface
- [ ] Tone profile learning from user edits
- [ ] Queue system for large batch jobs
- [ ] Integration with existing Humanizer web app
- [ ] Database storage for operation history
- [ ] Multi-language support
- [ ] Custom model selection
