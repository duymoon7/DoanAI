"""
Fix PostgreSQL table creation issue.
This script will diagnose and fix the problem with comprehensive logging.
"""
import os
import sys
from dotenv import load_dotenv
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def print_section(title):
    """Print a formatted section header"""
    logger.info("\n" + "=" * 80)
    logger.info(f"  {title}")
    logger.info("=" * 80)


def step_1_verify_connection():
    """Step 1: Verify database connection and URL"""
    print_section("STEP 1: Verify Database Connection")
    
    try:
        from app.database import (
            engine, DATABASE_URL, DB_HOST, DB_PORT, 
            DB_NAME, DB_USER, DB_PASSWORD, text
        )
        
        # Show full DATABASE_URL (hide password)
        safe_url = DATABASE_URL.replace(DB_PASSWORD, "***")
        logger.info(f"📊 Database Configuration:")
        logger.info(f"   DB_HOST: {DB_HOST}")
        logger.info(f"   DB_PORT: {DB_PORT}")
        logger.info(f"   DB_NAME: {DB_NAME}")
        logger.info(f"   DB_USER: {DB_USER}")
        logger.info(f"   Full URL: {safe_url}")
        
        # Test connection
        logger.info(f"\n🔌 Connecting to database...")
        with engine.connect() as conn:
            # Get current database
            result = conn.execute(text("SELECT current_database(), version()"))
            current_db, version = result.fetchone()
            
            logger.info(f"✅ Connection successful!")
            logger.info(f"   Current database: {current_db}")
            logger.info(f"   PostgreSQL: {version.split(',')[0]}")
            
            if current_db != DB_NAME:
                logger.error(f"❌ ERROR: Connected to '{current_db}' but expected '{DB_NAME}'!")
                return False
            
            if current_db != "electronics_db":
                logger.error(f"❌ ERROR: Connected to '{current_db}' but expected 'electronics_db'!")
                return False
            
            logger.info(f"✅ Connected to correct database: {current_db}")
            return True
            
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        return False


def step_2_import_all_models():
    """Step 2: Import all models explicitly"""
    print_section("STEP 2: Import All Models")
    
    try:
        logger.info("📦 Importing model modules...")
        
        # Import each model file explicitly
        from app.models import nguoi_dung
        logger.info("   ✅ nguoi_dung imported")
        
        from app.models import danh_muc
        logger.info("   ✅ danh_muc imported")
        
        from app.models import san_pham
        logger.info("   ✅ san_pham imported")
        
        from app.models import don_hang
        logger.info("   ✅ don_hang imported")
        
        from app.models import chi_tiet_don_hang
        logger.info("   ✅ chi_tiet_don_hang imported")
        
        from app.models import lich_su_chat
        logger.info("   ✅ lich_su_chat imported")
        
        logger.info("\n✅ All model modules imported successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to import models: {e}")
        import traceback
        traceback.print_exc()
        return False


def step_3_check_base_usage():
    """Step 3: Verify all models use the same Base"""
    print_section("STEP 3: Check Base Usage")
    
    try:
        from app.database import Base as DatabaseBase
        from app.models.base import BaseModel
        
        logger.info("🔍 Checking Base instances...")
        logger.info(f"   Database Base: {id(DatabaseBase)}")
        logger.info(f"   BaseModel Base: {id(BaseModel.__bases__[0])}")
        
        if id(DatabaseBase) == id(BaseModel.__bases__[0]):
            logger.info("✅ All models use the same Base instance!")
            return True
        else:
            logger.error("❌ ERROR: Models use different Base instances!")
            logger.error("   This will prevent tables from being registered!")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to check Base: {e}")
        return False


def step_4_check_registered_tables():
    """Step 4: Check registered tables in Base.metadata"""
    print_section("STEP 4: Check Registered Tables")
    
    try:
        from app.database import Base
        
        # Import all models to ensure they're registered
        from app.models import (
            NguoiDung, DanhMuc, SanPham,
            DonHang, ChiTietDonHang, LichSuChat
        )
        
        registered_tables = list(Base.metadata.tables.keys())
        
        logger.info(f"📋 Registered tables in Base.metadata:")
        logger.info(f"   Total: {len(registered_tables)} tables")
        
        if len(registered_tables) == 0:
            logger.error("❌ ERROR: No tables registered!")
            logger.error("   Models are not being registered with Base!")
            return False
        
        for table_name in sorted(registered_tables):
            logger.info(f"   ✅ {table_name}")
        
        expected_tables = [
            "nguoi_dung", "danh_muc", "san_pham",
            "don_hang", "chi_tiet_don_hang", "lich_su_chat"
        ]
        
        missing = set(expected_tables) - set(registered_tables)
        if missing:
            logger.error(f"❌ Missing tables: {', '.join(missing)}")
            return False
        
        logger.info(f"\n✅ All {len(registered_tables)} tables registered correctly!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to check registered tables: {e}")
        import traceback
        traceback.print_exc()
        return False


