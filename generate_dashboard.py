import json, os

def create_dashboard():
    try:
        with open('ai_report.json', 'r') as f:
            data = json.load(f)
    except:
        data = {"revenue_projected": 0, "articles": []}

    article_html = ""
    for art in data.get('articles', []):
        article_html += f"""
        <div class="col-md-6 mb-4">
            <div class="card h-100 shadow-sm border-0">
                <img src="https://source.unsplash.com/600x300/?business,{art['topic'].split()[0]}" class="card-img-top" style="height: 200px; object-fit: cover;">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span class="badge bg-primary">Premium</span>
                        <small class="text-muted">Audio Available 🎧</small>
                    </div>
                    <h5 class="card-title fw-bold">{art['topic']}</h5>
                    <p class="card-text text-muted">A comprehensive guide covering advanced strategies for 2026...</p>
                    <div class="d-grid">
                        <a href="articles/{art['filename']}" class="btn btn-dark">Read & Listen Now</a>
                    </div>
                </div>
            </div>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Profit Master Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #f0f2f5; font-family: 'Segoe UI', sans-serif; }}
            .hero {{ background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: white; padding: 80px 0; border-radius: 0 0 50px 50px; margin-bottom: 50px; }}
            .stat-box {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); text-align: center; transition: transform 0.3s; }}
            .stat-box:hover {{ transform: translateY(-5px); }}
            .icon-circle {{ width: 60px; height: 60px; background: #e3f2fd; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; color: #2196f3; font-size: 24px; }}
        </style>
    </head>
    <body>
        <div class="hero text-center">
            <h1 class="display-4 fw-bold">🚀 Profit Master v12.2</h1>
            <p class="lead">Automated AI Content & Monetization Engine</p>
        </div>
        
        <div class="container" style="margin-top: -80px;">
            <!-- STATS -->
            <div class="row mb-5">
                <div class="col-md-4 mb-3">
                    <div class="stat-box">
                        <div class="icon-circle"><i class="fas fa-dollar-sign"></i></div>
                        <h2 class="fw-bold text-success">${data.get('revenue_projected', 0):.2f}</h2>
                        <span class="text-muted">Projected Revenue</span>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="stat-box">
                        <div class="icon-circle"><i class="fas fa-newspaper"></i></div>
                        <h2 class="fw-bold">{len(data.get('articles', []))}</h2>
                        <span class="text-muted">New Articles</span>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="stat-box">
                        <div class="icon-circle"><i class="fas fa-chart-line"></i></div>
                        <h2 class="fw-bold text-primary">96%</h2>
                        <span class="text-muted">System Efficiency</span>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-12 mb-4">
                    <h3 class="fw-bold border-start border-5 border-primary ps-3">🔥 Latest Premium Content</h3>
                </div>
                {article_html}
            </div>
            
            <footer class="text-center mt-5 py-4 text-muted border-top">
                &copy; 2026 Profit Master Supreme • Auto-Generated
            </footer>
        </div>
    </body>
    </html>
    """
    
    with open('index.html', 'w') as f:
        f.write(html)

if __name__ == "__main__":
    create_dashboard()
