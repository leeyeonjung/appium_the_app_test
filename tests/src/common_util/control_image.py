# Third-party libraries
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim

def compare(img1, img2):
    """
    두 이미지의 유사도를 SSIM 기반으로 계산하여 0~100 점수 반환
    img1, img2: str 경로 또는 PIL.Image 객체
    """
    # 문자열 경로면 열기
    if isinstance(img1, str):
        img1 = Image.open(img1)
    if isinstance(img2, str):
        img2 = Image.open(img2)

    # RGB로 변환 (JPG/PNG 채널 차이 제거)
    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")

    # 두 이미지 크기 맞추기 (작은 쪽 기준)
    w1, h1 = img1.size
    w2, h2 = img2.size
    target_w = min(w1, w2)
    target_h = min(h1, h2)

    img1_resized = img1.resize((target_w, target_h), Image.Resampling.LANCZOS)
    img2_resized = img2.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # numpy 배열 변환
    arr1 = np.array(img1_resized)
    arr2 = np.array(img2_resized)

    # SSIM 계산 (컬러 지원: channel_axis=-1)
    score, _ = ssim(arr1, arr2, channel_axis=-1, full=True)

    return round(score * 100, 2)  # 0~100 점수

open = Image.open