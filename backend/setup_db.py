"""
Quick database setup script.
This will create the database and all tables.
"""
import sys
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def create_database_if_not_exists():
    """Create database if it doesn't exist"""
    logger.info("🔧 Checking if database exists...")
    
    try:
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "electronics_db")
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "password")
        
        logger.info(f"   Target database: {db_name}")
        logger.info(f"   Host: {db_host}:{db_port}")
        logger.info(f"   User: {db_user}")
        
        # Connect to PostgreSQL server (not to specific database)
        logger.info("   Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database="postgres",  # Connect to default database
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
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        logger.error("❌ psycopg2 is not installed!")
        logger.error("   Run: pip install psycopg2-binary")
        return False
    except Exception as e:
        logger.error(f"❌ Failed to create database: {e}")
        logger.error("\nPossible solutions:")
        logger.error("   1. Check PostgreSQL is running")
        logger.error("   2. Verify credentials in .env file")
        logger.error("   3. Ensure user has CREATE DATABASE permission")
        return False


def setup_tables():
    """Create all tables"""
    logger.info("\n🔨 Setting up database tables...")
    
    try:
        from app.database import init_db, check_db_connection
        
        # Check connection first
        if not check_db_connection():
            logger.error("❌ Cannot connect to database!")
            return False
        
        # Create tables
        init_db()
        logger.info("✅ All tables created successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
        return False


def main():
    """Main setup function"""
    logger.info("\n" + "=" * 60)
    logger.info("DATABASE SETUP")
    logger.info("=" * 60 + "\n")
    
    # Step 1: Create database
    if not create_database_if_not_exists():
        logger.error("\n❌ Setup failed at database creation step")
        return False
    
    # Step 2: Create tables
    if not setup_tables():
        logger.error("\n❌ Setup failed at table creation step")
        return False
    
    logger.info("\n" + "=" * 60)
    logger.info("🎉 DATABASE SETUP COMPLETED SUCCESSFULLY!")
    logger.info("=" * 60)
    logger.info("\nYour database is ready to use!")
    logger.info("\nNext steps:")
    logger.info("  1. Run the application: python run.py")
    logger.info("  2. Visit API docs: http://localhost:8000/docs")
    logger.info("=" * 60 + "\n")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
