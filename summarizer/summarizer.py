import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from summarizer.text_processor import TextProcessor

class VietnameseTextSummarizer:
    def __init__(self, n_clusters: int = 3):
        """
        Khởi tạo bộ tóm tắt văn bản
        
        Args:
            n_clusters (int): Số lượng cụm để tóm tắt
        """
        self.text_processor = TextProcessor()
        self.n_clusters = n_clusters
    
    def summarize(self, text: str, n_clusters: int = None) -> str:
        """
        Tóm tắt văn bản sử dụng phân cụm và cosine similarity
        
        Args:
            text (str): Văn bản cần tóm tắt
            n_clusters (int, optional): Số lượng cụm, nếu không truyền sẽ dùng mặc định
        
        Returns:
            str: Văn bản tóm tắt
        """
        # Sử dụng số cụm được truyền vào hoặc mặc định
        n_clusters = n_clusters or self.n_clusters
        
        # Tiền xử lý văn bản
        original_sentences, processed_sentences = self.text_processor.preprocess(text)
        
        # Kiểm tra độ dài văn bản
        if len(original_sentences) < n_clusters:
            return "Văn bản quá ngắn để tóm tắt với số cụm đã chọn!"
        
        # Tính ma trận TF-IDF với cải tiến
        tfidf = TfidfVectorizer(
            min_df=1, 
            max_df=0.9,  # Loại bỏ các từ quá phổ biến
            stop_words=None  # Đã loại bỏ stopwords ở text_processor
        )
        
        try:
            # Chuyển đổi văn bản sang vector
            vectors = tfidf.fit_transform(processed_sentences)
            
            # Kiểm tra ma trận vector
            if vectors.shape[0] == 0 or vectors.shape[1] == 0:
                return "Không thể tóm tắt: Không có đủ từ quan trọng sau khi tiền xử lý."
            
            # Phân cụm KMeans
            kmeans = KMeans(
                n_clusters=n_clusters,
                random_state=42,
                n_init=10
            )
            labels = kmeans.fit_predict(vectors)
            
            # Chọn câu đại diện bằng cosine similarity
            summarized = []
            for i in range(n_clusters):
                cluster_indices = np.where(labels == i)[0]
                if len(cluster_indices) == 0:
                    continue
                
                # Chọn câu gần centroid nhất bằng cosine similarity
                cluster_vectors = vectors[cluster_indices]
                centroid = kmeans.cluster_centers_[i]
                
                # Tính cosine similarity giữa các vector trong cụm và centroid
                similarities = cosine_similarity(cluster_vectors, centroid.reshape(1, -1)).flatten()
                best_idx = cluster_indices[np.argmax(similarities)]
                
                summarized.append(original_sentences[best_idx])
            
            # Sắp xếp các câu theo thứ tự xuất hiện
            summarized_sorted = sorted(summarized, key=lambda x: original_sentences.index(x))
            
            return '\n\n'.join(summarized_sorted)
            
        except ValueError as e:
            return f"Lỗi khi tóm tắt: {str(e)}"