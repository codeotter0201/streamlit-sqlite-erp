import streamlit as st
import pandas as pd

ph = st.session_state['ph']

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
    st.session_state['select_product_ids'] = id
    st.write('---')
    if len(id) > 0:
        for i in id:
            add_detail_section(id=i)

def sidebar_section():
    with st.sidebar:
        add_detail()

def main_section():
    ids = st.session_state['select_product_ids']
    
    all_data = ph().get_detail_data().sort_values('detail_ts', ascending=False)
    if len(ids) > 0 :
        all_data = all_data[all_data['id'].isin(ids)]
    all_data.insert(0, '刪除', False)
    col1, col2, col3 = st.columns([4,1,1])
    with col1:
        st.subheader('所有訂單')

    # with col3:
    #     if st.button('全部選取', use_container_width=True):
    #         all_data['刪除'] = True

    # with col3:
    #     if st.button('全部取消', use_container_width=True):
    #         all_data['刪除'] = False

    
    edited_df = st.experimental_data_editor(all_data, use_container_width=True)
    temp_df = edited_df[edited_df['刪除']].copy()
    st.subheader('刪除訂單')
    

    # col21, col22 = st.columns([1, 1])

    # with col21:
    #     if st.button('全部選取', use_container_width=True):
    #         temp_df = edited_df
    #     else:
    #         temp_df = edited_df[edited_df['刪除']].copy()
    #         temp_df.drop(columns=['刪除'], inplace=True, axis=1)

    # with col22:
    #     if st.button('全部取消', use_container_width=True):
    #         temp_df = pd.DataFrame()

    st.dataframe(temp_df, use_container_width=True)

    
    if st.button(f'刪除選取商品', use_container_width=True):
        for i, r in temp_df.iterrows():
            st.write(r.id)
            ph().delete_detail(ts=r.detail_ts)
    
    


    # id = st.multiselect('select_delete_product_details', all_data['id'].tolist(), label_visibility='hidden')
    # deleted_list = []
    # if len(id) > 0:
    #     temp_df = pd.DataFrame()
    #     for i in id:
    #         temp_df = pd.concat([temp_df, ph().get_product_detail_by_id(id=i)])
    #     st.dataframe(temp_df, use_container_width=True)
    #     col1, col2 = st.columns([5, 7])
    #     with col2:

        # if len(deleted_list) > 0:
        #     st.success(f'刪除成功\n{deleted_list} ')

sidebar_section()
main_section()