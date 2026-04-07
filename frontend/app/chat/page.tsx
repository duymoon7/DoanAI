'use client';

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  products?: Product[];
}

interface Product {
  id: number;
  ten: string;
  gia: number;
  hinh_anh: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Xin chào! Tôi là trợ lý AI của ElectroShop. Tôi có thể giúp bạn tìm kiếm sản phẩm, tư vấn mua hàng, và trả lời các câu hỏi về chính sách của shop. Bạn cần tôi giúp gì?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = { role: 'user', content: input };
    const currentInput = input;
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Call chatbot API using env variable
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
      const response = await fetch(`${apiUrl}/chatbot/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: currentInput,
          nguoi_dung_id: null
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const aiResponse: Message = {
        role: 'assistant',
        content: data.response || 'Xin lỗi, tôi không thể trả lời câu hỏi này.',
        products: data.products || undefined
      };
      setMessages(prev => [...prev, aiResponse]);
    } catch (error) {
      console.error('Error:', error);
      const errorResponse: Message = {
        role: 'assistant',
        content: 'Xin lỗi, đã có lỗi xảy ra khi kết nối với server. Vui lòng thử lại sau.'
      };
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">Tư vấn AI</h1>
      
      <div className="bg-white rounded-lg shadow-lg p-6 h-[600px] flex flex-col">
        <div className="flex-1 overflow-y-auto mb-4 space-y-4">
          {messages.map((msg, idx) => (
            <div key={idx}>
              <div
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[70%] p-4 rounded-lg whitespace-pre-wrap ${
                    msg.role === 'user'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {msg.content}
                </div>
              </div>
              
              {/* Display products if available */}
              {msg.products && msg.products.length > 0 && (
                <div className="mt-3 ml-0 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {msg.products.map((product) => (
                    <Link
                      key={product.id}
                      href={`/products/${product.id}`}
                      className="bg-white border rounded-lg p-3 hover:shadow-md transition-shadow"
                    >
                      <div className="relative w-full h-32 mb-2">
                        <Image
                          src={product.hinh_anh || '/placeholder.png'}
                          alt={product.ten}
                          fill
                          className="object-cover rounded"
                        />
                      </div>
                      <h4 className="text-sm font-semibold text-gray-900 line-clamp-2 mb-1">
                        {product.ten}
                      </h4>
                      <p className="text-primary font-bold">
                        {Number(product.gia).toLocaleString('vi-VN')}đ
                      </p>
                    </Link>
                  ))}
                </div>
              )}
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 p-4 rounded-lg">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>
            </div>
          )}
        </div>
        
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Nhập câu hỏi của bạn..."
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            Gửi
          </button>
        </div>
      </div>
      
      <div className="mt-6 bg-blue-50 p-4 rounded-lg">
        <h3 className="font-semibold mb-2">Gợi ý câu hỏi:</h3>
        <ul className="list-disc list-inside space-y-1 text-sm text-gray-700">
          <li>Tìm laptop gaming giá tốt</li>
          <li>So sánh iPhone 15 và Samsung S24</li>
          <li>Tai nghe chống ồn tốt nhất</li>
          <li>Chính sách bảo hành như thế nào?</li>
          <li>Giao hàng mất bao lâu?</li>
        </ul>
      </div>
    </div>
  );
}
