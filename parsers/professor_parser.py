"""
教授資訊解析模組
"""
import re
import base64
from bs4 import BeautifulSoup
from utils.logger import my_logger

class ProfessorParser:
    """教授資訊解析器"""
    
    @staticmethod
    def parse_html(html):
        """
        解析 HTML 獲取教授列表
        
        Args:
            html (str): 網頁 HTML 內容
            
        Returns:
            list: 教授資訊列表
        """
        if not html:
            return []
            
        soup = BeautifulSoup(html, features="html.parser")
        professor_items = soup.select('.i-member-item.col-md-6') # 每個元素表示一個教授
        
        professors = []
        for item in professor_items:
            li_elements = item.select('li') # 獲取資訊欄
            professor_info = ProfessorParser._extract_professor_info(li_elements, str(item))
            professors.append(professor_info)
        
        return professors
    
    @staticmethod
    def _extract_professor_info(li_elements, html_content):
        """
        從 HTML 元素中提取教授資訊
        
        Args:
            li_elements (list): <li> 元素列表
            html_content (str): 原始 HTML 內容，為了 email 欄位而生!
            
        Returns:
            dict: 教授資料\，格式:
            {
                "姓名": None, "職稱": None,
                "學歷": None, "經歷": list[str],
                "研究領域": list[str], "email": None,
                "辦公室": None, "Office hour": None
            }
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
        info['email'] = ProfessorParser._extract_email(html_content)
        
        my_logger.debug(f"教授 {info['姓名']} 資料處理完畢")
        return info
    
    @staticmethod
    def _extract_email(html_string):
        """
        從 HTML 字串中提取並解碼 email
        
        Args:
            html_string (str): 包含編碼 email 的 HTML
            
        Returns:
            str or None: 解碼後的 email 或 None
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