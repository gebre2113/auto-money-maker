#!/bin/bash
# setup.sh - ለመጀመሪያ ጊዜ የስርዓት ማዋቀር

echo "🚀 Setting up Profit Master System..."

# 1. Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Upgrade pip
pip install --upgrade pip

# 3. Install dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# 4. Install PyTorch separately
echo "🤖 Installing PyTorch..."
pip install torch --index-url https://download.pytorch.org/whl/cpu

# 5. Download NLTK data
echo "📚 Downloading NLTK data..."
python -c "
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
print('NLTK data downloaded')
"

# 6. Create necessary directories
mkdir -p generated_content
mkdir -p output
mkdir -p logs

echo "✅ Setup completed!"
echo "📁 Directories created:"
echo "   - generated_content/"
echo "   - output/"
echo "   - logs/"
echo ""
echo "🚀 To run the system:"
echo "   source venv/bin/activate"
echo "   python main.py --topic 'Your Topic' --language 'am'"
