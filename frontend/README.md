# ElectroShop - E-Commerce Frontend

Modern, professional e-commerce frontend built with Next.js 14, TypeScript, and Tailwind CSS.

## 🚀 Features

- ✅ Clean, minimalist UI (Amazon + Shopee inspired)
- ✅ Product listing with filters and sorting
- ✅ Product detail pages
- ✅ Shopping cart with localStorage persistence
- ✅ Responsive design (mobile-first)
- ✅ Loading skeletons
- ✅ Toast notifications
- ✅ Authentication pages (Login/Register)
- ✅ Category filtering
- ✅ Price range filter
- ✅ Search functionality

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Notifications**: React Hot Toast

## 📦 Installation

```bash
cd frontend
npm install
```

## 🏃 Running the App

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## 🔌 Backend Connection

Make sure your backend is running on `http://localhost:8000`

```bash
cd backend
python run.py
```

## 📁 Project Structure

```
frontend/
├── app/
│   ├── page.tsx              # Homepage
│   ├── products/
│   │   ├── page.tsx          # Product listing
│   │   └── [id]/page.tsx     # Product detail
│   ├── cart/page.tsx         # Shopping cart
│   ├── auth/
│   │   ├── login/page.tsx    # Login page
│   │   └── register/page.tsx # Register page
│   ├── layout.tsx            # Root layout
│   └── globals.css           # Global styles
├── components/
│   ├── Navbar.tsx            # Navigation bar
│   ├── Footer.tsx            # Footer
│   ├── ProductCard.tsx       # Product card component
│   └── LoadingSkeleton.tsx   # Loading states
├── contexts/
│   └── CartContext.tsx       # Cart state management
├── lib/
│   ├── api.ts                # API functions
│   └── types.ts              # TypeScript types
└── public/
    └── placeholder.png       # Placeholder image
```

## 🎨 Design System

### Colors
- Primary: `#0ea5e9` (Sky Blue)
- Accent: `#fb923c` (Orange)
- Background: `#f9fafb` (Gray 50)

### Components
- Buttons: `.btn-primary`, `.btn-secondary`
- Cards: `.card`
- Inputs: `.input`

## 📱 Pages

### Homepage (`/`)
- Hero banner
- Features section
- Categories
- Featured products
- Newsletter signup

### Products (`/products`)
- Product grid (4 columns)
- Sidebar filters:
  - Category
  - Price range
  - Sort options
- Search functionality
- Responsive layout

### Product Detail (`/products/[id]`)
- Large product image
- Product info
- Price with discount
- Quantity selector
- Add to cart / Buy now
- Features (shipping, warranty)

### Cart (`/cart`)
- Cart items list
- Quantity controls
- Order summary
- Promo code input
- Checkout button

### Auth Pages
- Login (`/auth/login`)
- Register (`/auth/register`)
- Clean centered card design
- Social login buttons

## 🔧 API Integration

All API calls are in `lib/api.ts`:

```typescript
// Get products
const products = await getProducts();

// Get single product
const product = await getProduct(id);

// Get categories
const categories = await getCategories();
```

## 🛒 Cart Management

Cart uses Context API with localStorage:

```typescript
const { cart, addToCart, removeFromCart, updateQuantity } = useCart();
```

## 🎯 Next Steps

- [ ] Implement authentication
- [ ] Add checkout flow
- [ ] User profile page
- [ ] Order history
- [ ] Product reviews
- [ ] Wishlist
- [ ] Search with debounce
- [ ] Image zoom on hover
- [ ] Related products

## 📝 Notes

- Images use Next.js Image component for optimization
- All remote images are allowed in `next.config.ts`
- Cart persists in localStorage
- Toast notifications for user feedback
- Responsive design with Tailwind breakpoints

---

**Ready to run!** 🎉

```bash
npm run dev
```
