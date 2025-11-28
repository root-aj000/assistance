'use client';

import React from 'react';

interface MessageBubbleProps {
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
}

export default function MessageBubble({ role, content, timestamp }: MessageBubbleProps) {
    const isUser = role === 'user';

    return (
        <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
            <div
                className={`max-w-[80%] rounded-lg px-4 py-3 ${isUser
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-900 border border-gray-200'
                    }`}
            >
                <div className="text-sm font-medium mb-1">
                    {isUser ? 'You' : 'AI Assistant'}
                </div>
                <div className="whitespace-pre-wrap">{content}</div>
                <div className="text-xs mt-2 opacity-70">
                    {timestamp.toLocaleTimeString()}
                </div>
            </div>
        </div>
    );
}
