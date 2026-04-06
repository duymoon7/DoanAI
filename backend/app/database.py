from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Database configuration from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "electronics_db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Construct DATABASE_URL based on port (PostgreSQL=5432, MySQL=3306)
if DB_PORT == "5432":
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    DB_DRIVER = "postgresql"
else:
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    DB_DRIVER = "mysql+pymysql"

# Log database configuration (hide password)
logger.info(f"📊 Database Configuration:")
logger.info(f"   Host: {DB_HOST}")
logger.info(f"   Port: {DB_PORT}")
logger.info(f"   Database: {DB_NAME}")
logger.info(f"   User: {DB_USER}")
logger.info(f"   Driver: {DB_DRIVER}")
logger.info(f"   URL: {DB_DRIVER}://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Create SQLAlchemy engine
# pool_pre_ping=True ensures connections are valid before using them
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,  # Set to True for SQL query logging in development
    pool_size=10,  # Maximum number of connections in the pool
    max_overflow=20,  # Maximum overflow connections
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for declarative models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    Yields a database session and ensures it closes after request.
    
    Usage in FastAPI:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database by creating all tables.
    Import all models before calling this function to ensure
    all tables are created.
    """
    logger.info("🔧 Initializing database...")
    
    try:
        # Import all models to register them with Base
        logger.info("📦 Importing models...")
        from app.models import (
            NguoiDung,
            DanhMuc,
            SanPham,
            DonHang,
            ChiTietDonHang,
            LichSuChat,
        )
        
        # Log all registered models
        logger.info(f"✅ Models imported successfully!")
        logger.info(f"📋 Registered models ({len(Base.metadata.tables)} tables):")
        for table_name in Base.metadata.tables.keys():
            logger.info(f"   - {table_name}")
        
        # Create all tables
        logger.info("🔨 Creating tables in database...")
        Base.metadata.create_all(bind=engine)
        
        # Verify tables were created
        with engine.connect() as conn:
            if DB_PORT == "5432":  # PostgreSQL
                result = conn.execute(text("""
                    SELECT tablename 
                    FROM pg_tables 
                    WHERE schemaname = 'public'
                    ORDER BY tablename
                """))
            else:  # MySQL
                result = conn.execute(text(f"""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = '{DB_NAME}'
                    ORDER BY table_name
                """))
            existing_tables = [row[0] for row in result]
            
            logger.info(f"✅ Tables in database ({len(existing_tables)} tables):")
            for table in existing_tables:
                logger.info(f"   - {table}")
        
        logger.info("✅ Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


def check_db_connection() -> bool:
    """
    Check if database connection is working.
    Returns True if connection is successful, False otherwise.
    """
    try:
        logger.info("🔍 Testing database connection...")
        logger.info(f"   Connecting to: {DB_NAME} on {DB_HOST}:{DB_PORT}")
        
        with engine.connect() as connection:
            if DB_PORT == "5432":  # PostgreSQL
                result = connection.execute(text("SELECT version()"))
                version = result.fetchone()[0]
                logger.info(f"✅ Database connection successful!")
                logger.info(f"   PostgreSQL version: {version}")
                logger.info(f"   Database: {DB_NAME}")
            else:  # MySQL
                result = connection.execute(text("SELECT version(), database()"))
                version, current_db = result.fetchone()
                logger.info(f"✅ Database connection successful!")
                logger.info(f"   MySQL version: {version}")
                logger.info(f"   Current database: {current_db}")
                
                if current_db != DB_NAME:
                    logger.warning(f"⚠️  Connected to '{current_db}' but expected '{DB_NAME}'")
                
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        logger.error(f"   Check your .env file and ensure MySQL is running")
        logger.error(f"   Database '{DB_NAME}' may not exist - create it in phpMyAdmin or run: CREATE DATABASE electronics_db;")
        return False


def drop_all_tables() -> None:
    """
    Drop all tables from the database.
    WARNING: This will delete all data!
    Use only for development/testing.
    """
    logger.warning("⚠️  Dropping all tables...")
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ All tables dropped successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to drop tables: {e}")
        raise


def reset_db() -> None:
    """
    Reset database by dropping and recreating all tables.
    WARNING: This will delete all data!
    Use only for development/testing.
    """
    logger.warning("⚠️  Resetting database...")
    drop_all_tables()
    init_db()
    logger.info("✅ Database reset completed!")
