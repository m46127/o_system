import streamlit as st
import pandas as pd
import io
import base64

def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Download {file_label}</a>'
    return href

def main():
    st.title("Inventory Management System")
    uploaded_picking_file = st.file_uploader("Choose a Picking Excel file", type="xlsx", key="picking")
    uploaded_inventory_file = st.file_uploader("Choose an Inventory Excel file", type="xlsx", key="inventory")
    
    if uploaded_picking_file and uploaded_inventory_file:
        # ピッキングリストのExcelファイルを読み込む
        picking_df = pd.read_excel(uploaded_picking_file, usecols=['SKU', '合計数量'])
        picking_df['SKU'] = picking_df['SKU'].astype(str).str.strip().str.upper()

        # 在庫表のExcelファイルを読み込む
        inventory_df = pd.read_excel(uploaded_inventory_file, header=5, usecols=[2])  # 6行目をヘッダーとして、'C'列を使用
        inventory_df.columns = ['SKU']  # 読み込んだ列に 'SKU' という名前を設定
        inventory_df['SKU'] = inventory_df['SKU'].astype(str).str.strip().str.upper()
        
        # ピッキングリストと在庫表をマージ
        merged_df = pd.merge(inventory_df, picking_df, on='SKU', how='left')
        merged_df['合計数量'].fillna(0, inplace=True)  # 数量がない場合は0で埋める
        
        # ファイルをダウンロードするためのリンクを作成
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            merged_df.to_excel(writer, sheet_name='Sheet1', index=False)

        binary_excel = output.getvalue()
        st.markdown(get_binary_file_downloader_html(binary_excel, 'Merged_Inventory.xlsx'), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
