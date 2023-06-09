# 動機
自家是傳統行業中的服飾攤販，還在使用傳統的紙本統計庫存，花了不少時間做庫存管理，相當不便也容易發生失誤。

研究市面上的電商和 POS 系統，發現每個都很棒，有相當完整的庫存管理系統，也有網路行銷、金流設定等等的服務，但對於每年千萬左右營收規模而言，不一定能用到平台提供的多元化服務，更可能在使用服務時，出現低效、價格高昂、員工學習成本過高的問題。

經過討論評估，認為庫存管理是目前業務流程中花費時間較多，也比較難管理的部分，所以先設計一套低成本且容易上手的庫存管理系統，對於自家案例來說是CP值較高的一個起手選擇，如果員工使用效果不錯，也可以利用已經建立好的數據資料，與現成的電商服務無縫銜接。

# 使用框架與技術
> 目前預設的場景是每月1000筆左右的資料新增，總資料10000筆以內的查詢，所以如果數據量遠大於這個預設應該要考慮效能問題。

* Python: 3.10.0
* 前端: streamlit, plotly
* 後端: pandas, sqlalchemy
* db: sqlite
* 資料結構
![](https://github.com/codeotter0201/erp/blob/master/erp.png)

# 使用畫面
![](https://github.com/codeotter0201/erp/blob/master/erp.gif)

# 快速使用
```shell
git clone https://github.com/codeotter0201/streamlit-sqlite-erp.git
```

```python
pip install --no-cache-dir -r requirements.txt
streamlit run main.py
```

# 未來優化方向
## 前端:
* 客製化視覺化圖表
* 帳號身份驗證功能

## DB:
* 異步插入資料的場景
* 查詢優化，減少對資料庫大範圍檢索

## 部署:
* dockerize
* 雲端伺服器上線、供桌電、手機端進行操作

## pytest

## 進銷條碼登錄系統