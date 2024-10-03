# main.py
import streamlit as st
from streamlit_option_menu import option_menu

# メニューの選択肢を定義
menu_options = ["トップページ", "ピッキング","並び替え", "PDF作成", "在庫","追加数量","送料"]

# サイドバーでオプションメニューを表示
selected_option = option_menu("メインメニュー", menu_options, icons=['house', 'upload', 'sort', 'file-pdf', 'layers', 'box'], menu_icon="cast", default_index=0)


# 選択肢に応じて表示するページを変更
if selected_option == "トップページ":
    # トップページの内容
    st.title("トップページ")
    st.write("ようこそ！")

elif selected_option == "ピッキング":
    # pick.py の内容をインポートして実行
    from pick import picking_page
    picking_page()

elif selected_option == "並び替え":
    # pick.py の内容をインポートして実行
    from sort import main as sort_main
    sort_main()


elif selected_option == "PDF作成":
    # pdf.py の内容をインポートして実行
    from pdf import main as pdf_main
    pdf_main()

elif selected_option == "在庫":
    # Inventory.py の内容をインポートして実行
    from inventory import main as Inventory_main
    Inventory_main()


elif selected_option == "追加数量":
    # Inventory.py の内容をインポートして実行
    from addition import main as addition_main
    addition_main()

elif selected_option == "送料":
    # Inventory.py の内容をインポートして実行
    from postage import main as postage_main
    postage_main()