import streamlit as st
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfgen import canvas
import pandas as pd
import os
import shutil
from PyPDF2 import PdfMerger, PdfReader
import glob
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

w, h = portrait(A4)

def create_pdf_files(uploaded_file):
    pdfmetrics.registerFont(TTFont('mmt', './fonts/GenShinGothic-Monospace-Medium.ttf'))
    output_files = []
    # output フォルダをクリーンアップ
    if os.path.exists('output'):
        shutil.rmtree('output')
    os.makedirs('output', exist_ok=True)
    
    # ファイルが空でないか確認
    uploaded_file.seek(0)
    if len(uploaded_file.read()) == 0:
        print("エラー: アップロードされたファイルが空です")
        return
    
    # ファイルをデータフレームに変換
    uploaded_file.seek(0)
    df = pd.read_excel(uploaded_file)

    for index, record in df.iterrows():
        # ファイルの指定
        output_file = f'./output/output_{index+1}.pdf'  # 完成したPDFの保存先
        output_files.append(output_file)
        # キャンバスの設定
        cv = canvas.Canvas(output_file, pagesize=(w, h))
        cv.setFillColorRGB(0, 0, 0)
        # 以下、PDF生成の処理...

        # フォントの設定
        cv.setFont('mmt', 12)

        # データの描画
        customer_id = record['顧客ID']
        if pd.isna(customer_id):
            customer_id_str = ''
        else:
            customer_id_str = str(int(customer_id))
        cv.setFont('mmt', 10) 
        cv.drawString(30, h - 120, f"顧客ID:{customer_id_str}")
        cv.drawString(30, h - 60, 'お買い上げ明細書兼領収書')
        cv.setFont('mmt', 12) 
        cv.drawString(30, h - 80, 'この度はお買い上げいただき、ありがとうございます。')
        cv.setFont('mmt', 10)
        cv.drawString(30, h - 140, f"{record['お届け先名称1']} 様")
        cv.drawString(30, h - 155, f"〒{record['お届け先郵便番号']}")
        cv.drawString(30, h - 170, str(record['お届け先住所1']))
        cv.drawString(30, h - 185, str(record['お届け先住所2']))
        cv.setFont('mmt', 8)
        cv.drawString(350, h - 60, str(record['ご依頼主名称1']))
        cv.drawString(350, h - 90, f"〒{record['ご依頼主郵便番号']}")
        cv.drawString(350, h - 105, str(record['ご依頼主住所1']))
        cv.drawString(350, h - 120, str(record['ご依頼主住所2']))
        cv.drawString(350, h - 135, 'TEL 0120-444-636(平日9:30~17:30)')

        # PDFの保存
        cv.showPage()
        cv.save()
    return output_files

def get_items(record):
    items_dict = {}
    for i in range(30):
        code = record[f'SKU{i + 1}']
        name = record[f'商品名{i + 1}']
        count = record[f'商品数量{i + 1}']

        if pd.notna(code):  # 商品コードが NaN でない場合
            if code not in items_dict:
                item = {
                    'code': code,
                    'name': name,
                    'count': count,
                }
                items_dict[code] = item
            else:
                items_dict[code]['count'] += count

    items = list(items_dict.values())
    return items

def merge_pdf_in_dir(dir_path, dst_path):
    l = glob.glob(os.path.join(dir_path, '*.pdf'))
    l.sort()

    merger = PdfMerger()
    for p in l:
        if not PdfReader(p).is_encrypted:
            merger.append(p)

    merger.write(dst_path)
    merger.close()

def main():
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
    if uploaded_file is not None:
        output_files = create_pdf_files(uploaded_file)
        merged_file = './output/merged.pdf'
        merge_pdf_in_dir('output', merged_file)

        with open(merged_file, "rb") as f:
            st.download_button(
                label="Download Merged PDF",
                data=f,
                file_name="merged.pdf",
                mime="application/pdf",
            )

# main関数を実行
if __name__ == "__main__":
    main()
