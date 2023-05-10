from pydantic import BaseModel

class Product(BaseModel):
    name: str
    color: str
    size: str
    photo_path: str

    class Config:
        # 校驗顏色和尺寸
        anystr_strip_whitespace = True  # 自動清理空格

        @classmethod
        def validate(cls, values):
            # 校驗顏色是否合法
            allowed_colors = ["紅", "綠", "藍", "黃", "黑", "灰"]
            if values.get("color") not in allowed_colors:
                raise ValueError(f"invalid color, allowed values are {allowed_colors}")

            # 校驗尺寸是否合法
            allowed_sizes = ["S", "M", "L", "2L", "XL", "XXL"]
            if values.get("size") not in allowed_sizes:
                raise ValueError(f"invalid size, allowed values are {allowed_sizes}")

            return values