def step_5_force_create_tables():
    """Step 5: Force table creation with drop and recreate"""
    print_section("STEP 5: Force Create Tables")
    
    try:
        from app.database import Base, engine
        
        # Import all models
        from app.models import (
            NguoiDung, DanhMuc, SanPham,
            DonHang, ChiTietDonHang, LichSuChat
        )
        
        logger.info("⚠️  Dropping all existing tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ Tables dropped")
        
        logger.info("\n🔨 Creating all tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Base.metadata.create_all() executed")
        
        logger.info("\n✅ Table creation completed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
        import traceback
        traceback.print_exc()
        return False


def step_6_verify_tables_in_db():
    """Step 6: Verify tables exist in PostgreSQL"""
    print_section("STEP 6: Verify Tables in PostgreSQL")
    
    try:
        from app.database import engine, text
        
        logger.info("🔍 Querying PostgreSQL for tables...")
        
        with engine.connect() as conn:
            # Get current database
            result = conn.execute(text("SELECT current_database()"))
            current_db = result.fetchone()[0]
            logger.info(f"   Current database: {current_db}")
            
            # Get all tables in public schema
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result]
            
            logger.info(f"\n📊 Tables in '{current_db}' database:")
            logger.info(f"   Total: {len(tables)} tables")
            
            if len(tables) == 0:
                logger.error("❌ ERROR: No tables found in database!")
                logger.error("   Tables were not created successfully!")
                return False
            
            for table_name in tables:
                logger.info(f"   ✅ {table_name}")
            
            expected_tables = [
                "nguoi_dung", "danh_muc", "san_pham",
                "don_hang", "chi_tiet_don_hang", "lich_su_chat"
            ]
            
            missing = set(expected_tables) - set(tables)
            if missing:
                logger.error(f"\n❌ Missing tables: {', '.join(missing)}")
                return False
            
            logger.info(f"\n✅ All {len(tables)} tables exist in PostgreSQL!")
            return True
            
    except Exception as e:
        logger.error(f"❌ Failed to verify tables: {e}")
        import traceback
        traceback.print_exc()
        return False


def step_7_test_crud():
    """Step 7: Test CRUD operations"""
    print_section("STEP 7: Test CRUD Operations")
    
    try:
        from app.database import SessionLocal
        from app.models import DanhMuc, SanPham
        
        db = SessionLocal()
        
        logger.info("🧪 Testing CREATE...")
        category = DanhMuc(ten="Test Category")
        db.add(category)
        db.commit()
        db.refresh(category)
        logger.info(f"   ✅ Created: {category}")
        
        logger.info("\n🧪 Testing READ...")
        found = db.query(DanhMuc).filter(DanhMuc.id == category.id).first()
        logger.info(f"   ✅ Found: {found}")
        
        logger.info("\n🧪 Testing relationship...")
        product = SanPham(
            ten="Test Product",
            gia=100.00,
            mo_ta="Test",
            danh_muc_id=category.id
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        logger.info(f"   ✅ Product created: {product}")
        logger.info(f"   ✅ Product category: {product.danh_muc.ten}")
        
        logger.info("\n🧪 Cleaning up...")
        db.delete(product)
        db.delete(category)
        db.commit()
        logger.info("   ✅ Test data cleaned up")
        
        db.close()
        
        logger.info("\n✅ CRUD operations working!")
        return True
        
    except Exception as e:
        logger.error(f"❌ CRUD test failed: {e}")
        import traceback
        traceback.print_exc()
        if 'db' in locals():
            db.rollback()
            db.close()
        return False


def main():
    """Run all steps"""
    print_section("🔧 FIX TABLES - COMPREHENSIVE DIAGNOSTIC AND REPAIR")
    
    steps = [
        ("Verify Database Connection", step_1_verify_connection),
        ("Import All Models", step_2_import_all_models),
        ("Check Base Usage", step_3_check_base_usage),
        ("Check Registered Tables", step_4_check_registered_tables),
        ("Force Create Tables", step_5_force_create_tables),
        ("Verify Tables in PostgreSQL", step_6_verify_tables_in_db),
        ("Test CRUD Operations", step_7_test_crud),
    ]
    
    results = []
    
    for step_name, step_func in steps:
        try:
            result = step_func()
            results.append((step_name, result))
            
            if not result:
                logger.error(f"\n❌ {step_name} failed!")
                logger.error("   Stopping execution.")
                break
                
        except Exception as e:
            logger.error(f"\n❌ Unexpected error in {step_name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((step_name, False))
            break
    
    # Summary
    print_section("SUMMARY")
    
    for step_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        logger.info(f"{step_name:.<60} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print_section("RESULT")
    
    if all_passed:
        logger.info("🎉 SUCCESS! All tables created and verified!")
        logger.info("\n📊 Summary:")
        logger.info("   ✅ Database: electronics_db")
        logger.info("   ✅ Tables: 6 tables created")
        logger.info("   ✅ Location: electronics_db → Schemas → public → Tables")
        logger.info("   ✅ Tables:")
        logger.info("      - nguoi_dung")
        logger.info("      - danh_muc")
        logger.info("      - san_pham")
        logger.info("      - don_hang")
        logger.info("      - chi_tiet_don_hang")
        logger.info("      - lich_su_chat")
        logger.info("\n🚀 Next steps:")
        logger.info("   1. Run: python run.py")
        logger.info("   2. Visit: http://localhost:8000/docs")
        logger.info("   3. Check: http://localhost:8000/debug/tables")
    else:
        logger.error("❌ FAILED! Some steps did not complete successfully.")
        logger.error("\nPlease review the errors above.")
        logger.error("Common issues:")
        logger.error("   1. Models not using same Base instance")
        logger.error("   2. Models not imported before create_all()")
        logger.error("   3. Database connection issues")
        logger.error("   4. Permission issues")
    
    logger.info("=" * 80 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
