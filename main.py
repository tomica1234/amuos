import streamlit as st
from streamlit_sortables import sort_items

st.subheader('順位予想')
st.number_input('カーナンバーを入力してください', min_value=0, max_value=100, step=1)





st.selectbox(
    'レースを選択してください',
    ['バーレーン', 'サウジアラビア', 'オーストラリア','鈴鹿','中国','マイアミ','エミリアロマーニャ','モナコ','カナダ','スペイン','オーストリア','イギリス','ハンガリー','ベルギー','オランダ','モンツァ','アゼルバイジャン','シンガポール','COTA','メキシコ','サンパウロ','ラスベガス','カタール','アブダビ'])

original_items = [
    {'header': '予選順位：', 'items':['フェルスタッペン', 'ペレス', 'ハミルトン', 'ラッセル', 'ルクレール', 'サインツ', 'ノリス', 'ピアストリ', 'アロンソ','ストロール','ガスリー','オコン','アルボン','サージェント','角田','リカルド','ボッタス','周','ヒュルケンベルグ','マグヌッセン']},
]
sorted_items = sort_items(original_items, multi_containers=True, direction='vertical')

original_items = [
    {'header': '決勝順位：', 'items':['フェルスタッペン', 'ペレス', 'ハミルトン', 'ラッセル', 'ルクレール', 'サインツ', 'ノリス', 'ピアストリ', 'アロンソ','ストロール','ガスリー','オコン','アルボン','サージェント','角田','リカルド','ボッタス','周','ヒュルケンベルグ','マグヌッセン']},
    {'header': '決勝リタイア：',
        'items': []}
]
sorted_items = sort_items(original_items, multi_containers=True, direction='vertical')

st.button('提出')
