"""
教授資訊解析模組
"""
import re
import base64
from bs4 import BeautifulSoup
from utils.logger import my_logger

class ProfessorParser:
    """Professor Information Parser"""
    
    @staticmethod
    def parse_html(html: str) -> list[dict] :
        """
        Parses the provided HTML content to extract information about professors.
        
        Args:
            html (str): The HTML content of the page to be parsed.
            
        Returns:
            list: A list of dictionaries, each containing professor information, with the following structure:
                - '姓名': The professor's name (str or None if not found).
                - '職稱': The professor's position or academic title (str or None if not found).
                - '學歷': The professor's education background (str or None if not found).
                - '經歷': A list of the professor's experiences (list of str, or an empty list if not found).
                - '研究領域': A list of the professor's research areas (list of str, or an empty list if not found).
                - 'email': The professor's email (str or None if not found).
                - '辦公室': The professor's office location (str or None if not found).
                - 'Office hour': The professor's office hours (str or None if not found, or a link to the schedule).
        """
        if not html:
            return []
            
        soup = BeautifulSoup(html, features="html.parser")
        professor_items = soup.select('.i-member-item.col-md-6') # 每個元素表示一個教授
        
        professors = []
        for item in professor_items:
            li_elements = item.select('li') # 獲取資訊欄
            professor_info = ProfessorParser.extract_professor_info(li_elements, str(item))
            professors.append(professor_info)
        
        return professors
    
    @staticmethod
    def extract_professor_info(li_elements, html_content):
        """
        Extracts detailed information about a professor from the given HTML elements.
        
        Args:
            li_elements (list): A list of <li> elements that contain professor information.
            html_content (str): The raw HTML content, used to extract the professor's email.
            
        Returns:
            dict: A dictionary containing the extracted information about the professor. The dictionary 
                includes the following keys:
                - '姓名': The professor's name (str or None if not found).
                - '職稱': The professor's position or academic title (str or None if not found).
                - '學歷': The professor's education background (str or None if not found).
                - '經歷': A list of the professor's experiences (list of str, or an empty list if not found).
                - '研究領域': A list of the professor's research areas (list of str, or an empty list if not found).
                - 'email': The professor's email (str or None if not found).
                - '辦公室': The professor's office location (str or None if not found).
                - 'Office hour': The professor's office hours (str or None if not found, or a link to the schedule).
        """
        my_logger.debug("開始清洗教授資料...")
        
        # 預設資訊
        info = {
            "姓名": None, "職稱": None,
            "學歷": None, "經歷": [],
            "研究領域": [], "email": None,
            "辦公室": None, "Office hour": None
        }
        
        # 搜尋目標資訊
        fields = ["姓名", "職稱", "學歷", "辦公室", "經歷", "研究領域", "Office hour"]
        
        # 提取內容函數
        def get_content(text):
            colon_pos = text.find(":")
            if colon_pos == -1:
                return text.strip()
            return text[colon_pos + 2:].replace('\xa0', '').strip('\n').strip()
        
        # 處理每個 li 元素
        for li in li_elements:
            for field in fields:
                if field in li.text:
                    if field == '研究領域':
                        info[field] = get_content(li.text).split('、')
                    elif field == 'Office hour':
                        try:
                            link = li.select_one('a')
                            if link and 'href' in link.attrs:
                                info[field] = f"時程表: {link['href']}"
                        except Exception as e:
                            my_logger.warning(f"解析 'Office hour' 錯誤: {e}")
                            pass # 不必要回傳錯誤訊息，我覺得這邊出現異常不重要
                    elif field == '經歷':
                        try:
                            span = li.select_one('span:nth-of-type(2)')
                            if span:
                                temp = str(span)
                                text_ls = temp.split("<br/>")
                                info[field] = [re.sub(r'<[^>]+>', '', txt).strip() 
                                                for txt in text_ls if txt.strip()]
                        except Exception as e:
                            my_logger.warning(f"解析 '經歷' 時出錯: {e}")
                            raise e # 拋出異常! 這個錯誤需要被處裡
                    else:
                        info[field] = get_content(li.text)
                    break
        
        # 解析 email
        info['email'] = ProfessorParser.extract_email(html_content)
        
        my_logger.debug(f"教授 {info['姓名']} 資料處理完畢")
        return info
    
    @staticmethod
    def extract_email(html_string):
        """
        Extracts and decodes the email address from the HTML content.
        
        Args:
            html_string (str): The HTML string containing the encoded email.
            
        Returns:
            str: The decoded email address (or None if not found or decoding fails).
        """
        my_logger.debug("進行 email 解碼..")
        
        if not isinstance(html_string, str):
            return None
        
        base64_email_pattern = r'atob\("([^"]+)"\)'
        match = re.search(base64_email_pattern, html_string)
        
        if match:
            try:
                base64_email = match.group(1)
                decoded_email = base64.b64decode(base64_email).decode('utf-8')
                return decoded_email.strip()
            except Exception as e:
                my_logger.warning(f"解碼 email 時出錯: {e}")
                return None
        else:
            return None