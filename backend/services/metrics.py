"""
Metrics tracking for indexing coverage.
"""
from typing import Dict, Any
from datetime import datetime


class MetricsTracker:
    """Tracks indexing metrics and coverage."""
    
    def __init__(self):
        """Initialize metrics tracker."""
        self.metrics = {
            'files_total': 0,
            'files_indexed': 0,
            'files_failed': 0,
            'asg_nodes': 0,
            'cfg_nodes': 0,
            'embeddings': 0,
            'chunks': 0,
            'last_index_time': None,
            'index_duration_seconds': 0
        }
    
    def start_indexing(self):
        """Mark start of indexing."""
        self.start_time = datetime.now()
    
    def finish_indexing(self):
        """Mark end of indexing."""
        if hasattr(self, 'start_time'):
            duration = (datetime.now() - self.start_time).total_seconds()
            self.metrics['index_duration_seconds'] = duration
            self.metrics['last_index_time'] = datetime.now().isoformat()
    
    def increment(self, metric: str, value: int = 1):
        """Increment a metric."""
        if metric in self.metrics:
            self.metrics[metric] += value
    
    def set(self, metric: str, value: Any):
        """Set a metric value."""
        self.metrics[metric] = value
    
    def get_stats(self) -> Dict[str, Any]:
        """Get all metrics."""
        # Calculate coverage percentages
        file_coverage = 0.0
        if self.metrics['files_total'] > 0:
            file_coverage = self.metrics['files_indexed'] / self.metrics['files_total']
        
        return {
            **self.metrics,
            'file_coverage_percent': round(file_coverage * 100, 2),
            'avg_chunks_per_file': round(
                self.metrics['chunks'] / max(self.metrics['files_indexed'], 1), 2
            ),
            'avg_nodes_per_file': round(
                self.metrics['asg_nodes'] / max(self.metrics['files_indexed'], 1), 2
            )
        }
    
    def reset(self):
        """Reset all metrics."""
        self.metrics = {
            'files_total': 0,
            'files_indexed': 0,
            'files_failed': 0,
            'asg_nodes': 0,
            'cfg_nodes': 0,
            'embeddings': 0,
            'chunks': 0,
            'last_index_time': None,
            'index_duration_seconds': 0
        }


# Global metrics tracker instance
metrics_tracker = MetricsTracker()
