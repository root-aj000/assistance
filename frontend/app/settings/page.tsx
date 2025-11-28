'use client';

import React from 'react';

export default function SettingsPage() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="mb-8">
                    <h2 className="text-3xl font-bold text-gray-900">⚙️ Settings</h2>
                    <p className="text-gray-600 mt-2">
                        Configure your AI coding assistant
                    </p>
                </div>

                <div className="space-y-6">
                    {/* API Configuration */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h3 className="text-xl font-semibold text-gray-900 mb-4">
                            API Configuration
                        </h3>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Backend URL
                                </label>
                                <input
                                    type="text"
                                    defaultValue="http://localhost:5001"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    API Status
                                </label>
                                <div className="flex items-center space-x-2">
                                    <span className="inline-block w-3 h-3 bg-green-500 rounded-full"></span>
                                    <span className="text-sm text-gray-600">Connected</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Model Settings */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h3 className="text-xl font-semibold text-gray-900 mb-4">
                            Model Settings
                        </h3>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    LLM Model
                                </label>
                                <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500">
                                    <option>gemini-2.5-flash (Default)</option>
                                    <option>gemini-2.5-pro</option>
                                    <option>gemini-2.5-flash-lite</option>
                                </select>
                                <p className="text-xs text-gray-500 mt-1">
                                    Flash: Fast & efficient | Pro: Most capable | Lite: Ultra-fast
                                </p>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Max Tokens per Request: <span className="text-indigo-600">70000</span>
                                </label>
                                <input
                                    type="range"
                                    min="10000"
                                    max="100000"
                                    step="1000"
                                    defaultValue="70000"
                                    className="w-full"
                                />
                            </div>
                        </div>
                    </div>

                    {/* Rate Limiting */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h3 className="text-xl font-semibold text-gray-900 mb-4">
                            Rate Limiting (Requests per Minute)
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Flash Model RPM
                                </label>
                                <input
                                    type="number"
                                    defaultValue="3"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Pro Model RPM
                                </label>
                                <input
                                    type="number"
                                    defaultValue="3"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Lite Model RPM
                                </label>
                                <input
                                    type="number"
                                    defaultValue="3"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Embedding RPM
                                </label>
                                <input
                                    type="number"
                                    defaultValue="3"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                />
                            </div>
                        </div>
                        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                            <p className="text-sm text-blue-800">
                                ℹ️ <strong>Rate Limiting Active:</strong> Set to 3 requests per minute (RPM) for free tier to avoid quota issues.
                                Adjust based on your API plan.
                            </p>
                        </div>
                    </div>

                    {/* Database Settings */}
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h3 className="text-xl font-semibold text-gray-900 mb-4">
                            Database Configuration
                        </h3>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Vector Store (FAISS)
                                </label>
                                <input
                                    type="text"
                                    defaultValue="./data/vector_db"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Graph Database (Neo4j)
                                </label>
                                <input
                                    type="text"
                                    defaultValue="neo4j://127.0.0.1:7687"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                />
                            </div>
                        </div>
                    </div>

                    {/* Save Button */}
                    <div className="flex justify-end">
                        <button className="px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 shadow-md hover:shadow-lg transition-all">
                            💾 Save Settings
                        </button>
                    </div>
                </div>
            </main>
        </div>
    );
}
