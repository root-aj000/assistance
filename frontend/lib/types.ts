/**
 * TypeScript type definitions for the Vibe Coding AI Agent.
 */

export interface FileInfo {
  path: string;
  name: string;
  extension: string;
  size: number;
}

export interface CodeChunk {
  id: string;
  file_path: string;
  start_line: number;
  end_line: number;
  code: string;
  tokens: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatRequest {
  question: string;
  stream?: boolean;
}

export interface ChatResponse {
  answer: string;
  context_stats: ContextStats;
}

export interface ContextStats {
  total_chunks: number;
  packed_chunks: number;
  context_tokens: number;
  system_tokens: number;
  total_tokens: number;
  utilization: number;
}

export interface DebugRequest {
  file_path: string;
  error_message: string;
  context?: string;
}

export interface DebugResponse {
  analysis: string;
  suggested_fix: string;
  context_stats: ContextStats;
}

export interface PlanRequest {
  goal: string;
  scope?: string;
}

export interface PlanResponse {
  plan: string;
  context_stats: ContextStats;
}

export interface IndexStats {
  metrics: {
    files_total: number;
    files_indexed: number;
    files_failed: number;
    asg_nodes: number;
    cfg_nodes: number;
    embeddings: number;
    chunks: number;
    file_coverage_percent: number;
  };
  vector_store: {
    total_embeddings: number;
    dimension: number;
  };
  graph_store: {
    code_nodes: number;
    cfg_nodes: number;
    relationships: number;
  };
}
