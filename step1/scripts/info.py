import pandas as pd

print(f"Pandas 버전: {pd.__version__}")

try:
    import torch

    print(f"PyTorch 버전: {torch.__version__}")
    print(f"GPU 사용 가능 여부: {torch.cuda.is_available()}")
except ImportError:
    print("PyTorch가 설치되어 있지 않습니다.")
