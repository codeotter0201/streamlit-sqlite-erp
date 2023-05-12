import streamlit as st
import pandas as pd

ph = st.session_state['ph']

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

# def delete_last_data():
#     df = get_temp_data()
#     if len(df) > 0:
#         df = df.drop(df.index[-1])
#         df.to_pickle('temp_data.pkl')

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
        if st.button(f'加入清單', use_container_width=True):
            add_temp_data(pd.DataFrame([df]))
    with col2:
        if st.button(f'清空清單', use_container_width=True):
            reset_temp_data()

    all_data = get_temp_data()
    if len(all_data) > 0:
        st.dataframe(all_data, use_container_width=True)
    else:
        st.info(':blue[清單無商品]')

    if len(all_data) > 0:
        all_data = all_data.drop(columns=['id'], axis=1).to_dict('records')

        if st.button(f'新增所有商品', use_container_width=True):
            for v in all_data:
                ph().create_product(**v)
            reset_temp_data()
            if st.button(f'重新整理', use_container_width=True):
                pass
            st.success(f'{all_data} 建立成功')

def sidebar_section():
    with st.sidebar:
        add_product()

def main_section():
    all_data = ph().get_product_data().sort_values('product_ts', ascending=False)
    all_data.insert(0, '刪除', False)
    col1, col2 = st.columns([1, 1])
    st.subheader('所有商品')
    edited_df = st.experimental_data_editor(all_data, use_container_width=True)
    # st.write('---')
    # st.subheader('刪除商品')
    # goods_tab, update_tab, delete_tab = st.tabs(['庫存', '更新', '刪除'])
    update_tab, delete_tab = st.tabs(['更新', '刪除'])

    # with goods_tab:
    #     all_detail_data = ph().get_detail_data().sort_values('detail_ts', ascending=False)
    #     all_detail_data = all_detail_data[all_detail_data.id.isin(edited_df[edited_df['刪除']].id.tolist())]
    #     all_detail_data.insert(0, '刪除', False)
    #     edited_detail = st.experimental_data_editor(all_detail_data, use_container_width=True)
        # st.dataframe(edited_detail[edited_detail['刪除']], use_container_width=True)

    with delete_tab:
        st.dataframe(edited_df[edited_df['刪除']], use_container_width=True)
        id = edited_df[edited_df['刪除']]['id'].tolist()

        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button(f'確定刪除'):
                for i in id:
                    ph().delete_product(id=i)
                with col2:
                    if st.button(f'重新整理'):
                        pass
                with col3:
                    st.success(f'刪除成功\n{id} ')



    # id = st.multiselect('select_delete_products', all_data['id'].tolist(), label_visibility='hidden')



    # deleted_list = []
    # if len(id) > 0:
    #     temp_df = pd.DataFrame()
    #     for i in id:
    #         temp_df = pd.concat([temp_df, ph().get_product_by_id(id=i)])
    #     st.dataframe(temp_df, use_container_width=True)
    #     col1, col2 = st.columns([5, 7])
    #     with col2:
    #         if st.button(f'刪除選取商品'):
    #             for i in id:
    #                 ph().delete_product(id=i)
    #                 deleted_list.append(i)
    #     if len(deleted_list) > 0:
    #         st.success(f'刪除成功\n{deleted_list} ')

sidebar_section()
main_section()