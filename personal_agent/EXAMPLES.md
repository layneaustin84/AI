# Personal Agent - Examples & Use Cases

This document provides practical examples for using your Personal Agent with real-world scenarios.

## Setup (One-Time)

```bash
cd personal_agent

# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env
cp .env.example .env

# ⚠️ Edit .env and add your GEMINI_API_KEY
nano .env  # or your favorite editor
```

---

## Example 1: Humanize an OSHA Report

**Scenario:** You've written a draft safety incident report and want to make it more professional and compliant.

**Input file:** `sample_documents/draft_report.txt`

**Command:**
```bash
python cli.py humanize --file sample_documents/draft_report.txt --tone osha_formal --output humanized_report.txt
```

**What happens:**
1. CLI reads `draft_report.txt`
2. Applies "osha_formal" tone profile (regulatory language, safety focus)
3. Saves result to `humanized_report.txt`
4. Logs operation to `logs/operations.jsonl`

**Expected output:** More formal, regulation-compliant language with stronger emphasis on corrective actions and safety protocols.

---

## Example 2: Create a LinkedIn Post from Draft

**Scenario:** You have notes about a workplace safety initiative and want to turn them into an engaging LinkedIn post.

**Command:**
```bash
python cli.py humanize "Our team just implemented a new safety inspection protocol that reduced incident reports by 40%. Here's how we did it: 1) Trained all staff 2) Created checklists 3) Monthly audits. Proud of our commitment to workplace safety!" --tone linkedin_casual
```

**What happens:**
1. CLI receives text from command line
2. Applies "linkedin_casual" tone (conversational, engaging, professional)
3. Outputs to terminal
4. You can copy/paste the result

---

## Example 3: Batch Process Multiple Documents

**Scenario:** You have 10 safety reports that all need to be formatted for OSHA compliance.

**Setup:**
```bash
# Create a directory with your draft reports
mkdir documents/
# Copy your 10 .txt files into documents/
```

**Command:**
```bash
python cli.py batch documents/ --tone osha_formal --preserve-names
```

**What happens:**
1. Finds all `.txt` files in `documents/` directory
2. Humanizes each one with osha_formal tone
3. Saves output files as `filename_humanized.txt`
4. Shows progress: `[1/10] Processing report1.txt... ✅`
5. Summary: `Completed: 10/10 files processed`
6. Output files go to `output/` directory

---

## Example 4: Extract Key Takeaways

**Scenario:** You have a long safety training document and want to extract the main points.

**Command:**
```bash
python cli.py takeaways "Your long training document text here..."
```

**Or from file:**
```bash
python cli.py takeaways "$(cat training_doc.txt)"
```

**What happens:**
1. CLI sends text to Gemini API
2. API extracts key takeaways as a bulleted list
3. Outputs to terminal

---

## Example 5: Summarize a Report

**Scenario:** You need a quick summary of a long incident investigation.

**Command:**
```bash
python cli.py summarize "Full investigation text here..."
```

**Or read from file:**
```bash
python cli.py summarize "$(cat investigation_report.txt)"
```

---

## Example 6: Document Type Auto-Detection

**Scenario:** You don't want to remember which tone to use - let the agent pick based on document type.

**Command:**
```bash
# Automatically uses osha_formal (default for "report" type)
python cli.py humanize --file safety_report.txt --doc-type report

# Automatically uses linkedin_casual (default for "social" type)
python cli.py humanize --file post_draft.txt --doc-type social

# Automatically uses technical (default for "code" type)
python cli.py humanize --file api_docs.txt --doc-type code
```

---

## Example 7: Add Custom Instructions

**Scenario:** You want the default tone, but with a custom instruction.

**Command:**
```bash
python cli.py humanize --file draft.txt --tone osha_formal \
  --instruction "Emphasize employee training requirements and add specific dates for implementation"
```

**What happens:**
1. Loads osha_formal tone profile
2. Appends your custom instruction to the system prompt
3. Gemini uses both the tone profile AND your custom instruction

---

## Example 8: Save Output to File

**Scenario:** You want to keep the humanized version for records.

**Command:**
```bash
python cli.py humanize --file draft.txt --tone osha_formal --output final_report.txt
```

**What happens:**
1. Processes text
2. Saves to `final_report.txt` in current directory
3. Shows confirmation: `✅ Output saved to: final_report.txt`

---

## Example 9: View Operation History

**Scenario:** You want to see what operations have been performed.

**Python code:**
```python
from file_handler import FileHandler
from config_loader import ConfigLoader

config = ConfigLoader()
handler = FileHandler(config)

# Get last 10 operations
history = handler.get_operation_history(limit=10)
for operation in history:
    print(f"[{operation['timestamp']}] {operation['operation']} - {operation['tone_profile']}")
```

