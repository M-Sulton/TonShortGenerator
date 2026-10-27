import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPSTREAM_DIR = os.path.join(BASE_DIR, "upstream_openshorts")
if UPSTREAM_DIR not in sys.path:
    sys.path.insert(0, UPSTREAM_DIR)

os.chdir(UPSTREAM_DIR)

# Import the original app from openshorts
from app import app
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

dashboard_dist = os.path.join(UPSTREAM_DIR, "dashboard", "dist")

# Mount fonts and static dist files directly at root so asset links resolve cleanly
if os.path.exists(dashboard_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(dashboard_dist, "assets")), name="dist_assets")
    if os.path.exists(os.path.join(dashboard_dist, "fonts")):
        app.mount("/fonts", StaticFiles(directory=os.path.join(dashboard_dist, "fonts")), name="dist_fonts")

    @app.get("/fonts.css")
    async def get_fonts_css():
        return FileResponse(os.path.join(dashboard_dist, "fonts.css"))

    @app.get("/logo-openshorts.png")
    async def get_logo():
        return FileResponse(os.path.join(dashboard_dist, "logo-openshorts.png"))

    @app.get("/vite.svg")
    async def get_vite():
        return FileResponse(os.path.join(dashboard_dist, "vite.svg"))

    @app.get("/dashboard")
    @app.get("/dashboard/")
    @app.get("/")
    async def serve_dashboard():
        return FileResponse(os.path.join(dashboard_dist, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3015)
