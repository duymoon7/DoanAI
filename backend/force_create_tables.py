#!/usr/bin/env python3
"""
Force create all database tables.
This script will:
1. Verify database connection
2. Import all models
3. Check Base metadata
4. Drop and recreate all tables
5. Verify tables were created
"""

import sys
import logging
from sqlalchemy import text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function to force create tables"""
    logger.info("=" * 70)
    logger.info("🔧 FORCE CREATE TABLES SCRIPT")
    logger.info("=" * 70)
    
    try:
        # Step 1: Import database components
        logger.info("\n📦 Step 1: Importing database components...")
        from app.database import engine, Base, DATABASE_URL, DB_NAME, DB_HOST, DB_PORT
        logger.info(f"   ✅ Database URL: postgresql+psycopg2://***@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        
        # Step 2: Test database connection
        logger.info("\n🔍 Step 2: Testing database connection...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version(), current_database()"))
            version, current_db = result.fetchone()
            logger.info(f"   ✅ PostgreSQL version: {version.split(',')[0]}")
            logger.info(f"   ✅ Current database: {current_db}")
            
            if current_db != DB_NAME:
                logger.error(f"   ❌ ERROR: Connected to '{current_db}' but expected '{DB_NAME}'")
                sys.exit(1)
        
        # Step 3: Import all models
        logger.info("\n📦 Step 3: Importing all models...")
        from app.models import (
            NguoiDung,
            DanhMuc,
            SanPham,
            DonHang,
            ChiTietDonHang,
            LichSuChat
        )
        logger.info("   ✅ All models imported successfully")
        
        # Step 4: Check registered tables in Base.metadata
        logger.info("\n📋 Step 4: Checking registered tables in Base.metadata...")
        registered_tables = list(Base.metadata.tables.keys())
        logger.info(f"   ✅ Found {len(registered_tables)} registered tables:")
        for table_name in sorted(registered_tables):
            logger.info(f"      - {table_name}")
        
        if len(registered_tables) != 6:
            logger.warning(f"   ⚠️  Expected 6 tables but found {len(registered_tables)}")
        
        # Step 5: Check current tables in database
        logger.info("\n🔍 Step 5: Checking current tables in database...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            existing_tables = [row[0] for row in result]
            
            if existing_tables:
                logger.info(f"   📊 Found {len(existing_tables)} existing tables:")
                for table in existing_tables:
                    logger.info(f"      - {table}")
            else:
                logger.info("   📊 No tables found in database")
        
        # Step 6: Drop all tables
        logger.info("\n🗑️  Step 6: Dropping all existing tables...")
        logger.warning("   ⚠️  This will delete all data!")
        Base.metadata.drop_all(bind=engine)
        logger.info("   ✅ All tables dropped")
        
        # Step 7: Create all tables
        logger.info("\n🔨 Step 7: Creating all tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("   ✅ Tables created")
        
        # Step 8: Verify tables were created
        logger.info("\n✅ Step 8: Verifying tables in database...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            final_tables = [row[0] for row in result]
            
            logger.info(f"   📊 Tables in database ({len(final_tables)} tables):")
            for table in final_tables:
                logger.info(f"      ✓ {table}")
        
        # Step 9: Verify expected tables
        logger.info("\n🎯 Step 9: Checking expected tables...")
        expected_tables = [
            "nguoi_dung",
            "danh_muc", 
            "san_pham",
            "don_hang",
            "chi_tiet_don_hang",
            "lich_su_chat"
        ]
        
        missing_tables = set(expected_tables) - set(final_tables)
        extra_tables = set(final_tables) - set(expected_tables)
        
        if missing_tables:
            logger.error(f"   ❌ Missing tables: {', '.join(missing_tables)}")
            sys.exit(1)
        
        if extra_tables:
            logger.warning(f"   ⚠️  Extra tables: {', '.join(extra_tables)}")
        
        logger.info("   ✅ All expected tables exist!")
        
        # Success summary
        logger.info("\n" + "=" * 70)
        logger.info("✅ SUCCESS! All tables created successfully!")
        logger.info("=" * 70)
        logger.info("\n📊 Database Summary:")
        logger.info(f"   Database: {DB_NAME}")
        logger.info(f"   Tables created: {len(final_tables)}")
        logger.info(f"   Tables: {', '.join(sorted(final_tables))}")
        logger.info("\n🎉 You can now use the database!")
        logger.info("   - Start FastAPI: uvicorn app.main:app --reload")
        logger.info("   - Check tables: http://localhost:8000/debug/tables")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error("\n" + "=" * 70)
        logger.error(f"❌ ERROR: {e}")
        logger.error("=" * 70)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
