"""
Complete end-to-end script to create electronics_db database and tables.
This script will:
1. Check environment variables
2. Create electronics_db database if it doesn't exist
3. Connect to electronics_db
4. Create all tables
5. Verify everything is working
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


def print_header(title):
    """Print a formatted header"""
    logger.info("\n" + "=" * 70)
    logger.info(title.center(70))
    logger.info("=" * 70)


def step_1_check_environment():
    """Step 1: Check environment variables"""
    print_header("STEP 1: Checking Environment Variables")
    
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "electronics_db")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD")
    
    logger.info(f"✅ DB_HOST: {db_host}")
    logger.info(f"✅ DB_PORT: {db_port}")
    logger.info(f"✅ DB_NAME: {db_name}")
    logger.info(f"✅ DB_USER: {db_user}")
    logger.info(f"✅ DB_PASSWORD: {'***' if db_password else 'NOT SET'}")
    
    if db_name != "electronics_db":
        logger.warning(f"⚠️  DB_NAME is '{db_name}' but should be 'electronics_db'")
        logger.warning("   Update your .env file: DB_NAME=electronics_db")
        return False
    
    if not db_password:
        logger.error("❌ DB_PASSWORD is not set!")
        logger.error("   Set it in your .env file")
        return False
    
    logger.info("\n✅ Environment variables are correct!")
    return True


def step_2_create_database():
    """Step 2: Create electronics_db database"""
    print_header("STEP 2: Creating Database 'electronics_db'")
    
    try:
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = "electronics_db"
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "password")
        
        logger.info(f"Connecting to PostgreSQL server at {db_host}:{db_port}...")
        
        # Connect to default postgres database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database="postgres",
            user=db_user,
            password=db_password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,)
        )
        exists = cursor.fetchone()
        
        if exists:
            logger.info(f"✅ Database '{db_name}' already exists")
        else:
            logger.info(f"📦 Creating database '{db_name}'...")
            cursor.execute(f'CREATE DATABASE {db_name}')
            logger.info(f"✅ Database '{db_name}' created successfully!")
        
        # Verify database exists
        cursor.execute(
            "SELECT datname FROM pg_database WHERE datname = %s",
            (db_name,)
        )
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            logger.info(f"\n✅ Database '{db_name}' is ready!")
            return True
        else:
            logger.error(f"❌ Failed to verify database '{db_name}'")
            return False
        
    except ImportError:
        logger.error("❌ psycopg2 is not installed!")
        logger.error("   Run: pip install psycopg2-binary")
        return False
    except Exception as e:
        logger.error(f"❌ Failed to create database: {e}")
        return False


def step_3_test_connection():
    """Step 3: Test connection to electronics_db"""
    print_header("STEP 3: Testing Connection to 'electronics_db'")
    
    try:
        from app.database import engine, DATABASE_URL, DB_NAME, text
        
        # Show connection string (hide password)
        safe_url = DATABASE_URL.replace(os.getenv("DB_PASSWORD", ""), "***")
        logger.info(f"Connection URL: {safe_url}")
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version(), current_database()"))
            version, current_db = result.fetchone()
            
            logger.info(f"✅ Connected successfully!")
            logger.info(f"   PostgreSQL: {version.split(',')[0]}")
            logger.info(f"   Current database: {current_db}")
            
            if current_db != "electronics_db":
                logger.error(f"❌ Connected to '{current_db}' instead of 'electronics_db'!")
                return False
            
            logger.info(f"\n✅ Connection to 'electronics_db' verified!")
            return True
            
    except Exception as e:
        logger.error(f"❌ Connection test failed: {e}")
        return False


def step_4_import_models():
    """Step 4: Import all models"""
    print_header("STEP 4: Importing Models")
    
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
        
        logger.info("✅ All models imported successfully!")
        logger.info("   - NguoiDung (Users)")
        logger.info("   - DanhMuc (Categories)")
        logger.info("   - SanPham (Products)")
        logger.info("   - DonHang (Orders)")
        logger.info("   - ChiTietDonHang (Order Items)")
        logger.info("   - LichSuChat (Chat History)")
        
        # Check registered tables
        registered_tables = list(Base.metadata.tables.keys())
        logger.info(f"\n📋 Registered tables ({len(registered_tables)}):")
        for table_name in registered_tables:
            logger.info(f"   - {table_name}")
        
        if len(registered_tables) == 6:
            logger.info(f"\n✅ All 6 models registered with Base!")
            return True
        else:
            logger.error(f"❌ Expected 6 tables but found {len(registered_tables)}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to import models: {e}")
        return False


def step_5_create_tables():
    """Step 5: Create all tables"""
    print_header("STEP 5: Creating Tables in 'electronics_db'")
    
    try:
        from app.database import Base, engine
        
        logger.info("🔨 Creating tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Base.metadata.create_all() executed successfully!")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
        return False


def step_6_verify_tables():
    """Step 6: Verify tables in database"""
    print_header("STEP 6: Verifying Tables in Database")
    
    try:
        from app.database import engine, text
        
        with engine.connect() as conn:
            # Get current database
            result = conn.execute(text("SELECT current_database()"))
            current_db = result.fetchone()[0]
            logger.info(f"Current database: {current_db}")
            
            # Get all tables
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]
            
            logger.info(f"\n📊 Tables in '{current_db}' ({len(tables)} tables):")
            for table in tables:
                logger.info(f"   ✅ {table}")
            
            expected_tables = [
                "nguoi_dung",
                "danh_muc",
                "san_pham",
                "don_hang",
                "chi_tiet_don_hang",
                "lich_su_chat"
            ]
            
            missing = set(expected_tables) - set(tables)
            if missing:
                logger.error(f"\n❌ Missing tables: {', '.join(missing)}")
                return False
            
            if len(tables) >= 6:
                logger.info(f"\n✅ All expected tables exist in 'electronics_db'!")
                return True
            else:
                logger.error(f"\n❌ Expected at least 6 tables but found {len(tables)}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Failed to verify tables: {e}")
        return False


def step_7_test_crud():
    """Step 7: Test CRUD operations"""
    print_header("STEP 7: Testing CRUD Operations")
    
    try:
        from app.database import SessionLocal
        from app.models import DanhMuc, SanPham
        
        db = SessionLocal()
        
        # Create
        logger.info("Creating test category...")
        category = DanhMuc(ten="Laptop")
        db.add(category)
        db.commit()
        db.refresh(category)
        logger.info(f"✅ Created: {category}")
        
        # Create product
        logger.info("Creating test product...")
        product = SanPham(
            ten="MacBook Pro",
            gia=2000.00,
            mo_ta="High-performance laptop",
            danh_muc_id=category.id
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        logger.info(f"✅ Created: {product}")
        
        # Read with relationship
        logger.info("Testing relationship...")
        product = db.query(SanPham).filter(SanPham.id == product.id).first()
        logger.info(f"✅ Product category: {product.danh_muc.ten}")
        
        # Clean up
        logger.info("Cleaning up test data...")
        db.delete(product)
        db.delete(category)
        db.commit()
        logger.info("✅ Test data cleaned up")
        
        db.close()
        
        logger.info(f"\n✅ CRUD operations working correctly!")
        return True
        
    except Exception as e:
        logger.error(f"❌ CRUD test failed: {e}")
        if 'db' in locals():
            db.rollback()
            db.close()
        return False


def main():
    """Run all steps"""
    print_header("🚀 ELECTRONICS_DB SETUP - END-TO-END")
    
    steps = [
        ("Check Environment Variables", step_1_check_environment),
        ("Create Database", step_2_create_database),
        ("Test Connection", step_3_test_connection),
        ("Import Models", step_4_import_models),
        ("Create Tables", step_5_create_tables),
        ("Verify Tables", step_6_verify_tables),
        ("Test CRUD Operations", step_7_test_crud),
    ]
    
    results = []
    
    for step_name, step_func in steps:
        try:
            result = step_func()
            results.append((step_name, result))
            
            if not result:
                logger.error(f"\n❌ {step_name} failed. Stopping setup.")
                break
                
        except Exception as e:
            logger.error(f"\n❌ Unexpected error in {step_name}: {e}")
            results.append((step_name, False))
            break
    
    # Summary
    print_header("SETUP SUMMARY")
    
    for step_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        logger.info(f"{step_name:.<50} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print_header("RESULT")
    
    if all_passed:
        logger.info("🎉 SUCCESS! Database 'electronics_db' is ready!")
        logger.info("\n📊 Summary:")
        logger.info("   ✅ Database: electronics_db")
        logger.info("   ✅ Tables: 6 tables created")
        logger.info("   ✅ Connection: Working")
        logger.info("   ✅ CRUD: Working")
        logger.info("\n🚀 Next steps:")
        logger.info("   1. Run: python run.py")
        logger.info("   2. Visit: http://localhost:8000/docs")
        logger.info("   3. Check: http://localhost:8000/debug/tables")
    else:
        logger.error("❌ SETUP FAILED!")
        logger.error("\nPlease fix the errors above and run this script again.")
        logger.error("For detailed diagnostics, run: python diagnose_db.py")
    
    logger.info("=" * 70 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
