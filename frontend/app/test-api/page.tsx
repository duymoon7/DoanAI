'use client';

import { useState } from 'react';

export default function TestAPIPage() {
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const testBackendConnection = async () => {
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/health');
      const data = await response.json();
      setResult({ type: 'health', data });
    } catch (err: any) {
      setError(`Health check failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const testCreateOrder = async () => {
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const orderData = {
        nguoi_dung_id: 1,
        tong_tien: 100000,
        trang_thai: 'pending',
        phuong_thuc_thanh_toan: 'cod',
      };

      const response = await fetch('http://localhost:8000/api/don-hang', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult({ type: 'order', data });
    } catch (err: any) {
      setError(`Create order failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Test API Connection</h1>

      <div className="space-y-4 mb-8">
        <button
          onClick={testBackendConnection}
          disabled={loading}
          className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
        >
          Test Backend Health
        </button>

        <button
          onClick={testCreateOrder}
          disabled={loading}
          className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 ml-4"
        >
          Test Create Order
        </button>
      </div>

      {loading && (
        <div className="p-4 bg-gray-100 rounded-lg">
          <p>Loading...</p>
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          <h3 className="font-bold mb-2">Error:</h3>
          <pre className="whitespace-pre-wrap">{error}</pre>
        </div>
      )}

      {result && (
        <div className="p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">
          <h3 className="font-bold mb-2">Success ({result.type}):</h3>
          <pre className="whitespace-pre-wrap">{JSON.stringify(result.data, null, 2)}</pre>
        </div>
      )}

      <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h3 className="font-bold mb-2">Debug Info:</h3>
        <p>API URL: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'}</p>
        <p>Backend: http://localhost:8000</p>
      </div>
    </div>
  );
}
