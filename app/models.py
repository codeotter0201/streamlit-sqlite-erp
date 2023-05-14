from sqlalchemy.orm import sessionmaker, declarative_base, validates
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum, Float

class MyBase:
    engine = None
    Session = None
    Base = None

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.Base = declarative_base()

        # 定义商品模型类
        class Product(self.Base):
            __tablename__ = 'products'

            id = Column(String, primary_key=True)
            product_ts = Column(DateTime, nullable=False)
            name = Column(String(256), nullable=False)
            color = Column(String(64), nullable=False)
            size = Column(String(64), nullable=False)
            photo_path = Column(String(256), nullable=True)

            @validates('color')
            def validate_color(self, key, color):
                allowed_colors = ["紅", "綠", "藍", "黃", "黑", "灰"]
                if color not in allowed_colors:
                    raise ValueError(f"invalid color, allowed values are {allowed_colors}")
                return color

            @validates('size')
            def validate_size(self, key, size):
                allowed_sizes = ["S", "M", "L", "2L", "XL", "XXL"]
                if size not in allowed_sizes:
                    raise ValueError(f"invalid size, allowed values are {allowed_sizes}")
                return size

        class Detail(self.Base):
            __tablename__ = 'detail'

            id = Column(String, ForeignKey('products.id'), primary_key=True)
            detail_ts = Column(DateTime, default=DateTime, primary_key=True)
            quantity = Column(Float, nullable=False)
            price = Column(Float, nullable=False)
            type = Column(String, nullable=False)
            supplier = Column(String(256), nullable=True)
            note = Column(String(256), nullable=True)

        self.product = Product
        self.detail = Detail
        self.create_db()

    def create_db(self):
        self.Base.metadata.create_all(self.engine)

    def reset_db(self):
        self.Base.metadata.drop_all(self.engine)
        self.create_db()