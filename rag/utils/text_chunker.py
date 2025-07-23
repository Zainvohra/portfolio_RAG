from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TextChunk:
    """Represents a chunk of text with metadata."""
    content: str
    chunk_id: str
    start_index: int
    end_index: int
    metadata: Dict[str, Any]
    word_count: int
    
    def __post_init__(self):
        if self.word_count == 0:
            self.word_count = len(self.content.split())


class TextChunker:
    """Advanced text chunking with multiple strategies for RAG optimization."""
    
    def __init__(self, 
                 chunk_size: int = 1000, 
                 overlap_size: int = 200,
                 min_chunk_size: int = 100):
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
        self.min_chunk_size = min_chunk_size
        self.name = "text_chunker"
        self.description = "Intelligent text chunking for RAG systems"
    
    def chunk_text(self, text: str, strategy: str = "recursive", metadata: Optional[Dict] = None) -> List[TextChunk]:
        """
        Chunk text using the specified strategy.
        
        Args:
            text: Input text to chunk
            strategy: Chunking strategy ('recursive', 'sentence', 'paragraph', 'semantic')
            metadata: Additional metadata to attach to chunks
            
        Returns:
            List of TextChunk objects
        """
        if not text or len(text.strip()) == 0:
            return []
        
        metadata = metadata or {}
        
        if strategy == "recursive":
            return self._recursive_chunk(text, metadata)
        elif strategy == "sentence":
            return self._sentence_chunk(text, metadata)
        elif strategy == "paragraph":
            return self._paragraph_chunk(text, metadata)
        elif strategy == "semantic":
            return self._semantic_chunk(text, metadata)
        else:
            raise ValueError(f"Unknown chunking strategy: {strategy}")
    
    def _recursive_chunk(self, text: str, metadata: Dict) -> List[TextChunk]:
        """
        Recursive chunking with overlap - best for general purpose RAG.
        Tries to split on natural boundaries while maintaining chunk size.
        """
        chunks = []
        separators = ["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " "]
        
        def _split_text(text_segment: str, start_idx: int) -> List[TextChunk]:
            if len(text_segment) <= self.chunk_size:
                if len(text_segment.strip()) >= self.min_chunk_size:
                    chunk_id = f"chunk_{len(chunks):04d}"
                    return [TextChunk(
                        content=text_segment.strip(),
                        chunk_id=chunk_id,
                        start_index=start_idx,
                        end_index=start_idx + len(text_segment),
                        metadata={**metadata, "chunking_strategy": "recursive"},
                        word_count=0  # Will be calculated in __post_init__
                    )]
                return []
            
            # Try to split on separators
            for separator in separators:
                if separator in text_segment:
                    parts = text_segment.split(separator)
                    if len(parts) > 1:
                        result_chunks = []
                        current_pos = start_idx
                        current_chunk = ""
                        
                        for i, part in enumerate(parts):
                            part_with_sep = part + (separator if i < len(parts) - 1 else "")
                            
                            if len(current_chunk + part_with_sep) <= self.chunk_size:
                                current_chunk += part_with_sep
                            else:
                                # Save current chunk if it's large enough
                                if len(current_chunk.strip()) >= self.min_chunk_size:
                                    chunk_id = f"chunk_{len(chunks) + len(result_chunks):04d}"
                                    result_chunks.append(TextChunk(
                                        content=current_chunk.strip(),
                                        chunk_id=chunk_id,
                                        start_index=current_pos,
                                        end_index=current_pos + len(current_chunk),
                                        metadata={**metadata, "chunking_strategy": "recursive"},
                                        word_count=0
                                    ))
                                
                                # Start new chunk with overlap
                                overlap_start = max(0, len(current_chunk) - self.overlap_size)
                                overlap_text = current_chunk[overlap_start:]
                                current_chunk = overlap_text + part_with_sep
                                current_pos += len(current_chunk) - len(overlap_text)
                        
                        # Add final chunk
                        if len(current_chunk.strip()) >= self.min_chunk_size:
                            chunk_id = f"chunk_{len(chunks) + len(result_chunks):04d}"
                            result_chunks.append(TextChunk(
                                content=current_chunk.strip(),
                                chunk_id=chunk_id,
                                start_index=current_pos,
                                end_index=current_pos + len(current_chunk),
                                metadata={**metadata, "chunking_strategy": "recursive"},
                                word_count=0
                            ))
                        
                        return result_chunks
            
            # If no separator works, force split
            mid_point = self.chunk_size
            chunk_id = f"chunk_{len(chunks):04d}"
            return [TextChunk(
                content=text_segment[:mid_point].strip(),
                chunk_id=chunk_id,
                start_index=start_idx,
                end_index=start_idx + mid_point,
                metadata={**metadata, "chunking_strategy": "recursive_forced"},
                word_count=0
            )]
        
        # Process the entire text
        current_position = 0
        remaining_text = text
        
        while remaining_text and len(remaining_text.strip()) >= self.min_chunk_size:
            new_chunks = _split_text(remaining_text[:self.chunk_size + self.overlap_size], current_position)
            chunks.extend(new_chunks)
            
            if new_chunks:
                # Move position forward, accounting for overlap
                chunk_length = len(new_chunks[0].content)
                advance = max(chunk_length - self.overlap_size, 1)
                current_position += advance
                remaining_text = remaining_text[advance:]
            else:
                break
        
        return chunks
    
    def _sentence_chunk(self, text: str, metadata: Dict) -> List[TextChunk]:
        """Chunk text by sentences, combining until chunk size is reached."""
        # Simple sentence splitting without regex patterns
        sentences = []
        current_sentence = ""
        
        for char in text:
            current_sentence += char
            if char in '.!?' and len(current_sentence.strip()) > 0:
                sentences.append(current_sentence.strip())
                current_sentence = ""
        
        # Add any remaining text
        if current_sentence.strip():
            sentences.append(current_sentence.strip())
        chunks = []
        current_chunk = ""
        current_start = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if len(current_chunk + " " + sentence) <= self.chunk_size:
                current_chunk += (" " if current_chunk else "") + sentence
            else:
                # Save current chunk
                if len(current_chunk.strip()) >= self.min_chunk_size:
                    chunk_id = f"chunk_{len(chunks):04d}"
                    chunks.append(TextChunk(
                        content=current_chunk.strip(),
                        chunk_id=chunk_id,
                        start_index=current_start,
                        end_index=current_start + len(current_chunk),
                        metadata={**metadata, "chunking_strategy": "sentence"},
                        word_count=0
                    ))
                
                current_chunk = sentence
                current_start += len(current_chunk)
        
        # Add final chunk
        if len(current_chunk.strip()) >= self.min_chunk_size:
            chunk_id = f"chunk_{len(chunks):04d}"
            chunks.append(TextChunk(
                content=current_chunk.strip(),
                chunk_id=chunk_id,
                start_index=current_start,
                end_index=current_start + len(current_chunk),
                metadata={**metadata, "chunking_strategy": "sentence"},
                word_count=0
            ))
        
        return chunks
    
    def _paragraph_chunk(self, text: str, metadata: Dict) -> List[TextChunk]:
        """Chunk text by paragraphs, combining until chunk size is reached."""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        chunks = []
        current_chunk = ""
        current_start = 0
        
        for paragraph in paragraphs:
            if len(current_chunk + "\n\n" + paragraph) <= self.chunk_size:
                current_chunk += ("\n\n" if current_chunk else "") + paragraph
            else:
                # Save current chunk
                if len(current_chunk.strip()) >= self.min_chunk_size:
                    chunk_id = f"chunk_{len(chunks):04d}"
                    chunks.append(TextChunk(
                        content=current_chunk.strip(),
                        chunk_id=chunk_id,
                        start_index=current_start,
                        end_index=current_start + len(current_chunk),
                        metadata={**metadata, "chunking_strategy": "paragraph"},
                        word_count=0
                    ))
                
                current_chunk = paragraph
                current_start += len(current_chunk)
        
        # Add final chunk
        if len(current_chunk.strip()) >= self.min_chunk_size:
            chunk_id = f"chunk_{len(chunks):04d}"
            chunks.append(TextChunk(
                content=current_chunk.strip(),
                chunk_id=chunk_id,
                start_index=current_start,
                end_index=current_start + len(current_chunk),
                metadata={**metadata, "chunking_strategy": "paragraph"},
                word_count=0
            ))
        
        return chunks
    
    def _semantic_chunk(self, text: str, metadata: Dict) -> List[TextChunk]:
        """
        Semantic chunking based on content structure and natural boundaries.
        Uses structural analysis without hardcoded patterns.
        """
        # For semantic chunking, fall back to paragraph-based approach
        # with some intelligent boundary detection based on text structure
        
        lines = text.split('\n')
        chunks = []
        current_chunk = ""
        current_start = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                current_chunk += "\n"
                continue
            
            # Detect potential topic boundaries using structural characteristics
            is_potential_header = (
                len(line) < 80 and  # Short lines are often headers
                line.isupper() or  # ALL CAPS
                (line[0].isupper() if line else False) and  # Starts with capital
                line.count('.') == 0 and  # No sentence-ending periods
                line.count('?') == 0 and  # No questions
                line.count('!') == 0  # No exclamations
            )
            
            # Also check if line starts with common structural indicators
            starts_with_number = line and line[0].isdigit()
            
            # Create boundary if we detect structure AND have enough content
            is_boundary = (is_potential_header or starts_with_number) and current_chunk and len(current_chunk) > self.min_chunk_size
            
            if is_boundary:
                # Save current chunk at topic boundary
                chunk_id = f"chunk_{len(chunks):04d}"
                chunks.append(TextChunk(
                    content=current_chunk.strip(),
                    chunk_id=chunk_id,
                    start_index=current_start,
                    end_index=current_start + len(current_chunk),
                    metadata={**metadata, "chunking_strategy": "semantic"},
                    word_count=0
                ))
                current_chunk = line + "\n"
                current_start += len(current_chunk)
            else:
                current_chunk += line + "\n"
                
                # Still respect max chunk size
                if len(current_chunk) >= self.chunk_size:
                    chunk_id = f"chunk_{len(chunks):04d}"
                    chunks.append(TextChunk(
                        content=current_chunk.strip(),
                        chunk_id=chunk_id,
                        start_index=current_start,
                        end_index=current_start + len(current_chunk),
                        metadata={**metadata, "chunking_strategy": "semantic"},
                        word_count=0
                    ))
                    current_chunk = ""
                    current_start += len(current_chunk)
        
        # Add final chunk
        if len(current_chunk.strip()) >= self.min_chunk_size:
            chunk_id = f"chunk_{len(chunks):04d}"
            chunks.append(TextChunk(
                content=current_chunk.strip(),
                chunk_id=chunk_id,
                start_index=current_start,
                end_index=current_start + len(current_chunk),
                metadata={**metadata, "chunking_strategy": "semantic"},
                word_count=0
            ))
        
        return chunks
    
    def get_chunk_statistics(self, chunks: List[TextChunk]) -> Dict[str, Any]:
        """Get statistics about the chunks."""
        if not chunks:
            return {}
        
        word_counts = [chunk.word_count for chunk in chunks]
        char_counts = [len(chunk.content) for chunk in chunks]
        
        return {
            "total_chunks": len(chunks),
            "total_words": sum(word_counts),
            "total_characters": sum(char_counts),
            "avg_words_per_chunk": sum(word_counts) / len(chunks),
            "avg_chars_per_chunk": sum(char_counts) / len(chunks),
            "min_words": min(word_counts),
            "max_words": max(word_counts),
            "min_chars": min(char_counts),
            "max_chars": max(char_counts),
            "strategies_used": list(set(chunk.metadata.get("chunking_strategy", "unknown") for chunk in chunks))
        }


# Create a global instance
text_chunker = TextChunker() 