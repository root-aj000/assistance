'use client';

import React, { useState, useEffect } from 'react';
import { FileInfo } from '@/lib/types';
import { apiClient } from '@/lib/api';

interface FileTreeProps {
    onFileSelect: (filePath: string) => void;
}

export default function FileTree({ onFileSelect }: FileTreeProps) {
    const [files, setFiles] = useState<FileInfo[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedFile, setSelectedFile] = useState<string | null>(null);

    useEffect(() => {
        loadFiles();
    }, []);

    const loadFiles = async () => {
        try {
            setLoading(true);
            const fileList = await apiClient.listFiles('.');
            setFiles(fileList);
            setError(null);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load files');
        } finally {
            setLoading(false);
        }
    };

    const handleFileClick = (file: FileInfo) => {
        setSelectedFile(file.path);
        onFileSelect(file.path);
    };

    const getFileIcon = (extension: string) => {
        switch (extension) {
            case '.py':
                return '🐍';
            case '.ts':
            case '.tsx':
                return '📘';
            case '.js':
            case '.jsx':
                return '📒';
            default:
                return '📄';
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="text-gray-500">Loading files...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-4">
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-800 text-sm">{error}</p>
                    <button
                        onClick={loadFiles}
                        className="mt-2 text-sm text-red-600 hover:text-red-800 underline"
                    >
                        Retry
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            {/* Header */}
            <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
                <h3 className="font-semibold text-gray-800">Repository Files</h3>
                <p className="text-xs text-gray-500 mt-1">{files.length} files</p>
            </div>

            {/* File List */}
            <div className="overflow-y-auto max-h-[600px]">
                {files.length === 0 ? (
                    <div className="p-4 text-center text-gray-400">
                        No files found
                    </div>
                ) : (
                    <ul className="divide-y divide-gray-100">
                        {files.map((file, idx) => (
                            <li
                                key={idx}
                                onClick={() => handleFileClick(file)}
                                className={`px-4 py-2 cursor-pointer transition-colors ${selectedFile === file.path
                                        ? 'bg-blue-50 border-l-2 border-blue-600'
                                        : 'hover:bg-gray-50'
                                    }`}
                            >
                                <div className="flex items-center space-x-2">
                                    <span className="text-lg">{getFileIcon(file.extension)}</span>
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm font-medium text-gray-900 truncate">
                                            {file.name}
                                        </p>
                                        <p className="text-xs text-gray-500 truncate">{file.path}</p>
                                    </div>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
}
