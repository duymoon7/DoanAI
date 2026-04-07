"""
AI Chatbot Router
=================
Tích hợp OpenAI/Gemini để hỗ trợ khách hàng TRONG PHẠM VI hệ thống bán đồ điện tử.
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


def get_ai_client():
    """Get AI client based on AI_PROVIDER env variable"""
    provider = os.getenv("AI_PROVIDER", "").lower()
    
    if provider == "openai":
        try:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key or api_key.startswith("your-"):
                logger.warning("OPENAI_API_KEY not configured properly")
                return None, None
            return OpenAI(api_key=api_key), "openai"
        except ImportError:
            logger.error("OpenAI library not installed. Run: pip install openai")
            return None, None
        except Exception as e:
            logger.error(f"Error initializing OpenAI: {e}")
            return None, None
            
    elif provider == "gemini":
        try:
            import google.generativeai as genai
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key or api_key.startswith("your-"):
                logger.warning("GEMINI_API_KEY not configured properly")
                return None, None
            genai.configure(api_key=api_key)
            return genai.GenerativeModel('gemini-pro'), "gemini"
        except ImportError:
            logger.error("Gemini library not installed. Run: pip install google-generativeai")
            return None, None
        except Exception as e:
            logger.error(f"Error initializing Gemini: {e}")
            return None, None
    
    logger.warning(f"Unknown AI_PROVIDER: {provider}")
    return None, None


def get_product_context(db: Session) -> str:
    """Get product information for AI context"""
    products = db.query(SanPham).limit(30).all()
    categories = db.query(DanhMuc).all()
    
    context = "=== DANH SÁCH SẢN PHẨM HIỆN CÓ ===\n\n"
    context += "Danh mục: " + ", ".join([c.ten for c in categories]) + "\n\n"
    
    for product in products:
        context += f"• {product.ten}: {int(product.gia):,}đ"
        if product.mo_ta:
            context += f" ({product.mo_ta})"
        context += "\n"
    
    return context


def get_system_prompt(product_context: str) -> str:
    """Tạo system prompt CHẶT CHẼ giới hạn phạm vi trả lời"""
    return f"""BẠN LÀ TRỢ LÝ AI CỦA ELECTROSHOP - CỬA HÀNG ĐIỆN TỬ.

=== PHẠM VI TRẢ LỜI (CHỈ ĐƯỢC TRẢ LỜI TRONG PHẠM VI NÀY) ===

1. SẢN PHẨM:
   - Điện thoại, laptop, tablet, tai nghe, đồng hồ thông minh, phụ kiện điện tử
   - Thông số kỹ thuật, giá cả, tính năng
   - So sánh sản phẩm
   - Gợi ý sản phẩm phù hợp với nhu cầu

2. MUA HÀNG / ĐƠN HÀNG:
   - Cách mua hàng, thêm vào giỏ
   - Thanh toán (COD, chuyển khoản, ví điện tử, thẻ)
   - Trạng thái đơn hàng
   - Giao hàng (miễn phí >500k, nhanh 2h nội thành, 1-3 ngày tỉnh)

3. TÀI KHOẢN:
   - Đăng nhập, đăng ký
   - Quên mật khẩu
   - Lịch sử mua hàng

4. CHÍNH SÁCH:
   - Bảo hành: 12 tháng chính hãng (một số sản phẩm 24 tháng)
   - Đổi trả: 7 ngày nếu lỗi nhà sản xuất
   - Vận chuyển: Miễn phí >500k
   - Hỗ trợ: Hotline, chat, email

5. SỬ DỤNG WEBSITE:
   - Tìm kiếm, lọc sản phẩm
   - Đánh giá sản phẩm
   - Xem đơn hàng

{product_context}

=== QUY TẮC BẮT BUỘC ===

✅ ĐƯỢC PHÉP:
- Trả lời các câu hỏi trong 5 phạm vi trên
- Gợi ý sản phẩm dựa trên nhu cầu
- Hướng dẫn sử dụng website
- Giải thích chính sách

