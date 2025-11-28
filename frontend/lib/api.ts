/**
 * API client for communicating with the backend.
 */
import {
    FileInfo,
    ChatRequest,
    ChatResponse,
    DebugRequest,
    DebugResponse,
    PlanRequest,
    PlanResponse,
    IndexStats
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001';

class ApiClient {
    /**
     * Chat with the codebase.
     */
    async chat(request: ChatRequest): Promise<ChatResponse> {
        const response = await fetch(`${API_BASE_URL}/ai/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(request)
        });

        if (!response.ok) {
            throw new Error(`Chat request failed: ${response.statusText}`);
        }

        return response.json();
    }

    /**
     * Debug code with error analysis.
     */
    async debug(request: DebugRequest): Promise<DebugResponse> {
        const response = await fetch(`${API_BASE_URL}/ai/debug`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(request)
        });

        if (!response.ok) {
            throw new Error(`Debug request failed: ${response.statusText}`);
        }

        return response.json();
    }

    /**
     * Create implementation plan.
     */
    async createPlan(request: PlanRequest): Promise<PlanResponse> {
        const response = await fetch(`${API_BASE_URL}/ai/plan`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(request)
        });

        if (!response.ok) {
            throw new Error(`Plan request failed: ${response.statusText}`);
        }

        return response.json();
    }

    /**
     * List repository files.
     */
    async listFiles(directory: string = '.'): Promise<FileInfo[]> {
        const response = await fetch(
            `${API_BASE_URL}/files?directory=${encodeURIComponent(directory)}`
        );

        if (!response.ok) {
            throw new Error(`List files failed: ${response.statusText}`);
        }

        const data = await response.json();
        return data.files;
    }

    /**
     * Get file content.
     */
    async getFileContent(filePath: string): Promise<{ path: string; content: string; lines: number }> {
        const response = await fetch(
            `${API_BASE_URL}/file?file_path=${encodeURIComponent(filePath)}`
        );

        if (!response.ok) {
            throw new Error(`Get file content failed: ${response.statusText}`);
        }

        return response.json();
    }

    /**
     * Get index statistics.
     */
    async getIndexStats(): Promise<IndexStats> {
        const response = await fetch(`${API_BASE_URL}/index/stats`);

        if (!response.ok) {
            throw new Error(`Get index stats failed: ${response.statusText}`);
        }

        return response.json();
    }

    /**
     * Trigger repository indexing.
     */
    async indexRepository(repositoryPath: string): Promise<{ status: string; stats: any }> {
        const response = await fetch(`${API_BASE_URL}/index/index`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ repository_path: repositoryPath })
        });

        if (!response.ok) {
            throw new Error(`Index repository failed: ${response.statusText}`);
        }

        return response.json();
    }
}

// Export singleton instance
export const apiClient = new ApiClient();
