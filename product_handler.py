from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum, Float
from sqlalchemy.orm import sessionmaker, declarative_base, validates
import pandas as pd
from models import MyBase

class ProductHandler(MyBase):
    def __init__(self) -> None:
        super().__init__('sqlite:///goods.db')

    # 创建商品记录的函数
    def create_product(self, name:str, color:str=None, size:str=None, photo_path:str=None) -> None:
        with self.Session() as session:
            colors = ["紅", "綠", "藍", "黃", "黑", "灰"] if color is None else [color]
            size = ["S", "M", "L", "2L", "XL", "XXL"] if size is None else [size]
            for c in colors:
                for s in size:
                    s = s.upper()
                    id = f'{name}_{c}_{s}'
                    # 检查主键是否存在
                    product = session.query(self.product).filter_by(id=id).first()
                    if product is not None:
                        continue  # 如果存在就跳过
                    product = self.product(id=id, product_ts=pd.Timestamp.now(), name=name, color=c, size=s, photo_path=photo_path)
                    session.add(product)
                    session.commit()

    # 根据商品 ID 查找商品记录的函数
    def get_product_by_id(self, id:str):
        with self.Session() as session:
            p = session.query(self.product).filter_by(id=id).first()
            session.commit()
            df = pd.DataFrame([(p.id, p.name, p.color, p.size, p.photo_path, p.product_ts)],
                            columns=['id', 'name', 'color', 'size', 'photo_path', 'product_ts'])
            return df

    # 更新商品记录的函数
    def update_product(self, id, name=None, color=None, size=None, photo_path=None):
        with self.Session() as session:
            product = session.query(self.product).filter_by(id=id).first()
            if name:
                product.name = name
            if color:
                product.color = color
            if size:
                product.size = size
            if photo_path:
                product.photo_path = photo_path
            session.commit()
            return product

    # 删除商品记录的函数
    def delete_product(self, id):
        with self.Session() as session:
            product = session.query(self.product).filter_by(id=id).first()
            session.delete(product)
            session.commit()
            return product

    def get_product_data(self):
        with self.Session() as session:
            results = session.query(self.product).all()
        df = pd.DataFrame([(p.id, p.name, p.color, p.size, p.photo_path, p.product_ts) for p in results],
                        columns=['id', 'name', 'color', 'size', 'photo_path', 'product_ts'])
        return df

    # 创建商品记录的函数
    def create_product＿detail(self, id, quantity, price, type, supplier, note=None):
        with self.Session() as session:
            t = pd.Timestamp.now()
            # t -= pd.Timedelta(pd.Series(range(3000)).sample(1).values[0], 'day')
            # t += pd.Timedelta(pd.Series(range(3000)).sample(1).values[0], 'day')
            detail = self.detail(detail_ts=t , id=id, quantity=quantity, price=price, type=type, supplier=supplier, note=note)
            session.add(detail)
            session.commit()
            return detail

    # 根据商品 ID 查找商品记录的函数
    def get_product_detail_by_id(self, id):
        with self.Session() as session:
            results = session.query(self.detail).filter_by(id=id).all()
        df = pd.DataFrame([(d.id, d.detail_ts, d.quantity, d.price, d.type, d.supplier, d.note) for d in results], 
                        columns=['id', 'detail_ts', 'quantity', 'price', 'type', 'supplier', 'note'])
        return df

    def get_detail_data(self):
        with self.Session() as session:
            results = session.query(self.detail).all()
        df = pd.DataFrame([(d.id, d.detail_ts, d.quantity, d.price, d.type, d.supplier, d.note) for d in results], 
                        columns=['id', 'detail_ts', 'quantity', 'price', 'type', 'supplier', 'note'])
        return df.sort_values('detail_ts', ascending=False)

    def gen_random_data(self):
        ph = self
        for g in ['男', '女', '中性']:
            for pt in ['長褲', '瑜珈褲', '壓力褲','短褲','上衣','排汗衣']:
                ph.create_product(g+pt)

        type = ['IN', 'OUT']
        supplier = ['柏國', '蝦皮']
        for _ in range(10):
            for i in ph.get_product_data().id.sample(100).values:
                for t in type:
                    for s in supplier:
                        m = 3 if t == 'IN' else -1
                        ph.create_product＿detail(i, 
                                                 pd.Series([50,150,250]).sample(1).values[0] * m, 
                                                 500 + pd.Series([100,500,1500]).sample(1).values[0], 
                                                 t, 
                                                 s
                                                 )
