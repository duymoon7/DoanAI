from .nguoi_dung import router as nguoi_dung_router
from .danh_muc import router as danh_muc_router
from .san_pham import router as san_pham_router
from .don_hang import router as don_hang_router
from .chi_tiet_don_hang import router as chi_tiet_don_hang_router
from .lich_su_chat import router as lich_su_chat_router
from .admin import router as admin_router
from .ma_giam_gia import router as ma_giam_gia_router

__all__ = [
    "nguoi_dung_router",
    "danh_muc_router",
    "san_pham_router",
    "don_hang_router",
    "chi_tiet_don_hang_router",
    "lich_su_chat_router",
    "admin_router",
    "ma_giam_gia_router",
]
