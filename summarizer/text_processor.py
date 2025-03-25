import os
import re
import numpy as np
from functools import lru_cache
from pyvi import ViTokenizer
from typing import List, Tuple

class TextProcessor:
    def __init__(self, stopwords_path: str = None):
        # Tải stopwords với caching để tăng hiệu suất
        self.stopwords = self._load_stopwords(stopwords_path)
    
    @lru_cache(maxsize=128)
    def _load_stopwords(self, stopwords_path: str = None) -> set:
        """
        Tải stopwords với caching để tăng hiệu suất
        """
        try:
            # Ưu tiên đường dẫn được truyền vào
            if stopwords_path and os.path.exists(stopwords_path):
                with open(stopwords_path, 'r', encoding='utf-8') as f:
                    return set(line.strip().lower() for line in f)
            
            # Thử đường dẫn mặc định
            default_path = os.path.join("resources", "vietnamese-stopwords.txt")
            if os.path.exists(default_path):
                with open(default_path, 'r', encoding='utf-8') as f:
                    return set(line.strip().lower() for line in f)
            
            # Danh sách stopwords nếu không có file
            return {
                "và", "của", "là", "trong", "cho", "với", "các", "có", "được", "đã", 
                "những", "này", "để", "tại", "theo", "từ", "khi", "như", "không", "còn",
                "bởi", "về", "một", "nhiều", "sau", "trên", "đến", "nhưng", "vì", "mà"
            }
        except Exception as e:
            print(f"Lỗi khi tải stopwords: {e}")
            return set()

    def preprocess(self, text: str, min_word_length: int = 2) -> Tuple[List[str], List[str]]:
        """
        Xử lý văn bản, loại bỏ stopwords và các từ quá ngắn
        
        Args:
            text (str): Văn bản đầu vào
            min_word_length (int): Độ dài tối thiểu của từ để giữ lại
        
        Returns:
            Tuple[List[str], List[str]]: Danh sách câu gốc và câu đã xử lý
        """
        # Tách văn bản thành các câu với regex nâng cao
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Loại bỏ các câu trắng và quá ngắn
        sentences = [s.strip() for s in sentences if s.strip() and len(s.split()) > 2]
        
        cleaned_sentences = []
        for sentence in sentences:
            # Tokenize và xử lý
            words = ViTokenizer.tokenize(sentence).split()
            
            # Lọc stopwords và từ quá ngắn
            cleaned_words = [
                word for word in words 
                if word.lower() not in self.stopwords and len(word) >= min_word_length
            ]
            
            # Chỉ giữ lại câu có từ sau khi lọc
            if cleaned_words:
                cleaned_sentences.append(' '.join(cleaned_words))
        
        return sentences, cleaned_sentences