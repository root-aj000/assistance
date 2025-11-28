'use client';

import React from 'react';

interface CodeViewerProps {
    code: string;
    language?: string;
    filePath?: string;
}

export default function CodeViewer({ code, language, filePath }: CodeViewerProps) {
    return (
        <div className="bg-gray-900 text-gray-100 rounded-lg shadow-lg overflow-hidden">
            {/* Header */}
            {filePath && (
                <div className="px-4 py-2 bg-gray-800 border-b border-gray-700">
                    <div className="flex items-center space-x-2 text-sm">
                        <span className="text-blue-400">📄</span>
                        <span className="font-mono">{filePath}</span>
                    </div>
                </div>
            )}

            {/* Code */}
            <div className="overflow-x-auto">
                <pre className="p-4">
                    <code className={`language-${language || 'text'}`}>{code}</code>
                </pre>
            </div>
        </div>
    );
}
