"""
Comprehensive database diagnostic script.
This script will identify and help fix common database setup issues.
"""
import os
import sys
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def check_environment_variables():
    """Check if all required environment variables are set"""
    logger.info("\n" + "=" * 60)
    logger.info("STEP 1: Checking Environment Variables")
    logger.info("=" * 60)
    
    required_vars = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Hide password
            display_value = "***" if var == "DB_PASSWORD" else value
            logger.info(f"✅ {var} = {display_value}")
        else:
            logger.error(f"❌ {var} is not set!")
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"\n⚠️  Missing variables: {', '.join(missing_vars)}")
        logger.error("   Please create a .env file with these variables")
        return False
    
    logger.info("\n✅ All environment variables are set!")
    return True


def check_postgresql_connection():
    """Check if PostgreSQL is accessible"""
    logger.info("\n" + "=" * 60)
    logger.info("STEP 2: Testing PostgreSQL Connection")
    logger.info("=" * 60)
    
    try:
        import psycopg2
        
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "electronics_db")
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "password")
        
        logger.info(f"Connecting to: {db_user}@{db_host}:{db_port}/{db_name}")
        
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        logger.info(f"✅ PostgreSQL connection successful!")
        logger.info(f"   Version: {version.split(',')[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        logger.error("❌ psycopg2 is not installed!")
        logger.error("   Run: pip install psycopg2-binary")
        return False
    except Exception as e:
        logger.error(f"❌ PostgreSQL connection failed: {e}")
        logger.error("\nPossible solutions:")
        logger.error("   1. Check if PostgreSQL is running")
        logger.error("   2. Verify database exists: CREATE DATABASE ecommerce_db;")
        logger.error("   3. Check credentials in .env file")
        logger.error("   4. Check firewall/network settings")
        return False


def check_sqlalchemy_setup():
    """Check SQLAlchemy setup"""
    logger.info("\n" + "=" * 60)
    logger.info("STEP 3: Checking SQLAlchemy Setup")
    logger.info("=" * 60)
    
    try:
        from app.database import engine, Base, DATABASE_URL
        
        # Hide password in URL
        safe_url = DATABASE_URL.replace(os.getenv("DB_PASSWORD", ""), "***")
        logger.info(f"Database URL: {safe_url}")
        
        # Test engine connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            logger.info("✅ SQLAlchemy engine is working!")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("   Check if app.database module exists")
        return False
    except Exception as e:
        logger.error(f"❌ SQLAlchemy setup error: {e}")
        return False


def check_models_import():
    """Check if models can be imported"""
    logger.info("\n" + "=" * 60)
    logger.info("STEP 4: Checking Models Import")
    logger.info("=" * 60)
    
    try:
        from app.models import (
            NguoiDung,
            DanhMuc,
            SanPham,
            DonHang,
            ChiTietDonHang,
            LichSuChat,
        )
        
        logger.info("✅ All models imported successfully!")
        logger.info("   - NguoiDung")
        logger.info("   - DanhMuc")
        logger.info("   - SanPham")
        logger.info("   - DonHang")
        logger.info("   - ChiTietDonHang")
        logger.info("   - LichSuChat")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Model import error: {e}")
        logger.error("   Check if all model files exist in app/models/")
        return False
    except Exception as e:
        logger.error(f"❌ Model error: {e}")
        return False


def check_base_metadata():
    """Check if models are registered with Base"""
    logger.info("\n" + "=" * 60)
    logger.info("STEP 5: Checking Base Metadata")
    logger.info("=" * 60)
    
    try:
        from app.database import Base
        from app.models import (
            NguoiDung,
            DanhMuc,
            SanPham,
            DonHang,
            ChiTietDonHang,
            LichSuChat,
        )
        
        registered_tables = list(Base.metadata.tables.keys())
        
        logger.info(f"📋 Registered tables ({len(registered_tables)}):")
        for table_name in registered_tables:
            logger.info(f"   - {table_name}")
        
        if len(registered_tables) == 0:
            logger.error("❌ No tables registered with Base!")
            logger.error("   Models may not be inheriting from Base correctly")
            return False
        
        expected_tables = [
            "nguoi_dung",
            "danh_muc",
            "san_pham",
            "don_hang",
            "chi_tiet_don_hang",
            "lich_su_chat"
        ]
        
        missing_tables = set(expected_tables) - set(registered_tables)
        if missing_tables:
            logger.warning(f"⚠️  Missing tables: {', '.join(missing_tables)}")
        
        logger.info("✅ Base metadata is configured!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Base metadata error: {e}")
        return False


def create_tables():
    """Create all tables"""
    logger.info("\n" + "=" * 60)
    logger.info("STEP 6: Creating Tables")
    logger.info("=" * 60)
    
    try:
        from app.database import init_db
        
        init_db()
        logger.info("✅ Tables created successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Table creation failed: {e}")
        return False


def verify_tables_in_database():
    """Verify tables exist in database"""
    logger.info("\n" + "=" * 60)
    logger.info("STEP 7: Verifying Tables in Database")
    logger.info("=" * 60)
    
    try:
        from app.database import engine
        
        with engine.connect() as conn:
            result = conn.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            existing_tables = [row[0] for row in result]
        
        logger.info(f"📊 Tables in database ({len(existing_tables)}):")
        for table in existing_tables:
            logger.info(f"   - {table}")
        
        if len(existing_tables) == 0:
            logger.error("❌ No tables found in database!")
            logger.error("   Tables were not created successfully")
            return False
        
        logger.info("✅ Tables verified in database!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Table verification failed: {e}")
        return False


def main():
    """Run all diagnostic checks"""
    logger.info("\n" + "🔍" * 30)
    logger.info("DATABASE DIAGNOSTIC TOOL")
    logger.info("🔍" * 30)
    
    checks = [
        ("Environment Variables", check_environment_variables),
        ("PostgreSQL Connection", check_postgresql_connection),
        ("SQLAlchemy Setup", check_sqlalchemy_setup),
        ("Models Import", check_models_import),
        ("Base Metadata", check_base_metadata),
        ("Table Creation", create_tables),
        ("Table Verification", verify_tables_in_database),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
            
            if not result:
                logger.error(f"\n⚠️  {check_name} failed. Stopping diagnostics.")
                break
                
        except Exception as e:
            logger.error(f"\n❌ Unexpected error in {check_name}: {e}")
            results.append((check_name, False))
            break
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("DIAGNOSTIC SUMMARY")
    logger.info("=" * 60)
    
    for check_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        logger.info(f"{check_name:.<40} {status}")
    
    all_passed = all(result[1] for result in results)
    
    logger.info("=" * 60)
    if all_passed:
        logger.info("🎉 ALL CHECKS PASSED!")
        logger.info("   Your database is properly configured and ready to use.")
        logger.info("\n   Next steps:")
        logger.info("   1. Run: python run.py")
        logger.info("   2. Visit: http://localhost:8000/docs")
    else:
        logger.error("⚠️  SOME CHECKS FAILED!")
        logger.error("   Please fix the issues above and run this script again.")
    logger.info("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
