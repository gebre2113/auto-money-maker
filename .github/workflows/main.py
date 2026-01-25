name: Profit Master Supreme v12.0 - Ultimate AI Ecosystem

on:
  # 1. በየጊዜው በራሱ እንዲነሳ (Schedules)
  schedule:
    - cron: '*/30 * * * *'  # በየ30 ደቂቃው
    - cron: '0 */3 * * *'    # በየ3 ሰዓቱ
    - cron: '0 0 1 * *'      # በወር አንድ ጊዜ
  
  # 2. የማስጀመሪያ ቁልፍ (Manual Trigger)
  workflow_dispatch:
    inputs:
      action_type:
        description: 'የማስኬድ አይነት'
        required: true
        default: 'full_cycle'
        type: choice
        options:
          - content_generation
          - full_cycle
          - emergency_recovery

jobs:
  profit-engine:
    runs-on: ubuntu-latest
    timeout-minutes: 60  # ለትልቅ ስክሪፕት ጊዜ መጨመር አስፈላጊ ነው
    
    steps:
    - name: "📥 ኮድ ማውረድ"
      uses: actions/checkout@v4
      
    - name: "🐍 Python ማዘጋጀት"
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        cache: 'pip' # ፍጥነት ለመጨመር
        
    - name: "📦 ጥገኛ ፓኬጆች መጫን"
      run: |
        python -m pip install --upgrade pip
        pip install feedparser requests google-genai groq tweepy pandas openai
        # ሌሎች አስፈላጊ ላይብረሪዎችን እዚህ ይጨምሩ
        
    - name: "🚀 Profit Master ማስኬድ"
      env:
        # ሚስጥራዊ ቁልፎችን ከ Secrets መጥራት
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
        WORDPRESS_URL: ${{ secrets.WORDPRESS_URL }}
        WORDPRESS_USER: ${{ secrets.WORDPRESS_USER }}
        WORDPRESS_PASSWORD: ${{ secrets.WORDPRESS_PASSWORD }}
      run: |
        # 10,000 መስመር ያለውን ዋናውን ፋይል መጥራት
        python profit_master.py --auto
        
    - name: "📊 ውጤት ማስቀመጥ (Artifacts)"
      if: always() # ስህተት ቢኖርም ሪፖርቱን እንዲያወርድ
      uses: actions/upload-artifact@v4
      with:
        name: profit-master-results
        path: |
          *.log
          reports/
          automation_log.json
