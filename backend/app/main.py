from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import check_db_connection, init_db
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="E-Commerce API",
    description="API cho hệ thống bán thiết bị điện tử",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://frontend:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Run on application startup.
    Check database connection and initialize tables.
    """
    logger.info("=" * 60)
    logger.info("🚀 Starting E-Commerce API Application")
    logger.info("=" * 60)
    
    # Wait for database to be ready
    import time
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        if check_db_connection():
            break
        retry_count += 1
        logger.info(f"⏳ Waiting for database... ({retry_count}/{max_retries})")
        time.sleep(2)
    
    if retry_count >= max_retries:
        logger.error("❌ Could not connect to database after 30 retries")
        return
    
    # Initialize database tables
    try:
        init_db()
        
        # Auto-seed initial data
        from app.database import SessionLocal
        from app.models import DanhMuc, SanPham
        
        db = SessionLocal()
        try:
            # Check if data already exists
            cat_count = db.query(DanhMuc).count()
            prod_count = db.query(SanPham).count()
            
            if cat_count == 0 or prod_count == 0:
                logger.info("🌱 Seeding initial data...")
                import subprocess
                import sys
                result = subprocess.run(
                    [sys.executable, "seed_initial_data.py"],
                    cwd="/app",
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    logger.info("✅ Initial data seeded successfully!")
                else:
                    logger.warning(f"⚠️  Seeding warning: {result.stderr}")
            else:
                logger.info(f"📊 Database already has data: {cat_count} categories, {prod_count} products")
        finally:
            db.close()
        
        logger.info("=" * 60)
        logger.info("✅ Application started successfully!")
        logger.info("📚 API Documentation: http://localhost:8000/docs")
        logger.info("=" * 60)
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        logger.error("⚠️  Application started but database may not be ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("👋 Shutting down application...")


@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "message": "E-Commerce API is running!",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = check_db_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected"
    }


@app.get("/debug/tables")
async def debug_tables():
    """
    Debug endpoint to check database tables.
    Returns current database, registered models, and actual tables in DB.
    """
    from app.database import engine, Base, text, DB_NAME
    
    try:
        # Import all models to ensure they're registered
        from app.models import (
            NguoiDung, DanhMuc, SanPham,
            DonHang, ChiTietDonHang, LichSuChat
        )
        
        # Get registered models
        registered_tables = list(Base.metadata.tables.keys())
        
        # Get actual tables in database
        with engine.connect() as conn:
            # Get current database
            result = conn.execute(text("SELECT current_database()"))
            current_db = result.fetchone()[0]
            
            # Get all tables
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            actual_tables = [row[0] for row in result]
        
        # Check if all expected tables exist
        expected_tables = [
            "nguoi_dung", "danh_muc", "san_pham",
            "don_hang", "chi_tiet_don_hang", "lich_su_chat"
        ]
        missing_tables = set(expected_tables) - set(actual_tables)
        
        return {
            "current_database": current_db,
            "expected_database": DB_NAME,
            "database_correct": current_db == DB_NAME,
            "registered_models": sorted(registered_tables),
            "registered_count": len(registered_tables),
            "actual_tables": sorted(actual_tables),
            "actual_count": len(actual_tables),
            "expected_tables": expected_tables,
            "missing_tables": list(missing_tables),
            "status": "ok" if len(actual_tables) >= 6 and not missing_tables else "incomplete",
            "message": "All tables exist" if not missing_tables else f"Missing: {', '.join(missing_tables)}"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }


# Import and include routers
from app.routers import (
    nguoi_dung_router,
    danh_muc_router,
    san_pham_router,
    don_hang_router,
    chi_tiet_don_hang_router,
    lich_su_chat_router
)

app.include_router(nguoi_dung_router)
app.include_router(danh_muc_router)
app.include_router(san_pham_router)
app.include_router(don_hang_router)
app.include_router(chi_tiet_don_hang_router)
app.include_router(lich_su_chat_router)
