from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, movie, global_stats

app = FastAPI(title="Hive Movie Dashboard API")

# --- Enable CORS for React ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(movie.router)
app.include_router(global_stats.router)