❌ NGHIÊM CẤM:
- Trả lời câu hỏi NGOÀI phạm vi hệ thống
- Viết code, giải toán, dịch thuật
- Trả lời về chính trị, thể thao, tin tức, giải trí
- Kể chuyện, tư vấn sức khỏe, pháp luật
- Bịa đặt thông tin không có trong hệ thống

=== CÁCH XỬ LÝ CÂU HỎI NGOÀI PHẠM VI ===

Nếu câu hỏi KHÔNG liên quan đến 5 phạm vi trên, BẮT BUỘC trả lời:

"Xin lỗi, tôi chỉ có thể hỗ trợ các vấn đề liên quan đến hệ thống bán hàng điện tử của ElectroShop như:
• Tư vấn sản phẩm (điện thoại, laptop, tablet, phụ kiện)
• Hướng dẫn mua hàng và thanh toán
• Thông tin về đơn hàng, giao hàng
• Chính sách bảo hành, đổi trả
• Sử dụng website

Bạn cần tôi giúp gì về các vấn đề trên?"

=== PHONG CÁCH TRẢ LỜI ===
- Tiếng Việt, thân thiện, chuyên nghiệp
- Ngắn gọn, rõ ràng (2-4 câu)
- Không dài dòng, không lặp lại
- Nếu không chắc chắn về dữ liệu cụ thể → trả lời an toàn, không bịa số liệu"""


def get_smart_fallback_response(message: str, db: Session) -> tuple[str, Optional[List[dict]]]:
    """Fallback thông minh khi không có AI provider"""
    message_lower = message.lower()
    response_text = ""
    relevant_products = []
    
    # Kiểm tra câu hỏi ngoài phạm vi
    out_of_scope_keywords = [
        "code", "lập trình", "python", "javascript", "html", "css",
        "toán", "phương trình", "tính", "giải",
        "dịch", "translate", "english", "tiếng anh",
        "chính trị", "bóng đá", "thể thao", "tin tức",
        "sức khỏe", "bệnh", "thuốc", "y tế",
        "pháp luật", "luật", "hợp đồng",
        "nấu ăn", "công thức", "món ăn"
    ]
    
    if any(keyword in message_lower for keyword in out_of_scope_keywords):
        return (
            "Xin lỗi, tôi chỉ có thể hỗ trợ các vấn đề liên quan đến hệ thống bán hàng điện tử của ElectroShop như:\n"
            "• Tư vấn sản phẩm (điện thoại, laptop, tablet, phụ kiện)\n"
            "• Hướng dẫn mua hàng và thanh toán\n"
            "• Thông tin về đơn hàng, giao hàng\n"
            "• Chính sách bảo hành, đổi trả\n"
            "• Sử dụng website\n\n"
            "Bạn cần tôi giúp gì về các vấn đề trên?",
            None
        )
    
    # Tìm kiếm sản phẩm theo từ khóa
    if any(word in message_lower for word in ["iphone", "điện thoại", "phone", "smartphone"]):
        products = db.query(SanPham).join(DanhMuc).filter(DanhMuc.ten.like("%Điện thoại%")).limit(3).all()
        response_text = "Chúng tôi có nhiều mẫu điện thoại tuyệt vời! Dưới đây là một số gợi ý phù hợp:"
        relevant_products = [{"id": p.id, "ten": p.ten, "gia": float(p.gia), "hinh_anh": p.hinh_anh} for p in products]
        
    elif any(word in message_lower for word in ["laptop", "macbook", "máy tính"]):
        products = db.query(SanPham).join(DanhMuc).filter(DanhMuc.ten.like("%Laptop%")).limit(3).all()
        response_text = "Chúng tôi có nhiều laptop chất lượng cao! Dưới đây là một số gợi ý:"
        relevant_products = [{"id": p.id, "ten": p.ten, "gia": float(p.gia), "hinh_anh": p.hinh_anh} for p in products]
        
    elif any(word in message_lower for word in ["tablet", "ipad", "máy tính bảng"]):
        products = db.query(SanPham).join(DanhMuc).filter(DanhMuc.ten.like("%Tablet%")).limit(3).all()
        response_text = "Chúng tôi có nhiều tablet phù hợp! Dưới đây là một số gợi ý:"
        relevant_products = [{"id": p.id, "ten": p.ten, "gia": float(p.gia), "hinh_anh": p.hinh_anh} for p in products]
        
    elif any(word in message_lower for word in ["tai nghe", "headphone", "airpods", "earphone"]):
        products = db.query(SanPham).join(DanhMuc).filter(DanhMuc.ten.like("%Tai nghe%")).limit(3).all()
        response_text = "Chúng tôi có nhiều tai nghe chất lượng! Dưới đây là một số gợi ý:"
        relevant_products = [{"id": p.id, "ten": p.ten, "gia": float(p.gia), "hinh_anh": p.hinh_anh} for p in products]
        
    elif any(word in message_lower for word in ["đồng hồ", "watch", "smartwatch"]):
        products = db.query(SanPham).join(DanhMuc).filter(DanhMuc.ten.like("%Đồng hồ%")).limit(3).all()
        response_text = "Chúng tôi có nhiều đồng hồ thông minh! Dưới đây là một số gợi ý:"
        relevant_products = [{"id": p.id, "ten": p.ten, "gia": float(p.gia), "hinh_anh": p.hinh_anh} for p in products]
        
    elif any(word in message_lower for word in ["giá rẻ", "rẻ nhất", "tiết kiệm", "giá tốt"]):
        products = db.query(SanPham).order_by(SanPham.gia.asc()).limit(5).all()
        response_text = "Dưới đây là các sản phẩm có giá tốt nhất:"
        relevant_products = [{"id": p.id, "ten": p.ten, "gia": float(p.gia), "hinh_anh": p.hinh_anh} for p in products]
        
    elif any(word in message_lower for word in ["cao cấp", "đắt nhất", "premium", "sang trọng"]):
        products = db.query(SanPham).order_by(SanPham.gia.desc()).limit(5).all()
        response_text = "Dưới đây là các sản phẩm cao cấp:"
        relevant_products = [{"id": p.id, "ten": p.ten, "gia": float(p.gia), "hinh_anh": p.hinh_anh} for p in products]
        
    elif any(word in message_lower for word in ["bảo hành", "warranty"]):
        response_text = "Tất cả sản phẩm được bảo hành chính hãng 12 tháng. Một số sản phẩm cao cấp có thể được bảo hành lên đến 24 tháng. Bạn có thể yên tâm mua sắm!"
        
    elif any(word in message_lower for word in ["giao hàng", "ship", "vận chuyển", "delivery"]):
        response_text = "Chúng tôi hỗ trợ giao hàng miễn phí toàn quốc cho đơn hàng trên 500.000đ. Giao hàng nhanh trong 2h tại nội thành và 1-3 ngày cho các tỉnh thành khác."
        
    elif any(word in message_lower for word in ["thanh toán", "payment", "trả tiền", "pay"]):
        response_text = "Chúng tôi hỗ trợ nhiều hình thức thanh toán:\n• Tiền mặt khi nhận hàng (COD)\n• Chuyển khoản ngân hàng\n• Ví điện tử (Momo, ZaloPay)\n• Thẻ tín dụng/ghi nợ"
        
    elif any(word in message_lower for word in ["đổi trả", "hoàn tiền", "return"]):
        response_text = "Chính sách đổi trả: Bạn có thể đổi trả sản phẩm trong vòng 7 ngày nếu phát hiện lỗi nhà sản xuất. Sản phẩm cần còn nguyên tem, hộp và chưa qua sử dụng."
        
    elif any(word in message_lower for word in ["đơn hàng", "order", "mua hàng"]):
        response_text = "Để xem đơn hàng của bạn:\n1. Đăng nhập vào tài khoản\n2. Vào mục 'Đơn hàng' trên menu\n3. Xem chi tiết và trạng thái đơn hàng\n\nBạn cũng có thể liên hệ hotline để được hỗ trợ!"
        
    else:
        response_text = "Xin chào! Tôi là trợ lý AI của ElectroShop. Tôi có thể giúp bạn:\n\n• Tìm kiếm và tư vấn sản phẩm điện tử\n• Thông tin về giá cả, bảo hành, giao hàng\n• Hướng dẫn mua hàng và thanh toán\n• Chính sách đổi trả\n• Sử dụng website\n\nBạn cần tôi giúp gì?"
    
    return response_text, relevant_products if relevant_products else None


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    chat_data: ChatMessage,
    db: Session = Depends(get_db)
):
    """
    Chat với AI assistant - CHỈ TRẢ LỜI TRONG PHẠM VI HỆ THỐNG
    """
    try:
        # Get AI client
        client, provider = get_ai_client()
        
        if not client:
            # Fallback thông minh
            logger.info("Using smart fallback (no AI provider)")
            response_text, relevant_products = get_smart_fallback_response(chat_data.message, db)
            
            # Save chat history
            if chat_data.nguoi_dung_id:
                chat_history = LichSuChat(
                    nguoi_dung_id=chat_data.nguoi_dung_id,
                    tin_nhan=chat_data.message,
                    phan_hoi=response_text
                )
                db.add(chat_history)
                db.commit()
            
            return {
                "response": response_text,
                "products": relevant_products
            }
        
        # Get product context
        product_context = get_product_context(db)
        system_prompt = get_system_prompt(product_context)
        
        # Call AI based on provider
        if provider == "openai":
            logger.info("Using OpenAI provider")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": chat_data.message}
                ],
                max_tokens=400,
                temperature=0.7
            )
            ai_response = response.choices[0].message.content
            
        elif provider == "gemini":
            logger.info("Using Gemini provider")
            full_prompt = f"{system_prompt}\n\nUser: {chat_data.message}\n\nAssistant:"
            response = client.generate_content(full_prompt)
            ai_response = response.text
        else:
            raise Exception("Unknown provider")
        
        # Save chat history
        if chat_data.nguoi_dung_id:
            chat_history = LichSuChat(
                nguoi_dung_id=chat_data.nguoi_dung_id,
                tin_nhan=chat_data.message,
                phan_hoi=ai_response
            )
            db.add(chat_history)
            db.commit()
        
        # Find relevant products based on keywords
        relevant_products = []
        keywords = chat_data.message.lower()
        
        if any(word in keywords for word in ["iphone", "điện thoại", "phone", "smartphone"]):
            products = db.query(SanPham).join(DanhMuc).filter(DanhMuc.ten.like("%Điện thoại%")).limit(3).all()
            relevant_products = [{"id": p.id, "ten": p.ten, "gia": float(p.gia), "hinh_anh": p.hinh_anh} for p in products]
            
        elif any(word in keywords for word in ["laptop", "macbook", "máy tính"]):
            products = db.query(SanPham).join(DanhMuc).filter(DanhMuc.ten.like("%Laptop%")).limit(3).all()
            relevant_products = [{"id": p.id, "ten": p.ten, "gia": float(p.gia), "hinh_anh": p.hinh_anh} for p in products]
            
        elif any(word in keywords for word in ["tablet", "ipad"]):
            products = db.query(SanPham).join(DanhMuc).filter(DanhMuc.ten.like("%Tablet%")).limit(3).all()
            relevant_products = [{"id": p.id, "ten": p.ten, "gia": float(p.gia), "hinh_anh": p.hinh_anh} for p in products]
            
        elif any(word in keywords for word in ["tai nghe", "headphone", "airpods"]):
            products = db.query(SanPham).join(DanhMuc).filter(DanhMuc.ten.like("%Tai nghe%")).limit(3).all()
            relevant_products = [{"id": p.id, "ten": p.ten, "gia": float(p.gia), "hinh_anh": p.hinh_anh} for p in products]
        
        return {
            "response": ai_response,
            "products": relevant_products if relevant_products else None
        }
        
    except Exception as e:
        logger.error(f"Chatbot error: {e}", exc_info=True)
        # Fallback an toàn
        response_text, relevant_products = get_smart_fallback_response(chat_data.message, db)
        return {
            "response": response_text,
            "products": relevant_products
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
