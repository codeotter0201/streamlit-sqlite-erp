import streamlit as st
from product_handler import ProductHandler
import pandas as pd

def get_temp_data():
    try:
        return pd.read_pickle('temp_data.pkl')
    except:
        df = pd.DataFrame(
            dict(
                name=[],
                color=[],
                size=[],
                id=[]
            )
        )
        df.to_pickle('temp_data.pkl')
        return df

def add_temp_data(data:pd.DataFrame):
    df = get_temp_data()
    if data['id'].tolist()[0] not in df['id'].tolist():
        pd.concat([df, data]).to_pickle('temp_data.pkl')

def reset_temp_data():
    pd.DataFrame(
        dict(
            name=[],
            color=[],
            size=[],
            id=[]
        )
    ).to_pickle('temp_data.pkl')

def add_product():
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input('品名', key=None)
    with col2:
        color = st.selectbox('顏色', ["紅", "綠", "藍", "黃", "黑", "灰"])
    with col3:
        size = st.selectbox('尺寸', ["S", "M", "L", "2L", "XL", "XXL"])
    df = dict(
        name = name,
        color = color,
        size = size,
    )
    df['id'] = '_'.join([df["name"], df["color"], df["size"]])
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f'新增預備清單'):
            add_temp_data(pd.DataFrame([df]))
    with col2:
        if st.button(f'清空預備清單'):
            reset_temp_data()

    all_data = get_temp_data()
    if len(all_data) > 0:
        st.dataframe(all_data, use_container_width=True)
    else:
        st.info(':blue[預備清單無商品]')
        # st.info('預備清單無商品', unsafe_allow_html=True)

    if len(all_data) > 0:
        all_data = all_data.drop(columns=['id'], axis=1).to_dict('records')

        if st.button(f'建立所有檔案', use_container_width=True):
            for v in all_data:
                ph().create_product(**v)
            reset_temp_data()
            st.success(f'{all_data} 建立成功')

def add_detail_section(id:str):
    # st.write('---')
    st.warning(f'商品: {id}')
    # quantity, price, type, supplier, note=None
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    with col2:
        quantity = st.number_input('數量', value=50, step=1, max_value=1000, key=id)
    with col1: 
        price = st.number_input('價格', value=100, step=1, max_value=10000, key=id+'1')
    with col3:
        type = st.selectbox('類型', ["進貨", "出貨"], key=id+'1.5')
        type = 'IN' if type == '進貨' else 'OUT'
    with col4:
        supplier = st.text_input('供應商', key=id+'2')
    note = st.text_input('備註', key=id+'3')

    temp = dict(
        id=id,
        quantity=quantity,
        price=price,
        type=type,
        supplier=supplier,
        note=note
    )

    if st.button(f'確定新增', use_container_width=True, key=id+'4'):
        ph().create_product_detail(**temp)
        # st.write(temp)
        st.success(f'新增成功')
    st.write('---')

def add_detail():
    all_data = ph().get_product_data().sort_values('product_ts', ascending=False)
    id = st.multiselect('add_product_detail', all_data['id'].tolist(), label_visibility='hidden')
    st.write('---')
    if len(id) > 0:
        for i in id:
            add_detail_section(id=i)
        # ret = ph().get_product_detail_by_id(id=id[0])

        # st.write(ret)

    
    # col1, col2 = st.columns(2)
    # with col1:
    #     if st.button(f'新增預備清單'):
    #         add_temp_data(pd.DataFrame([df]))
    # with col2:
    #     if st.button(f'清空預備清單'):
    #         reset_temp_data()

    # all_data = get_temp_data()
    # if len(all_data) > 0:
    #     st.dataframe(all_data, use_container_width=True)
    # else:
    #     st.info(':blue[預備清單無商品]')
    #     # st.info('預備清單無商品', unsafe_allow_html=True)

    # if len(all_data) > 0:
    #     all_data = all_data.drop(columns=['id'], axis=1).to_dict('records')

    #     if st.button(f'建立所有檔案', use_container_width=True):
    #         for v in all_data:
    #             ph().create_product(**v)
    #         reset_temp_data()
    #         st.success(f'{all_data} 建立成功')

st.set_page_config(
    page_title="庫存管理系統",
    layout="wide",
)

st.session_state['temp_product'] = []

@st.cache_resource
def ph():
    # Create a database connection object that points to the URL.
    ph = ProductHandler()
    return ph

# st.write('---')

with st.sidebar:
    add_product_tag, add_detail_tag = st.tabs(['新增商品檔案', '新增商品細節'])
    with add_product_tag:
        add_product()
    with add_detail_tag:
        add_detail()
        # product_mode = False
        # add_product()
    # add_product()



product_tag, detail_tag, summary_detail, summary_all_tag = st.tabs(['商品總覽', '商品細節', '商品分析', '總庫存分析'])
all_data = ph().get_product_data().sort_values('product_ts', ascending=False)
with product_tag:
    st.dataframe(all_data, use_container_width=True)
    st.write('---')
    st.subheader('刪除商品')
    id = st.multiselect('select_delete_products', all_data['id'].tolist(), label_visibility='hidden')
    deleted_list = []
    if len(id) > 0:
        temp_df = pd.DataFrame()
        for i in id:
            temp_df = pd.concat([temp_df, ph().get_product_by_id(id=i)])
        st.dataframe(temp_df, use_container_width=True)
        col1, col2 = st.columns([5, 7])
        with col2:
            if st.button(f'刪除選取商品'):
                for i in id:
                    ph().delete_product(id=i)
                    deleted_list.append(i)
        if len(deleted_list) > 0:
            st.success(f'刪除成功\n{deleted_list} ')

with detail_tag:
    all_data = ph().get_detail_data().sort_values('detail_ts', ascending=False)
    st.dataframe(all_data, use_container_width=True)
    

    # st.write('---')

    # id = st.selectbox('取得商品細節', ph().get_product_data().sort_values('product_ts', ascending=False)['id'].tolist())
    # if id is not None:
    #     ret = ph().get_product_detail_by_id(id=id).sort_values('detail_ts', ascending=False)
    #     st.write(ret)
    #     # if st.button(f'刪除'):
    #     #     ph().delete_product(id=id)

