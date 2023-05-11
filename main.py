import streamlit as st
from product_handler import ProductHandler

st.set_page_config(
    page_title="庫存管理系統",
    # page_icon=":otter:",  # https://icon-sets.iconify.design/fa6-solid/otter/
    layout="wide",
    # initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

@st.cache_resource
def ph():
    # Create a database connection object that points to the URL.
    ph = ProductHandler()
    return ph

st.write('---')

name = st.text_input('品名')
color = st.text_input('顏色')
size = st.text_input('尺寸')

st.write(f'{name}_{color}_{size}')

if st.button(f'新增商品檔案'):
    ph().create_product(name=name, color=color, size=size)


st.write('---')

st.write(ph().get_product_data().sort_values('product_ts', ascending=False).head(), use_container_width=True)


st.write('---')

id = st.selectbox('取得商品ID', ph().get_product_data().sort_values('product_ts', ascending=False)['id'].tolist())
if id is not None:
    ret = ph().get_product_by_id(id=id)
    st.write(ret)
    if st.button(f'刪除'):
        ph().delete_product(id=id)

st.write('---')

id = st.selectbox('取得商品細節', ph().get_product_data().sort_values('product_ts', ascending=False)['id'].tolist())
if id is not None:
    ret = ph().get_product_detail_by_id(id=id).sort_values('detail_ts', ascending=False)
    st.write(ret)
    # if st.button(f'刪除'):
    #     ph().delete_product(id=id)

