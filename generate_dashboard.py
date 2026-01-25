import json
with open('ai_report.json', 'r') as f: data = json.load(f)

cards = ""
for art in data.get('articles', []):
    cards += f"""
    <div class="col-md-6 mb-4">
        <div class="card shadow border-0">
            <div class="card-body">
                <h5 class="fw-bold">{art['topic']}</h5>
                <span class="badge bg-success">Quality: {art['quality']}%</span>
                <hr>
                <a href="articles/{art['filename']}" class="btn btn-primary w-100">📖 Read & Listen</a>
            </div>
        </div>
    </div>
    """

html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Profit Master v12.3</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <h1 class="text-center mb-5">🚀 Profit Master v12.3</h1>
        <div class="row">{cards}</div>
    </div>
</body>
</html>
"""
with open('index.html', 'w') as f: f.write(html)
