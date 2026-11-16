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

