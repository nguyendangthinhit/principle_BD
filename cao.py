import time
import json
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from urllib.parse import urljoin, urlparse
import pandas as pd

class ThptScoreScraper:
    def __init__(self, headless=True):
        """
        Khởi tạo web scraper cho trang phổ điểm THPT
        """
        self.base_url = "https://xaydungchinhsach.chinhphu.vn/chieu-15-6-cong-bo-pho-diem-thi-tot-nghiep-thpt-2025-119250715071137062.htm"
        self.data = {
            'metadata': {},
            'content': {},
            'images': [],
            'statistics': {},
            'pdf_links': []
        }
        
        # Thiết lập Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def scrape_page_content(self):
        """
        Cào toàn bộ nội dung văn bản từ trang web
        """
        print("Đang cào nội dung trang web...")
        
        try:
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Lấy title trang
            try:
                title = self.driver.find_element(By.TAG_NAME, "title").text
                self.data['metadata']['title'] = title
            except:
                self.data['metadata']['title'] = "PHỔ ĐIỂM THI TỐT NGHIỆP THPT 2025"
            
            # Lấy toàn bộ text content
            try:
                body = self.driver.find_element(By.TAG_NAME, "body")
                self.data['content']['full_text'] = body.text
            except:
                print("Không thể lấy nội dung body")
            
            # Lấy các đoạn văn
            paragraphs = []
            try:
                p_elements = self.driver.find_elements(By.TAG_NAME, "p")
                for p in p_elements:
                    if p.text.strip():
                        paragraphs.append(p.text.strip())
                self.data['content']['paragraphs'] = paragraphs
            except:
                print("Không thể lấy các đoạn văn")
            
            # Lấy các heading
            headings = []
            for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                try:
                    elements = self.driver.find_elements(By.TAG_NAME, tag)
                    for element in elements:
                        if element.text.strip():
                            headings.append({
                                'tag': tag,
                                'text': element.text.strip()
                            })
                except:
                    continue
            self.data['content']['headings'] = headings
            
            # Lấy các link
            links = []
            try:
                a_elements = self.driver.find_elements(By.TAG_NAME, "a")
                for a in a_elements:
                    href = a.get_attribute("href")
                    text = a.text.strip()
                    if href and text:
                        links.append({
                            'url': href,
                            'text': text
                        })
                self.data['content']['links'] = links
            except:
                print("Không thể lấy các link")
                
        except Exception as e:
            print(f"Lỗi khi cào nội dung trang: {e}")
    
    def scrape_images(self):
        """
        Cào thông tin và tải xuống tất cả hình ảnh
        """
        print("Đang cào thông tin hình ảnh...")
        
        try:
            img_elements = self.driver.find_elements(By.TAG_NAME, "img")
            
            for i, img in enumerate(img_elements):
                try:
                    src = img.get_attribute("src")
                    alt = img.get_attribute("alt") or f"Image_{i+1}"
                    
                    if src:
                        # Tạo absolute URL nếu cần
                        if src.startswith("//"):
                            src = "https:" + src
                        elif src.startswith("/"):
                            src = urljoin(self.base_url, src)
                        
                        image_info = {
                            'index': i + 1,
                            'src': src,
                            'alt': alt,
                            'filename': self._generate_filename(src, i+1)
                        }
                        
                        self.data['images'].append(image_info)
                        
                except Exception as e:
                    print(f"Lỗi khi xử lý hình ảnh {i+1}: {e}")
                    
        except Exception as e:
            print(f"Lỗi khi cào hình ảnh: {e}")
    
    def download_images(self, folder_path="images"):
        """
        Tải xuống tất cả hình ảnh
        """
        print("Đang tải xuống hình ảnh...")
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        for img_info in self.data['images']:
            try:
                response = requests.get(img_info['src'], stream=True)
                if response.status_code == 200:
                    filepath = os.path.join(folder_path, img_info['filename'])
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    img_info['local_path'] = filepath
                    print(f"Đã tải: {img_info['filename']}")
                else:
                    print(f"Không thể tải: {img_info['src']}")
                    
            except Exception as e:
                print(f"Lỗi khi tải hình ảnh {img_info['filename']}: {e}")
    
    def extract_statistics(self):
        """
        Trích xuất các thống kê về điểm thi từ nội dung
        """
        print("Đang trích xuất thống kê...")
        
        full_text = self.data['content'].get('full_text', '')
        
        # Trích xuất số liệu điểm 10 theo môn
        score_10_stats = {}
        subjects = [
            "Địa lý", "Vật lý", "Lịch sử", "Kinh tế pháp luật", 
            "Hóa học", "Toán", "Tiếng Anh", "Công nghệ nông nghiệp",
            "Sinh học", "Tin học", "Công nghệ công nghiệp", "Ngữ Văn"
        ]
        
        for subject in subjects:
            try:
                # Tìm số liệu điểm 10 cho môn học
                import re
                pattern = f"Môn {subject}.*?(\d+(?:\.\d+)?)\s*bài.*?điểm 10"
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    score_10_stats[subject] = {
                        'diem_10_2025': int(match.group(1).replace('.', ''))
                    }
                    
                    # Tìm số liệu năm 2024 nếu có
                    pattern_2024 = f"năm 2024.*?(\d+(?:\.\d+)?)\s*bài.*?điểm 10"
                    match_2024 = re.search(pattern_2024, match.group(0), re.IGNORECASE)
                    if match_2024:
                        score_10_stats[subject]['diem_10_2024'] = int(match_2024.group(1).replace('.', ''))
                        
            except Exception as e:
                print(f"Lỗi khi trích xuất thống kê cho môn {subject}: {e}")
        
        # Trích xuất số liệu điểm liệt
        failed_stats = {}
        try:
            pattern = r"Môn (.+?):\s*(\d+)\s*bài.*?điểm liệt"
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            for subject, count in matches:
                subject = subject.strip()
                failed_stats[subject] = int(count)
        except Exception as e:
            print(f"Lỗi khi trích xuất thống kê điểm liệt: {e}")
        
        self.data['statistics'] = {
            'diem_10_theo_mon': score_10_stats,
            'diem_liet_theo_mon': failed_stats,
            'tong_bai_diem_liet': 936,
            'tong_bai_diem_liet_2024': 585
        }
    
    def scrape_pdf_links(self):
        """
        Tìm và lấy các link PDF
        """
        print("Đang tìm các link PDF...")
        
        try:
            links = self.data['content'].get('links', [])
            for link in links:
                if link['url'].endswith('.pdf'):
                    self.data['pdf_links'].append({
                        'url': link['url'],
                        'text': link['text']
                    })
                    
        except Exception as e:
            print(f"Lỗi khi tìm PDF links: {e}")
    
    def _generate_filename(self, url, index):
        """
        Tạo tên file cho hình ảnh
        """
        try:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                filename = f"image_{index}.jpg"
            return filename
        except:
            return f"image_{index}.jpg"
    
    def save_data(self, output_folder="scraped_data"):
        """
        Lưu tất cả dữ liệu đã cào
        """
        print("Đang lưu dữ liệu...")
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Lưu dữ liệu JSON
        json_file = os.path.join(output_folder, "thpt_2025_data.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        # Lưu dữ liệu text
        text_file = os.path.join(output_folder, "thpt_2025_content.txt")
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("PHỔ ĐIỂM THI TỐT NGHIỆP THPT 2025\n")
            f.write("=" * 50 + "\n\n")
            
            if 'full_text' in self.data['content']:
                f.write("NỘI DUNG TRANG:\n")
                f.write("-" * 20 + "\n")
                f.write(self.data['content']['full_text'])
                f.write("\n\n")
            
            # Ghi thống kê
            f.write("THỐNG KÊ ĐIỂM THI:\n")
            f.write("-" * 20 + "\n")
            stats = self.data.get('statistics', {})
            
            if 'diem_10_theo_mon' in stats:
                f.write("Số bài đạt điểm 10 theo môn:\n")
                for subject, data in stats['diem_10_theo_mon'].items():
                    f.write(f"- {subject}: {data.get('diem_10_2025', 0)} bài (2025)")
                    if 'diem_10_2024' in data:
                        f.write(f", {data['diem_10_2024']} bài (2024)")
                    f.write("\n")
                f.write("\n")
            
            if 'diem_liet_theo_mon' in stats:
                f.write("Số bài bị điểm liệt theo môn:\n")
                for subject, count in stats['diem_liet_theo_mon'].items():
                    f.write(f"- {subject}: {count} bài\n")
        
        # Lưu thông tin hình ảnh CSV
        if self.data['images']:
            df_images = pd.DataFrame(self.data['images'])
            csv_file = os.path.join(output_folder, "thpt_2025_images.csv")
            df_images.to_csv(csv_file, index=False, encoding='utf-8')
        
        # Lưu thống kê CSV
        if self.data['statistics'].get('diem_10_theo_mon'):
            stats_data = []
            for subject, data in self.data['statistics']['diem_10_theo_mon'].items():
                stats_data.append({
                    'mon_hoc': subject,
                    'diem_10_2025': data.get('diem_10_2025', 0),
                    'diem_10_2024': data.get('diem_10_2024', 0)
                })
            
            df_stats = pd.DataFrame(stats_data)
            stats_csv = os.path.join(output_folder, "thpt_2025_statistics.csv")
            df_stats.to_csv(stats_csv, index=False, encoding='utf-8')
        
        print(f"Đã lưu tất cả dữ liệu vào thư mục: {output_folder}")
    
    def run_full_scrape(self, download_images=True, output_folder="scraped_data"):
        """
        Chạy toàn bộ quá trình cào dữ liệu
        """
        try:
            print("Bắt đầu cào dữ liệu trang PHỔ ĐIỂM THI TỐT NGHIỆP THPT 2025...")
            print("=" * 60)
            
            # Cào nội dung trang
            self.scrape_page_content()
            
            # Cào thông tin hình ảnh
            self.scrape_images()
            
            # Tải hình ảnh nếu được yêu cầu
            if download_images and self.data['images']:
                images_folder = os.path.join(output_folder, "images")
                self.download_images(images_folder)
            
            # Trích xuất thống kê
            self.extract_statistics()
            
            # Tìm PDF links
            self.scrape_pdf_links()
            
            # Lưu dữ liệu
            self.save_data(output_folder)
            
            print("\n" + "=" * 60)
            print("TỔNG KẾT KẾT QUẢ CRAO DỮ LIỆU:")
            print(f"- Số đoạn văn: {len(self.data['content'].get('paragraphs', []))}")
            print(f"- Số heading: {len(self.data['content'].get('headings', []))}")
            print(f"- Số hình ảnh: {len(self.data['images'])}")
            print(f"- Số môn học có thống kê điểm 10: {len(self.data['statistics'].get('diem_10_theo_mon', {}))}")
            print(f"- Số PDF links: {len(self.data['pdf_links'])}")
            print("=" * 60)
            
        except Exception as e:
            print(f"Lỗi trong quá trình cào dữ liệu: {e}")
        
        finally:
            self.close()
    
    def close(self):
        """
        Đóng browser
        """
        if self.driver:
            self.driver.quit()

# Sử dụng scraper
if __name__ == "__main__":
    # Tạo instance scraper
    scraper = ThptScoreScraper(headless=False)  # Đặt headless=True để chạy ngầm
    
    # Chạy toàn bộ quá trình cào dữ liệu
    scraper.run_full_scrape(
        download_images=True,  # Có tải hình ảnh không
        output_folder="thpt_2025_data"  # Thư mục lưu dữ liệu
    )