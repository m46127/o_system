import streamlit as st
import pandas as pd
import os
from werkzeug.utils import secure_filename
from io import BytesIO

UPLOAD_FOLDER = 'uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx'}

def picking_page():
    st.title('ファイルアップロード')

    # 確認とディレクトリの作成
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    uploaded_file = st.file_uploader("ファイルを選択してください", type=['xlsx'])

    if uploaded_file is not None:
        if allowed_file(uploaded_file.name):
            filename = secure_filename(uploaded_file.name)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            with open(filepath, 'wb') as f:
                f.write(uploaded_file.getbuffer())

            df = pd.read_excel(filepath)

            item_code_name = {}
            item_code_num = {}
            for i in range(len(df)):
                customer = df.iloc[i]
                for x in range(29):  # 適宜変更してください。
                    item_code = customer.get(f"SKU{x+1}")
                    item_name = customer.get(f"商品名{x+1}")
                    item_num = customer.get(f"商品数量{x+1}")

                    if pd.notna(item_code) and pd.notna(item_name) and pd.notna(item_num):
                        if item_code not in item_code_name:
                            item_code_name[item_code] = item_name
                            item_code_num[item_code] = int(item_num)
                        else:
                            item_code_num[item_code] += int(item_num)

            sorted_items = sorted(
                item_code_name.keys(),
                key=lambda x: (x[0], int(x[1:]))
            )

            picking_datas = [["SKU", "商品名", "合計数量"]]
            for code in sorted_items:
                data = [code, item_code_name[code], item_code_num[code]]
                picking_datas.append(data)

            picking_datas_df = pd.DataFrame(picking_datas[1:], columns=picking_datas[0])

            excel_stream = BytesIO()
            picking_datas_df.to_excel(excel_stream, index=False)
            excel_stream.seek(0)

            st.download_button(
                label="Excelファイルをダウンロード",
                data=excel_stream,
                file_name='picking_list.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            st.error('許可されていないファイル形式です。Excelファイルをアップロードしてください。')
    else:
        st.info('ファイルをアップロードしてください。')

if __name__ == "__main__":
    picking_page()

