import os

def load_text_file(filepath, encodings=('utf-8', 'latin-1')):
    """
    Tải nội dung từ file văn bản với các encoding khác nhau
    
    Parameters:
    -----------
    filepath : str
        Đường dẫn đến file
    encodings : tuple
        Tuple chứa các encoding cần thử
        
    Returns:
    --------
    str
        Nội dung file
    """
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read(), encoding
        except UnicodeDecodeError:
            continue
        except Exception as e:
            raise e
    
    raise UnicodeDecodeError(f"Không thể đọc file với các encoding: {encodings}")