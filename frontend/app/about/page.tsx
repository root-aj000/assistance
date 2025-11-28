'use client';

import React from 'react';

export default function AboutPage() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="mb-8">
                    <h2 className="text-3xl font-bold text-gray-900">ℹ️ About Vibe Coding AI</h2>
                    <p className="text-gray-600 mt-2">
                        Your intelligent code understanding and debugging assistant
                    </p>
                </div>

                <div className="space-y-6">
                    {/* Overview */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h3 className="text-xl font-semibold text-gray-900 mb-4">
                            What is Vibe Coding AI?
                        </h3>
                        <p className="text-gray-700 leading-relaxed">
                            Vibe Coding AI Agent is an advanced AI-powered coding assistant that helps you understand,
                            debug, and improve your codebase. It combines the power of large language models with
                            sophisticated code analysis tools to provide intelligent insights and assistance.
                        </p>
                    </div>

                    {/* Features */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h3 className="text-xl font-semibold text-gray-900 mb-4">
                            Key Features
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="flex items-start space-x-3">
                                <span className="text-2xl">🔍</span>
                                <div>
                                    <h4 className="font-semibold text-gray-900">Semantic Code Search</h4>
                                    <p className="text-sm text-gray-600">Find code using natural language queries</p>
                                </div>
                            </div>
                            <div className="flex items-start space-x-3">
                                <span className="text-2xl">💬</span>
                                <div>
                                    <h4 className="font-semibold text-gray-900">AI Chat Assistant</h4>
                                    <p className="text-sm text-gray-600">Ask questions about your codebase</p>
                                </div>
                            </div>
                            <div className="flex items-start space-x-3">
                                <span className="text-2xl">🐛</span>
                                <div>
                                    <h4 className="font-semibold text-gray-900">Debug Analysis</h4>
                                    <p className="text-sm text-gray-600">Get AI-powered debugging suggestions</p>
                                </div>
                            </div>
                            <div className="flex items-start space-x-3">
                                <span className="text-2xl">📊</span>
                                <div>
                                    <h4 className="font-semibold text-gray-900">Code Graph Traversal</h4>
                                    <p className="text-sm text-gray-600">Explore code relationships and dependencies</p>
                                </div>
                            </div>
                            <div className="flex items-start space-x-3">
                                <span className="text-2xl">✨</span>
                                <div>
                                    <h4 className="font-semibold text-gray-900">Code Generation</h4>
                                    <p className="text-sm text-gray-600">Generate implementation plans and code</p>
                                </div>
                            </div>
                            <div className="flex items-start space-x-3">
                                <span className="text-2xl">🚀</span>
                                <div>
                                    <h4 className="font-semibold text-gray-900">Fast & Efficient</h4>
                                    <p className="text-sm text-gray-600">Optimized for large codebases</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Technology Stack */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h3 className="text-xl font-semibold text-gray-900 mb-4">
                            Technology Stack
                        </h3>
                        <div className="space-y-3">
                            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <span className="font-medium text-gray-900">LLM & Embeddings</span>
                                <span className="text-indigo-600">Google Gemini 2.0 Flash</span>
                            </div>
                            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <span className="font-medium text-gray-900">Vector Database</span>
                                <span className="text-indigo-600">FAISS</span>
                            </div>
                            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <span className="font-medium text-gray-900">Graph Database</span>
                                <span className="text-indigo-600">Neo4j</span>
                            </div>
                            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <span className="font-medium text-gray-900">Code Parsing</span>
                                <span className="text-indigo-600">Tree-sitter</span>
                            </div>
                            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <span className="font-medium text-gray-900">Backend</span>
                                <span className="text-indigo-600">FastAPI (Python)</span>
                            </div>
                            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <span className="font-medium text-gray-900">Frontend</span>
                                <span className="text-indigo-600">Next.js (React + TypeScript)</span>
                            </div>
                        </div>
                    </div>

                    {/* Version Info */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h3 className="text-xl font-semibold text-gray-900 mb-4">
                            Version Information
                        </h3>
                        <div className="space-y-2 text-gray-700">
                            <p><strong>Version:</strong> 1.0.0</p>
                            <p><strong>Release Date:</strong> November 2025</p>
                            <p><strong>License:</strong> MIT</p>
                        </div>
                    </div>

                    {/* Links */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h3 className="text-xl font-semibold text-gray-900 mb-4">
                            Resources
                        </h3>
                        <div className="space-y-2">
                            <a
                                href="http://localhost:5001/docs"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="block text-indigo-600 hover:text-indigo-800 hover:underline"
                            >
                                📖 API Documentation
                            </a>
                            <a
                                href="https://ai.google.dev/gemini-api/docs"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="block text-indigo-600 hover:text-indigo-800 hover:underline"
                            >
                                🔗 Gemini API Documentation
                            </a>
                            <a
                                href="https://ai.google.dev/gemini-api/docs/rate-limits"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="block text-indigo-600 hover:text-indigo-800 hover:underline"
                            >
                                ⚡ Rate Limits & Quotas
                            </a>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
