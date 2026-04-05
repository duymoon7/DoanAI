"""
Quick verification script for electronics_db.
Shows current status and confirms everything is working.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("\n" + "=" * 70)
    print("ELECTRONICS_DB VERIFICATION".center(70))
    print("=" * 70)
    
    # Check environment
    print("\n📋 Environment Configuration:")
    db_name = os.getenv("DB_NAME", "NOT SET")
    print(f"   DB_NAME: {db_name}")
    
    if db_name != "electronics_db":
        print(f"\n   ⚠️  WARNING: DB_NAME is '{db_name}'")
        print(f"   Expected: 'electronics_db'")
        print(f"   Update your .env file: DB_NAME=electronics_db")
        return False
    
    print(f"   ✅ Correct database name!")
    
    # Check connection
    print("\n🔌 Connection Test:")
    try:
        from app.database import engine, text, DB_NAME
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database()"))
            current_db = result.fetchone()[0]
            
            print(f"   Connected to: {current_db}")
            
            if current_db != "electronics_db":
                print(f"   ❌ ERROR: Connected to '{current_db}' instead of 'electronics_db'")
                return False
            
            print(f"   ✅ Connected to correct database!")
            
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        print(f"\n   Run: python create_electronics_db.py")
        return False
    
    # Check tables
    print("\n🗄️  Database Tables:")
    try:
        from app.database import engine, text
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]
            
            if not tables:
                print(f"   ⚠️  No tables found!")
                print(f"   Run: python create_electronics_db.py")
                return False
            
            print(f"   Found {len(tables)} tables:")
            for table in tables:
                print(f"      ✅ {table}")
            
            expected = ["nguoi_dung", "danh_muc", "san_pham", "don_hang", "chi_tiet_don_hang", "lich_su_chat"]
            missing = set(expected) - set(tables)
            
            if missing:
                print(f"\n   ⚠️  Missing tables: {', '.join(missing)}")
                return False
                
    except Exception as e:
        print(f"   ❌ Error checking tables: {e}")
        return False
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ VERIFICATION PASSED!".center(70))
    print("=" * 70)
    print("\n📊 Status:")
    print(f"   ✅ Database: electronics_db")
    print(f"   ✅ Tables: {len(tables)} tables")
    print(f"   ✅ Connection: Working")
    print("\n🚀 Ready to use!")
    print("   Run: python run.py")
    print("   Visit: http://localhost:8000/docs")
    print("=" * 70 + "\n")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
