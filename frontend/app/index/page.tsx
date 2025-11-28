'use client';

import React, { useState } from 'react';
import { apiClient } from '@/lib/api';

export default function IndexPage() {
    const [directory, setDirectory] = useState('');
    const [loading, setLoading] = useState(false);
    const [status, setStatus] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);

    const handleIndex = async () => {
        if (!directory) {
            setStatus({ message: 'Please enter a directory path', type: 'error' });
            return;
        }

        setLoading(true);
        setStatus({ message: 'Indexing repository...', type: 'info' });

        try {
            await apiClient.indexRepository(directory);
            setStatus({ message: 'Repository indexed successfully!', type: 'success' });
        } catch (error: any) {
            setStatus({
                message: error.message || 'Failed to index repository',
                type: 'error'
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="mb-8">
                    <h2 className="text-3xl font-bold text-gray-900">📚 Index Repository</h2>
                    <p className="text-gray-600 mt-2">
                        Index your codebase to enable AI-powered search and analysis
                    </p>
                </div>

                <div className="bg-white rounded-lg shadow-lg p-6">
                    <div className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Repository Path
                            </label>
                            <input
                                type="text"
                                value={directory}
                                onChange={(e) => setDirectory(e.target.value)}
                                placeholder="e.g., U:/Assistance or C:/path/to/your/repo"
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            />
                            <p className="text-sm text-gray-500 mt-2">
                                Enter the full path to your repository
                            </p>
                        </div>

                        <button
                            onClick={handleIndex}
                            disabled={loading}
                            className={`
                w-full px-6 py-3 rounded-lg font-medium text-white transition-all
                ${loading
                                    ? 'bg-gray-400 cursor-not-allowed'
                                    : 'bg-indigo-600 hover:bg-indigo-700 shadow-md hover:shadow-lg'
                                }
              `}
                        >
                            {loading ? '⏳ Indexing...' : '🚀 Start Indexing'}
                        </button>

                        {status && (
                            <div
                                className={`
                  p-4 rounded-lg
                  ${status.type === 'success' ? 'bg-green-100 text-green-800' : ''}
                  ${status.type === 'error' ? 'bg-red-100 text-red-800' : ''}
                  ${status.type === 'info' ? 'bg-blue-100 text-blue-800' : ''}
                `}
                            >
                                {status.message}
                            </div>
                        )}
                    </div>

                    <div className="mt-8 pt-6 border-t border-gray-200">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">
                            How it works
                        </h3>
                        <ul className="space-y-2 text-sm text-gray-600">
                            <li className="flex items-start">
                                <span className="mr-2">1️⃣</span>
                                <span>The system scans your repository and extracts code structure</span>
                            </li>
                            <li className="flex items-start">
                                <span className="mr-2">2️⃣</span>
                                <span>Code is chunked and embedded using Gemini embeddings</span>
                            </li>
                            <li className="flex items-start">
                                <span className="mr-2">3️⃣</span>
                                <span>Vectors are stored in FAISS for fast similarity search</span>
                            </li>
                            <li className="flex items-start">
                                <span className="mr-2">4️⃣</span>
                                <span>Code relationships are mapped in Neo4j graph database</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </main>
        </div>
    );
}
