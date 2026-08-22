from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import predict, vendors, procurement, risk, financial, score, contracts

app = FastAPI(title="ProcuraIQ API", version="1.0.0")

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(predict.router, prefix="/api/predict", tags=["Predict"])
app.include_router(vendors.router, prefix="/api/vendors", tags=["Vendors"])
app.include_router(procurement.router, prefix="/api/procurement", tags=["Procurement"])
app.include_router(risk.router, prefix="/api/risk", tags=["Risk"])
app.include_router(financial.router, prefix="/api/financial", tags=["Financial"])
app.include_router(score.router, prefix="/api/score", tags=["Scoring"])
app.include_router(contracts.router, prefix="/api/contracts", tags=["Contracts"])

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
