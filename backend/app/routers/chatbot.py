"""
AI Chatbot Router
=================
Tích hợp OpenAI GPT để hỗ trợ khách hàng.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.models import LichSuChat, NguoiDung, SanPham, DanhMuc
from app.auth import get_current_active_user
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chatbot", tags=["AI Chatbot"])


class ChatMessage(BaseModel):
    message: str
    nguoi_dung_id: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    products: Optional[List[dict]] = None


def get_openai_client():
    """Get OpenAI client (lazy import)"""
    try:
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found in environment")
            return None
        return OpenAI(api_key=api_key)
    except ImportError:
        logger.error("OpenAI library not installed. Run: pip install openai")
        return None
    except Exception as e:
        logger.error(f"Error initializing OpenAI client: {e}")
        return None


def get_product_context(db: Session) -> str:
    """Get product information for AI context"""
    products = db.query(SanPham).limit(20).all()
    categories = db.query(DanhMuc).all()
    
    context = "Thông tin sản phẩm hiện có:\n\n"
    context += "Danh mục: " + ", ".join([c.ten for c in categories]) + "\n\n"
    
    for product in products:
        context += f"- {product.ten}: {product.gia:,}đ"
        if product.mo_ta:
            context += f" - {product.mo_ta}"
        context += "\n"
    
    return context


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    chat_data: ChatMessage,
    db: Session = Depends(get_db)
):
    """
    Chat với AI assistant
    
    - Hỗ trợ tư vấn sản phẩm
    - Trả lời câu hỏi về shop
    - Gợi ý sản phẩm phù hợp
    """
    try:
        # Get OpenAI client
        client = get_openai_client()
        
        if not client:
            # Fallback response if OpenAI not configured
            logger.warning("OpenAI not configured, using fallback response")
            return {
                "response": "Xin chào! Tôi là trợ lý AI của ElectroShop. Hiện tại hệ thống AI đang được cấu hình. Bạn có thể xem danh sách sản phẩm của chúng tôi hoặc liên hệ bộ phận hỗ trợ để được tư vấn.",
                "products": None
            }
        
        # Get product context
        product_context = get_product_context(db)
        
        # System prompt
        system_prompt = f"""Bạn là trợ lý AI của cửa hàng điện tử ElectroShop.
Nhiệm vụ của bạn:
- Tư vấn sản phẩm điện tử (điện thoại, laptop, tablet, phụ kiện)
- Giúp khách hàng chọn sản phẩm phù hợp
- Trả lời câu hỏi về sản phẩm, giá cả, tính năng
- Thân thiện, nhiệt tình, chuyên nghiệp

{product_context}

Lưu ý:
- Chỉ tư vấn về sản phẩm có trong danh sách
- Nếu không có sản phẩm phù hợp, gợi ý sản phẩm tương tự
- Trả lời ngắn gọn, dễ hiểu
- Sử dụng tiếng Việt
"""
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": chat_data.message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        # Save chat history
        if chat_data.nguoi_dung_id:
            chat_history = LichSuChat(
                nguoi_dung_id=chat_data.nguoi_dung_id,
                tin_nhan=chat_data.message,
                phan_hoi=ai_response
            )
            db.add(chat_history)
            db.commit()
        
        # Try to find relevant products
        relevant_products = []
        keywords = chat_data.message.lower()
        
        if any(word in keywords for word in ["iphone", "điện thoại", "phone"]):
            products = db.query(SanPham).join(DanhMuc).filter(
                DanhMuc.ten.like("%Điện thoại%")
            ).limit(3).all()
            relevant_products = [
                {
                    "id": p.id,
                    "ten": p.ten,
                    "gia": p.gia,
                    "hinh_anh": p.hinh_anh
                }
                for p in products
            ]
        elif any(word in keywords for word in ["laptop", "macbook"]):
            products = db.query(SanPham).join(DanhMuc).filter(
                DanhMuc.ten.like("%Laptop%")
            ).limit(3).all()
            relevant_products = [
                {
                    "id": p.id,
                    "ten": p.ten,
                    "gia": p.gia,
                    "hinh_anh": p.hinh_anh
                }
                for p in products
            ]
        
        return {
            "response": ai_response,
            "products": relevant_products if relevant_products else None
        }
        
    except Exception as e:
        logger.error(f"Chatbot error: {e}")
        # Fallback response if OpenAI fails
        return {
            "response": "Xin lỗi, tôi đang gặp sự cố kỹ thuật. Vui lòng thử lại sau hoặc liên hệ bộ phận hỗ trợ.",
            "products": None
        }


@router.get("/history/{user_id}")
async def get_chat_history(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Lấy lịch sử chat của user
    """
    history = db.query(LichSuChat).filter(
        LichSuChat.nguoi_dung_id == user_id
    ).order_by(
        LichSuChat.ngay_tao.desc()
    ).offset(skip).limit(limit).all()
    
    return history


@router.delete("/history/{chat_id}")
async def delete_chat_history(
    chat_id: int,
    current_user: NguoiDung = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Xóa một tin nhắn trong lịch sử
    """
    chat = db.query(LichSuChat).filter(LichSuChat.id == chat_id).first()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Không tìm thấy tin nhắn")
    
    # Check ownership
    if chat.nguoi_dung_id != current_user.id and current_user.vai_tro != "admin":
        raise HTTPException(status_code=403, detail="Không có quyền xóa tin nhắn này")
    
    db.delete(chat)
    db.commit()
    
    return {"message": "Đã xóa tin nhắn thành công"}
