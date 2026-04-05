#!/bin/bash

# Personal Agent Setup Script

echo "🚀 Personal Agent Setup"
echo "======================="

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "✓ Python version: $python_version"

# Create virtual environment (optional)
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
else
    source venv/bin/activate
    echo "✓ Using existing virtual environment"
fi

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Setup .env file
if [ ! -f ".env" ]; then
    echo "⚙️  Setting up .env file..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env and add your GEMINI_API_KEY"
    echo "✓ .env file created from .env.example"
else
    echo "✓ .env file already exists"
fi

# Create necessary directories
mkdir -p output logs
echo "✓ Created output and logs directories"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env and add your GEMINI_API_KEY"
echo "2. Run: python cli.py profiles"
echo "3. Try: python cli.py humanize 'Your text here'"
echo ""
