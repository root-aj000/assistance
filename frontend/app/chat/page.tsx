'use client';

import React from 'react';
import ChatBox from '@/components/ChatBox';

export default function ChatPage() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="mb-6">
                    <h2 className="text-3xl font-bold text-gray-900">💬 AI Chat</h2>
                    <p className="text-gray-600 mt-2">
                        Ask questions about your codebase, get debugging help, or generate code
                    </p>
                </div>

                <div className="h-[calc(100vh-250px)]">
                    <ChatBox />
                </div>
            </main>
        </div>
    );
}
