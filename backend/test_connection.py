"""
Script to test database connection and setup.
Run this to verify your database configuration is correct.
"""
from app.database import check_db_connection, init_db, SessionLocal, Base, engine, text
from app.models import NguoiDung, DanhMuc, SanPham
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def test_connection():
    """Test database connection"""
    logger.info("=" * 60)
    logger.info("TEST 1: Database Connection")
    logger.info("=" * 60)
    
    if check_db_connection():
        logger.info("✅ Connection test PASSED!")
        return True
    else:
        logger.error("❌ Connection test FAILED!")
        return False


def test_model_registration():
    """Test that models are registered with Base"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 2: Model Registration")
    logger.info("=" * 60)
    
    try:
        # Import all models
        from app.models import (
            NguoiDung,
            DanhMuc,
            SanPham,
            DonHang,
            ChiTietDonHang,
            LichSuChat,
        )
        
        # Check registered tables
        registered_tables = list(Base.metadata.tables.keys())
        logger.info(f"📋 Registered models ({len(registered_tables)} tables):")
        for table_name in registered_tables:
            logger.info(f"   - {table_name}")
        
        if len(registered_tables) > 0:
            logger.info("✅ Model registration test PASSED!")
            return True
        else:
            logger.error("❌ No models registered!")
            return False
            
    except Exception as e:
        logger.error(f"❌ Model registration test FAILED: {e}")
        return False


def test_table_creation():
    """Test table creation"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 3: Table Creation")
    logger.info("=" * 60)
    
    try:
        init_db()
        logger.info("✅ Table creation test PASSED!")
        return True
    except Exception as e:
        logger.error(f"❌ Table creation test FAILED: {e}")
        return False


def test_table_verification():
    """Verify tables exist in database"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 4: Table Verification")
    logger.info("=" * 60)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            existing_tables = [row[0] for row in result]
            
            logger.info(f"📊 Tables in database ({len(existing_tables)} tables):")
            for table in existing_tables:
                logger.info(f"   - {table}")
            
            if len(existing_tables) > 0:
                logger.info("✅ Table verification test PASSED!")
                return True
            else:
                logger.error("❌ No tables found in database!")
                return False
                
    except Exception as e:
        logger.error(f"❌ Table verification test FAILED: {e}")
        return False


def test_crud_operations():
    """Test basic CRUD operations"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 5: CRUD Operations")
    logger.info("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Create a category
        danh_muc = DanhMuc(ten="Laptop")
        db.add(danh_muc)
        db.commit()
        db.refresh(danh_muc)
        logger.info(f"✅ Created category: {danh_muc}")
        
        # Create a product
        san_pham = SanPham(
            ten="MacBook Pro",
            gia=2000.00,
            mo_ta="High-performance laptop",
            danh_muc_id=danh_muc.id
        )
        db.add(san_pham)
        db.commit()
        db.refresh(san_pham)
        logger.info(f"✅ Created product: {san_pham}")
        
        # Query with relationship
        product = db.query(SanPham).filter(SanPham.id == san_pham.id).first()
        logger.info(f"✅ Product category: {product.danh_muc.ten}")
        
        # Clean up
        db.delete(san_pham)
        db.delete(danh_muc)
        db.commit()
        logger.info("✅ Cleaned up test data")
        
        logger.info("✅ CRUD operations test PASSED!")
        return True
        
    except Exception as e:
        logger.error(f"❌ CRUD operations test FAILED: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def main():
    """Run all tests"""
    logger.info("\n" + "🧪" * 30)
    logger.info("DATABASE DIAGNOSTIC TESTS")
    logger.info("🧪" * 30 + "\n")
    
    results = []
    
    # Test 1: Connection
    results.append(("Connection", test_connection()))
    
    # Test 2: Model Registration
    results.append(("Model Registration", test_model_registration()))
    
    # Test 3: Table Creation
    results.append(("Table Creation", test_table_creation()))
    
    # Test 4: Table Verification
    results.append(("Table Verification", test_table_verification()))
    
    # Test 5: CRUD Operations
    results.append(("CRUD Operations", test_crud_operations()))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        logger.info(f"{test_name:.<40} {status}")
    
    all_passed = all(result[1] for result in results)
    
    logger.info("=" * 60)
    if all_passed:
        logger.info("🎉 ALL TESTS PASSED! Database is ready to use.")
    else:
        logger.error("⚠️  SOME TESTS FAILED. Please check the errors above.")
    logger.info("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
