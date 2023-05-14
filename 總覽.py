import streamlit as st
from product_handler import ProductHandler
import pandas as pd

st.set_page_config(
    page_title="庫存管理系統",
    layout="wide",
)

@st.cache_resource
def ph():
    # Create a database connection object that points to the URL.
    ph = ProductHandler()
    return ph

st.session_state['temp_product'] = []
st.session_state['ph'] = ph

def get_product_info():
    df = ph().get_detail_data()
    gp = df.groupby('id')
    df = dict(
        total_purchace = gp.apply(lambda x:(x.price * x.quantity)[x.type=='IN'].sum()),
        total_sellout = gp.apply(lambda x:(x.price * x.quantity)[x.type=='OUT'].abs().sum()),

        total_orders = gp.apply(lambda x:x.shape[0]),
        total_buy_orders = gp.apply(lambda x:x[x.type=='IN'].shape[0]),
        total_sell_orders = gp.apply(lambda x:x[x.type=='OUT'].shape[0]),

        avg_buy_price = gp.apply(lambda x:(x.price)[x.type=='IN'].abs().mean()).round(),
        avg_sell_price = gp.apply(lambda x:(x.price)[x.type=='OUT'].abs().mean()).round(),

        total_buy_amount = gp.apply(lambda x:x[x.type=='IN'].quantity.sum()),
        total_sell_amount = gp.apply(lambda x:x[x.type=='OUT'].quantity.sum()).abs(),

    )

    df = pd.DataFrame(df)
    df['diff_amount'] = df.total_sellout - df.total_purchace
    df['profit_percent'] = (df.avg_sell_price / df.avg_buy_price) - 1
    return df

def get_portfolio_info():
    df = ph().get_detail_data()
    df = dict(
        total_products = df.id.unique().shape[0],
        total_orders = df.shape[0],
        total_purchace_amount = df.price[df.type=='IN'].sum(),
        total_sellout_amount = df.price[df.type=='OUT'].abs().sum(),
    )
    return pd.DataFrame([df])

# df = ph().get_product_data()
# df = get_portfolio_info()
# df = get_product_info()
df = ph().get_detail_data()

st.dataframe(df, use_container_width=True)