**Or view raw log:**
```bash
tail logs/operations.jsonl
```

---

## Example 10: Check Usage Statistics

**Python code:**
```python
from file_handler import FileHandler
from config_loader import ConfigLoader

config = ConfigLoader()
handler = FileHandler(config)

stats = handler.get_stats()
print(f"Total operations: {stats['total_operations']}")
print(f"Avg input length: {stats['avg_input_length']}")
print(f"Avg output length: {stats['avg_output_length']}")
print(f"Compression ratio: {stats['compression_ratio']}")
```

---

## Real-World Workflow Example

**Scenario:** Daily safety report processing workflow

```bash
#!/bin/bash
# daily_process.sh

echo "🔄 Daily Safety Report Processing"

# 1. Check for new reports
NEW_REPORTS=$(find ./incoming --name "*.txt" -mtime -1)

if [ -z "$NEW_REPORTS" ]; then
    echo "No new reports today"
    exit 0
fi

# 2. Process each report
python cli.py batch ./incoming --tone osha_formal \
    --output-dir ./processed \
    --preserve-names

# 3. Archive originals
mkdir -p ./archive
mv ./incoming/*.txt ./archive/

# 4. Show statistics
python -c "
from file_handler import FileHandler
from config_loader import ConfigLoader
config = ConfigLoader()
handler = FileHandler(config)
stats = handler.get_stats()
print(f'\\n✅ Processing complete')
print(f'Total operations: {stats[\"total_operations\"]}')
"

echo "📧 Ready to email processed reports"
```

**Run daily:**
```bash
chmod +x daily_process.sh
./daily_process.sh
```

---

## Tone Profile Comparison

See the same text in different tones:

**Original:**
> "The safety inspection found three broken emergency lights and a missing first aid kit."

**osha_formal:**
> "The facility inspection identified three non-compliant emergency lighting units and a missing first aid station, presenting potential OSHA violations and requiring immediate corrective action."

**linkedin_casual:**
> "During our safety check today, we discovered some maintenance items that needed attention - a few emergency lights and a first aid kit that need replacing. Great reminder of why regular inspections matter! 🔍✅"

**technical:**
> "The inspection audit revealed 3x emergency lighting fixtures (model XYZ) non-functional and 1x first aid station missing required supplies. Recommendation: Replace fixtures per specification 2.4.1 and restock per OSHA 1910.151(b)."

**executive_summary:**
> "Safety inspection identified critical maintenance issues requiring immediate attention: emergency lighting and first aid station gaps. Estimated remediation time: 4 hours."

**friendly:**
> "We just did a safety walk-through and found a couple of things to fix - some emergency lights aren't working and we need to restock our first aid kit. Nothing serious, and we're on it!"

---

## Tips & Best Practices

### 1. Always Verify Output
Start with short texts to understand each tone profile before processing large batches.

### 2. Create Backups
Keep originals before batch processing:
```bash
cp -r documents documents_backup
python cli.py batch documents --tone osha_formal
```

### 3. Use Document Types
Let the agent choose the tone when possible:
```bash
python cli.py humanize --file document.txt --doc-type report
```

### 4. Stack Custom Instructions
For complex needs, stack the tone profile with a custom instruction:
```bash
python cli.py humanize --file doc.txt --tone osha_formal \
  --instruction "Also ensure all dates are in YYYY-MM-DD format and add implementation deadlines"
```

### 5. Monitor Operations Log
Check `logs/operations.jsonl` to track usage and identify patterns.

### 6. Automate with Cron
Schedule daily report processing:
```bash
0 9 * * * /home/user/AI/personal_agent/daily_process.sh
```

---

## Troubleshooting

### Error: "GEMINI_API_KEY not set"
**Solution:** Edit `.env` and add your API key:
```bash
nano .env
# Add: GEMINI_API_KEY=your_actual_key_here
```

### Error: "Tone profile not found"
**Solution:** List available profiles:
```bash
python cli.py profiles
```

### Error: "No files matching pattern"
**Solution:** Verify directory path and file extensions:
```bash
ls documents/  # Check files exist
python cli.py batch documents --pattern "*.txt"  # Check pattern
```

### Slow Processing
**Reason:** Gemini API rate limiting
**Solution:** Process in smaller batches or add delays between requests

---

## Next Steps

1. ✅ Run your first humanization
2. ✅ Try different tone profiles
3. ✅ Process a batch of documents
4. ✅ Check your operation history
5. 🎯 Automate daily workflows
6. 🔧 Extend with custom tone profiles
7. 🚀 Build the web dashboard (coming next!)

Good luck with your Personal Agent! 🚀
