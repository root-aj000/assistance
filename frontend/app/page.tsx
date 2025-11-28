'use client';

import React, { useState } from 'react';
import ChatBox from '@/components/ChatBox';
import FileTree from '@/components/FileTree';
import CodeViewer from '@/components/CodeViewer';
import { apiClient } from '@/lib/api';

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [fileContent, setFileContent] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const handleFileSelect = async (filePath: string) => {
    setLoading(true);
    try {
      const content = await apiClient.getFileContent(filePath);
      setSelectedFile(filePath);
      setFileContent(content.content);
    } catch (error) {
      console.error('Error loading file:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <p className="text-lg text-gray-700">
            AI-powered code understanding and debugging assistant
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Select a file from the tree, view its code, and chat with AI about it
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Sidebar - File Tree */}
          <div className="lg:col-span-1">
            <FileTree onFileSelect={handleFileSelect} />
          </div>

          {/* Middle Column - Code Viewer */}
          <div className="lg:col-span-1">
            {selectedFile ? (
              <div className="h-full">
                <CodeViewer
                  code={loading ? 'Loading...' : fileContent}
                  filePath={selectedFile}
                  language={selectedFile.endsWith('.py') ? 'python' : 'typescript'}
                />
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-lg h-full flex items-center justify-center">
                <div className="text-center text-gray-400">
                  <p>Select a file to view its contents</p>
                </div>
              </div>
            )}
          </div>

          {/* Right Column - Chat */}
          <div className="lg:col-span-1 h-[600px]">
            <ChatBox />
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>
            Powered by Gemini 2.5 Flash • FAISS • Neo4j • Tree-sitter
          </p>
        </div>
      </main>
    </div>
  );
}

