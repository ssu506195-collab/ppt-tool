# 文章資料規格
每篇為 UTF-8 JSON；檔名等於 slug.json。slug 僅允許小寫英文、數字與單一連字號，且以英文字母開頭。
category 對應 modules.json 的 id。kind 只能是 concept、tutorial、troubleshooting。
version 填 2024 R2。minutes 為正整數。updated 為 YYYY-MM-DD。
verification 為「文件查證／待實機驗證」或「實機驗證」；實機驗證須填 tested_by、tested_on、evidence，evidence 為儲存於 assets/ 下的相對檔案路徑陣列。
prerequisites、tags、related 為文字陣列；related 指向既有文章 slug，不得指向自己。
sources 是 {title,url,version,support} 陣列，至少一筆，url 必須是 https 官方文件或原始研究連結，support 說明所支持的內容。
sections 為 {id,title,blocks} 陣列，id 使用 kebab-case。
blocks 支援：
- {"type":"p","text":"純文字"}
- {"type":"list","items":["項目一","項目二"]}
- {"type":"steps","items":[{"title":"步驟","text":"路徑、選取對象、數值、用途與檢查"}]}
- {"type":"table","headers":["欄一","欄二"],"rows":[["值一","值二"]]}
- {"type":"note","title":"注意","text":"提示內容"}
- {"type":"formula","text":"(K − ω²M)φ = 0"}
- {"type":"beam"}：共用原創懸臂樑幾何示意圖；不可宣稱是 ANSYS 雲圖。
所有文字均經 HTML escape；不要在內容中寫 HTML 或 Markdown 語法。
必要段落標題見 AGENTS.md 第 5 節，必須含對應詞語。


## V2 圖解與重點區塊
所有文字可使用 **粗體** 與 ==重點標記==；渲染前先 escape，不接受原始 HTML。
- spotlight：{type,label,text}，每篇的短摘要或觀察提示。
- figure：{type,src,title,alt,caption}，src 指向 assets/diagrams/ 的 SVG，所有欄位必填。圖說交代示意範圍與是否實機。
- modes：{type:"modes"}，沿用共用五型態振型互動，不自行硬編實際頻率或三維階數。
- compare：{type,items:[{title,text}]}，二至三個並排概念或比較。
- details / checkpoint：{type,title,items:["段落"]}，以可展開說明補充觀念或思考提示。
圖解資料依據 scripts/make_diagrams.py 與 assets/modal-math.js，彎曲振型以解析式繪製。數學測試位於 scripts/test_modes.cjs。

## V3 多物理互動與分類
- lab：{"type":"lab","name":"electrostatic"}；name 僅可為 electrostatic、impact、channel。使用共用解析模型與明確單位，不新增虛構求解結果。
- modules.json 每分類包含 id、name、tool、desc、ready、route（文章 slug 陣列）、lab、cover、environment。新增文章請在 route 加入閱讀順序；首頁分類與入口由此產生。
- 新圖解集中 scripts/make_multiphysics_diagrams.py；新互動共用 scripts/labs.py、assets/labs.js、assets/lab-math.js。修改公式後執行 node scripts/test_labs.cjs。
