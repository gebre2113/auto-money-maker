import json
with open('ai_report.json', 'r') as f: data = json.load(f)

cards = ""
for art in data.get('articles', []):
    cards += f"""
    <div class="col-md-6 mb-4">
        <div class="card h-100 shadow border-0" style="border-radius: 15px; overflow: hidden;">
            <div class="card-body text-center p-5">
                <h3 class="fw-bold mb-3">{art['topic']}</h3>
                <a href="articles/{art['filename']}" class="btn btn-outline-dark btn-lg rounded-pill px-5">Read Now ➔</a>
            </div>
        </div>
    </div>
    """

html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Profit Master v12.5</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background: linear-gradient(120deg, #f6d365 0%, #fda085 100%); min-height: 100vh; font-family: 'Segoe UI', sans-serif; }}
        .container {{ background: rgba(255,255,255,0.9); border-radius: 20px; padding: 40px; margin-top: 50px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-5">🚀 Profit Master v12.5</h1>
        <h3 class="text-center mb-5">Revenue: ${data.get('revenue', 0):.2f}</h3>
        <div class="row">{cards}</div>
    </div>
</body>
</html>
"""
with open('index.html', 'w') as f: f.write(html)
