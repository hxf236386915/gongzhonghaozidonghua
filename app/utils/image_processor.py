from PIL import Image, ImageDraw, ImageFont
import io
import base64
from typing import Dict, Tuple, Optional
import magic
import hashlib
import os
import shutil
from datetime import datetime, timedelta

class ImageProcessor:
    ALLOWED_FORMATS = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
    MAX_SIZE = 1024 * 1024 * 5  # 5MB
    CACHE_DIR = "cache/images"
    FONT_DIR = "app/assets/fonts"
    DEFAULT_FONT_URL = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Regular.otf"
    DEFAULT_FONT_PATH = "app/assets/fonts/NotoSansCJK-Regular.otf"

    def __init__(self):
        os.makedirs(self.CACHE_DIR, exist_ok=True)
        os.makedirs(self.FONT_DIR, exist_ok=True)
        self._ensure_default_font()
        self._init_cache_cleanup()

    def _ensure_default_font(self):
        """确保默认字体文件存在"""
        if not os.path.exists(self.DEFAULT_FONT_PATH):
            try:
                import requests
                print("Downloading default font...")
                response = requests.get(self.DEFAULT_FONT_URL)
                response.raise_for_status()
                with open(self.DEFAULT_FONT_PATH, 'wb') as f:
                    f.write(response.content)
                print("Default font downloaded successfully")
            except Exception as e:
                print(f"Failed to download default font: {e}")
                # 如果下载失败，使用系统默认字体
                if os.path.exists("/System/Library/Fonts/PingFang.ttc"):  # macOS
                    self.DEFAULT_FONT_PATH = "/System/Library/Fonts/PingFang.ttc"
                elif os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):  # Linux
                    self.DEFAULT_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
                else:
                    print("Warning: No suitable font found, watermark may not work properly")

    def _init_cache_cleanup(self):
        """初始化缓存清理"""
        self.cleanup_cache()

    def cleanup_cache(self, max_age_days: int = 7):
        """清理旧的缓存文件"""
        try:
            now = datetime.now()
            for root, dirs, files in os.walk(self.CACHE_DIR):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if now - file_modified > timedelta(days=max_age_days):
                        os.remove(file_path)
                        
            # 清理空目录
            for root, dirs, files in os.walk(self.CACHE_DIR, topdown=False):
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    if not os.listdir(dir_path):  # 如果目录为空
                        os.rmdir(dir_path)
        except Exception as e:
            print(f"Cache cleanup failed: {e}")

    def _get_cache_path(self, image_data: bytes) -> str:
        """生成图片缓存路径"""
        hash_value = hashlib.md5(image_data).hexdigest()
        date_path = datetime.now().strftime("%Y/%m/%d")
        cache_path = os.path.join(self.CACHE_DIR, date_path)
        os.makedirs(cache_path, exist_ok=True)
        return os.path.join(cache_path, f"{hash_value}.webp")

    def validate_image(self, image_data: bytes) -> bool:
        """验证图片格式和大小"""
        if len(image_data) > self.MAX_SIZE:
            raise ValueError("Image size exceeds maximum allowed size")
        
        mime_type = magic.from_buffer(image_data, mime=True)
        if mime_type not in self.ALLOWED_FORMATS:
            raise ValueError(f"Unsupported image format: {mime_type}")
        
        return True

    def optimize_image(
        self,
        image_data: bytes,
        max_width: int = 800,
        quality: int = 85,
        format: str = 'WEBP'
    ) -> bytes:
        """优化图片尺寸和质量"""
        image = Image.open(io.BytesIO(image_data))
        
        # 保持宽高比缩放
        if image.width > max_width:
            ratio = max_width / image.width
            new_size = (max_width, int(image.height * ratio))
            image = image.resize(new_size, Image.LANCZOS)
        
        # 转换为RGB模式（处理RGBA图片）
        if image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        
        # 保存优化后的图片
        output = io.BytesIO()
        image.save(output, format=format, quality=quality, optimize=True)
        return output.getvalue()

    def add_watermark(
        self,
        image_data: bytes,
        watermark_text: str,
        position: str = 'bottom-right',
        opacity: int = 50
    ) -> bytes:
        """添加水印"""
        image = Image.open(io.BytesIO(image_data))
        
        # 创建水印层
        watermark = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)
        
        # 计算水印位置
        font_size = int(min(image.size) * 0.05)  # 水印大小为图片较小边的5%
        try:
            font = ImageFont.truetype(self.DEFAULT_FONT_PATH, font_size)
        except Exception as e:
            print(f"Failed to load font: {e}, using default font")
            font = ImageFont.load_default()
        
        text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # 根据position参数确定水印位置
        padding = 20
        if position == 'bottom-right':
            position = (image.width - text_width - padding, image.height - text_height - padding)
        elif position == 'bottom-left':
            position = (padding, image.height - text_height - padding)
        elif position == 'top-right':
            position = (image.width - text_width - padding, padding)
        elif position == 'top-left':
            position = (padding, padding)
        else:  # center
            position = ((image.width - text_width) // 2, (image.height - text_height) // 2)
        
        # 绘制水印
        draw.text(position, watermark_text, font=font, fill=(255, 255, 255, opacity))
        
        # 合并水印和原图
        output = io.BytesIO()
        Image.alpha_composite(image.convert('RGBA'), watermark).convert('RGB').save(
            output, 'WEBP', quality=95
        )
        return output.getvalue()

    def process_image(
        self,
        image_data: bytes,
        optimize: bool = True,
        add_watermark: bool = False,
        watermark_text: Optional[str] = None,
        max_width: int = 800,
        quality: int = 85
    ) -> Dict:
        """处理图片的主函数"""
        try:
            # 验证图片
            self.validate_image(image_data)
            
            # 检查缓存
            cache_path = self._get_cache_path(image_data)
            if os.path.exists(cache_path):
                with open(cache_path, 'rb') as f:
                    processed_data = f.read()
            else:
                # 优化图片
                if optimize:
                    image_data = self.optimize_image(
                        image_data,
                        max_width=max_width,
                        quality=quality
                    )
                
                # 添加水印
                if add_watermark and watermark_text:
                    image_data = self.add_watermark(image_data, watermark_text)
                
                # 保存到缓存
                processed_data = image_data
                with open(cache_path, 'wb') as f:
                    f.write(processed_data)
            
            # 转换为base64
            base64_data = base64.b64encode(processed_data).decode()
            
            return {
                "data": f"data:image/webp;base64,{base64_data}",
                "size": {
                    "width": max_width,
                    "height": None  # 高度会根据宽度自动计算
                }
            }
            
        except Exception as e:
            raise ValueError(f"Image processing failed: {str(e)}") 