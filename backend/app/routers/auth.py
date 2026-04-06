"""
Authentication Router
====================
Endpoints cho đăng nhập, đăng ký, và quản lý authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.models import NguoiDung
from app.schemas import (
    NguoiDungCreate,
    NguoiDungResponse,
    Token,
    LoginRequest,
    RegisterRequest
)
from app.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=NguoiDungResponse, status_code=201)
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Đăng ký tài khoản mới
    
    - Kiểm tra email đã tồn tại chưa
    - Hash password
    - Tạo user mới với role 'user'
    """
    try:
        # Check if email exists
        existing_user = db.query(NguoiDung).filter(NguoiDung.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email đã được sử dụng"
            )
        
        # Hash password
        hashed_password = get_password_hash(user_data.mat_khau)
        
        # Create new user
        new_user = NguoiDung(
            email=user_data.email,
            mat_khau=hashed_password,
            ho_ten=user_data.ho_ten,
            vai_tro="user"  # Default role
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Đăng nhập
    
    - Xác thực email và password
    - Trả về JWT access token
    """
    # Find user by email
    user = db.query(NguoiDung).filter(NguoiDung.email == login_data.email).first()
    
    if not user or not verify_password(login_data.mat_khau, user.mat_khau):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.vai_tro},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login (for Swagger UI)
    
    - Username field = email
    - Password field = password
    """
    user = db.query(NguoiDung).filter(NguoiDung.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.mat_khau):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.vai_tro},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=NguoiDungResponse)
def get_current_user_info(current_user: NguoiDung = Depends(get_current_active_user)):
    """
    Lấy thông tin user hiện tại từ token
    
    - Requires: Bearer token in Authorization header
    """
    return current_user


@router.post("/change-password")
def change_password(
    old_password: str,
    new_password: str,
    current_user: NguoiDung = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Đổi mật khẩu
    
    - Xác thực mật khẩu cũ
    - Hash và lưu mật khẩu mới
    """
    # Verify old password
    if not verify_password(old_password, current_user.mat_khau):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu cũ không đúng"
        )
    
    # Hash new password
    hashed_password = get_password_hash(new_password)
    current_user.mat_khau = hashed_password
    
    db.commit()
    
    return {"message": "Đổi mật khẩu thành công"}
