import streamlit as st
from streamlit_sortables import sort_items
from google.oauth2.service_account import Credentials
import gspread


service_account_info = st.secrets["google_service_account"]

st.subheader('アムオスF1順位予想2025')

#if 'car_number' in st.session_state:
if st.session_state['name'] == 'このカーナンバーは申請されていません。公式SNSのDMにて参加申請をしてください。':
    st.write("入力ページにて必要な情報を入力してください")
else:
    st.write(f"参加者名: {st.session_state['name']}")
    st.write(f"レース名: {st.session_state['race']}")

    original_items_q = [
        {'header': '予選順位：', 'items':['フェルスタッペン', 'ローソン', 'アントネッリ', 'ラッセル', 'ルクレール', 'ハミルトン', 'ノリス', 'ピアストリ', 'アロンソ','ストロール','ガスリー','ドゥーハン','アルボン','サインツ','角田','ハジャー','ヒュルケンベルグ','ボルトレート','オコン','ベアマン']},
    ]
    sorted_items_q = sort_items(original_items_q, multi_containers=True, direction='vertical')

    original_items_r = [
        {'header': '決勝順位：', 'items':['フェルスタッペン', 'ローソン', 'アントネッリ', 'ラッセル', 'ルクレール', 'ハミルトン', 'ノリス', 'ピアストリ', 'アロンソ','ストロール','ガスリー','ドゥーハン','アルボン','サインツ','角田','ハジャー','ヒュルケンベルグ','ボルトレート','オコン','ベアマン']},
        {'header': '決勝リタイア：',
            'items': []}
    ]
    sorted_items_r = sort_items(original_items_r, multi_containers=True, direction='vertical')

    # 予選順位のリストを取得
    sorted_qual = sorted_items_q[0]["items"]
    # 決勝順位のリストを取得
    sorted_race = sorted_items_r[0]["items"]
    # 決勝リタイアのリストを取得 (もし決勝でリタイアした車があれば)
    sorted_ret = sorted_items_r[1]["items"]

    driver_number = {'フェルスタッペン':1, 'ローソン':30, 'アントネッリ':12, 'ラッセル':63, 'ルクレール':16, 'ハミルトン':44, 'ノリス':4, 'ピアストリ':81, 'アロンソ':14,'ストロール':18,'ガスリー':10,'ドゥーハン':7,'アルボン':23,'サインツ':55,'角田':22,'ハジャー':6,'ヒュルケンベルグ':27,'ボルトレート':5,'オコン':31,'ベアマン':87}

    if st.button('提出'):
        # ここでカーナンバー、レース選択、並び替えられた順位などの情報を取得します
        # 実際のspreadsheetへの書き込み処理をここに追加します

        scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_info(service_account_info,scopes=scopes)
        client = gspread.authorize(creds)

        spreadsheet = client.open('F1順位予想企画2025')
        worksheet = spreadsheet.worksheet('参加者予想')

        fixed_order = [1, 30, 12, 63, 16, 44, 4, 81, 14, 18, 10, 7, 23, 55, 22, 6, 27, 5, 31, 87]
        # 予選とレースの結果を格納するリストを初期化
        data_qual = []
        data_race = []

        # 予選結果を data_qual リストに格納
        for driver_num in fixed_order:
            driver_name = list(driver_number.keys())[list(driver_number.values()).index(driver_num)]  #ナンバーからドライバー名を逆引き
            if driver_name in sorted_qual:
                qual_position = sorted_qual.index(driver_name) + 1
                data_qual.append(qual_position)
            else:
                data_qual.append(None)  # 予選データがない場合は None を追加

        # レース結果を data_race リストに格納、リタイアした場合は 'ret' を格納
        for driver_num in fixed_order:
            driver_name = list(driver_number.keys())[list(driver_number.values()).index(driver_num)]  #ナンバーからドライバー名を逆引き
            if driver_name in sorted_ret:
                data_race.append("ret")
            elif driver_name in sorted_race:
                race_position = sorted_race.index(driver_name) + 1
                data_race.append(race_position)
            else:
                data_race.append(None)  # レースデータがない場合は None を追加



        all_values = worksheet.get_all_values()
        max_col = max(len(row) for row in all_values)  # 最大列数を取得


        search_car_number = st.session_state['car_number']
        search_race = st.session_state['race']

        all_values = worksheet.get_all_values()

        # 条件を満たす列が存在するかどうかのフラグ
        column_exists = False

        # 全列を走査して条件を満たすか確認
        for col_index, col_values in enumerate(zip(*all_values), start=1):
            try:
                # 1行目を整数として、2行目を文字列として比較
                if int(col_values[0]) == int(search_car_number) and col_values[1] == search_race:
                    column_exists = True
                    #print(f"条件に合致する列は {col_index} 列目に存在します。")
                    break  # 条件を満たす列が見つかったらループを抜ける
            except ValueError:
                # int変換できない場合は、この列は無視（整数でないため条件に合わない）
                continue
        if column_exists:
                st.write('すでに提出済みです')
            # ここに特定の値が含まれている場合の処理を書く
        else:
            st.write('このままお待ちください')

            # dataリストの値を縦に入れる列を指定（最右列の次）
            target_col = max_col + 1

            worksheet.update_cell(1, target_col, st.session_state['car_number'])
            worksheet.update_cell(1, target_col+1, st.session_state['car_number'])

            worksheet.update_cell(2, target_col, st.session_state['race'])
            worksheet.update_cell(2, target_col+1, st.session_state['race'])

            worksheet.update_cell(3, target_col, '予選')
            worksheet.update_cell(3, target_col+1, '決勝')
            
 
            # dataリストの値を指定した列に縦に入れる
            for i, value in enumerate(data_qual, start=4):
                worksheet.update_cell(i, target_col, value)

            for i, value in enumerate(data_race, start=4):
                worksheet.update_cell(i, target_col+1, value)


            st.write('提出完了しました')

