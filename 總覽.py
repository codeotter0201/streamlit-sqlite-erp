import streamlit as st
from product_handler import ProductHandler
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="庫存管理系統",
    layout="wide",
)

@st.cache_resource
def ph():
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
    detail_df = ph().get_detail_data()
    df = dict(
        total_products = detail_df.id.unique().shape[0],
        total_orders = detail_df.shape[0],
        total_purchace_amount = (detail_df.price * detail_df.quantity)[detail_df.type=='IN'].sum() / 10000,
        total_sellout_amount = (detail_df.price * detail_df.quantity)[detail_df.type=='OUT'].abs().sum() / 10000,
    )

    d = detail_df.detail_ts.dt.strftime('%Y-%m')
    gp = detail_df.groupby(d)
    df['current_add_products'] = gp.id.apply(set).apply(len).values[-1]
    df['current_orders'] = gp.count().id.values[-1]
    df['current_purchace_amount'] = int(round(gp.apply(lambda x:(x.price*x.quantity)[x.type=='IN'].sum() / 10000).values[-1], 0))
    df['current_sellout_amount'] = int(round(gp.apply(lambda x:(x.price*x.quantity)[x.type=='OUT'].abs().sum() / 10000).values[-1], 0))
    df['current_profit'] = df['current_sellout_amount'] - df['current_purchace_amount']
    return pd.DataFrame([df])

def get_portfolio_month_info():
    detail_df = ph().get_detail_data()
    d = detail_df.detail_ts.dt.strftime('%Y-%m')
    gp = detail_df.groupby(d)
    df = dict(
        total_products = gp.id.apply(lambda x:len(x.unique())),
        total_orders = gp.apply(lambda x:x.shape[0]),
        total_purchace_amount = gp.apply(lambda x:(x.price * x.quantity)[x.type=='IN'].sum()),
        total_sellout_amount = gp.apply(lambda x:(x.price * x.quantity)[x.type!='IN'].sum()),
    )
    df = pd.DataFrame(df)
    df['total_profit'] = df.total_sellout_amount - df.total_purchace_amount
    return df

def kpi(pmi:pd.DataFrame):

    # create three columns
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi4, kpi5, kpi6 = st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="商品總數 🛍️",
        value=pmi.total_products.sum(),
        delta=int(pmi.total_products.iloc[-1]),
        
    )

    kpi2.metric(
        label="訂單總數 📈",
        value=pmi.total_orders.sum(),
        delta=int(pmi.total_orders.iloc[-1]),
    )

    kpi4.metric(
        label="進貨總金額 💸",
        value=f'{int(round(pmi.total_purchace_amount.sum()/10000, 0))} 萬',
        delta=int(round(pmi.total_purchace_amount.iloc[-1] / 10000, 0)),
    )

    kpi5.metric(
        label="出貨總金額 💰",
        value=f'{int(round(pmi.total_sellout_amount.sum()/10000, 0))} 萬',
        delta=int(round(pmi.total_sellout_amount.iloc[-1] / 10000, 0)),
    )

    kpi6.metric(
        label="總利潤 💵",
        value=f'{int(round((pmi.total_sellout_amount.sum() - pmi.total_purchace_amount.sum()) / 10000, 0))} 萬',
        delta=int(round((pmi.total_sellout_amount - pmi.total_purchace_amount).iloc[-1] / 10000, 0)),
    )

# st.dataframe(pmi, use_container_width=True)
# st.dataframe(df1, use_container_width=True)
# print(pmi.total_profit, pmi.total_profit.cumsum())


def plot_fig(df):
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
               x=df.total_profit.index, 
               y=df.total_profit.cumsum(), 
               name="累積損益", 
               marker_color="red",
            #    line=dict(width=1)
        ), secondary_y=False
    )
    fig.add_trace(
        go.Bar(
               x=df.total_profit.index, 
               y=df.total_profit, 
               name="每月損益", 
               marker_color=["orange" if i > 0 else "gray" for i in df.total_profit],
               opacity=0.5
            #    line=dict(width=1)
        ), secondary_y=True
    )
    fig.update_layout(title='損益圖')
    st.plotly_chart(fig, use_container_width=True)

pmi = get_portfolio_month_info().iloc[23:]

kpi(pmi)
st.write('---')
plot_fig(pmi)

