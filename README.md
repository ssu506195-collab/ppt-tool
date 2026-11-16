# ANSYS Lab Notes｜實驗室 ANSYS 學習與問題整理站

提供初學者可以接續使用的模擬筆記。第一版主題是 ANSYS Workbench 2024 R2 / Mechanical 模態分析；使用英文介面名稱搭配繁體中文說明。教學目前為文件查證，尚待 ANSYS 實機驗證。

## 快速瀏覽
開啟 docs/index.html 即可離線瀏覽。搜尋、文章類型篩選、已讀進度、手機導覽、振型播放與圖解放大都不需要 API。
若瀏覽器限制本機儲存，已讀進度只在目前頁面暫存；網站內容仍可閱讀。

## V2 圖解版新增內容
- 13 張可重建的原創 SVG 圖解；各篇依主題使用，不以同一張圖替代所有內容。
- 五種互動振型：一階 Z 向彎曲、Y 向側彎、二階與三階 Z 向彎曲、扭轉概念。可切換、播放／暫停、調整相位與展示倍率。
- 一句話摘要、螢光重點、並排概念卡與展開式觀察提示。
- 手機可點圖解放大，再左右捲動查看。沒有 JavaScript 時，SVG 連結仍可直接打開。
- 彎曲使用 Euler–Bernoulli 解析式；扭轉僅作幾何概念示意。沒有虛構 ANSYS 頻率或真實求解雲圖。

## 重新生成與檢查
需要 Python 3.10 以上，僅使用標準函式庫，不需要 pip 或 npm。

```sh
python scripts/build.py
python scripts/check.py
node scripts/test_modes.cjs
python -m http.server 8000 --directory docs
```

瀏覽 http://localhost:8000 。Windows 的 Python 啟動指令若為 py，可將上述 python 改成 py。

## 上傳 GitHub 與啟用 Pages
1. 建立新的 GitHub Repository（儲存庫），例如 ansys-lab-notes。若希望老師直接瀏覽，使用可公開存取的儲存庫與網頁。
2. 解壓縮完整專案。將「專案資料夾內」的 AGENTS.md、README.md、content、templates、scripts、assets、docs 等一起上傳到儲存庫根目錄；不要只上傳 ZIP，也不要只傳 docs。
3. 在 GitHub 的 Settings（設定）→ Pages（頁面），Source（來源）選 Deploy from a branch（從分支部署）。
4. Branch（分支）選 main，Folder（資料夾）選 /docs，按 Save（儲存）。
5. 等待 GitHub Pages 完成。網址通常是 https://<帳號>.github.io/<儲存庫名稱>/ 。以 Pages 顯示的實際連結為準。
6. 開啟網站，檢查首頁、四篇文章、搜尋及 AGENTS.md，再填入 SUBMISSION.md 的實際連結。

不需要填任何 API key，也不需要建置工作流程。若使用其他分支，請選實際存放檔案的分支。
V2 另外附根目錄 index.html 自動導向 docs/index.html；即使 Pages 暫時仍使用 / (root)，也能進入網站，不會再只顯示 README。建議的正式設定仍為 main /docs。

## 如何新增內容
AI 先讀 AGENTS.md，再依 content/schema.md 複製 templates/article.json 建立 content/articles/<slug>.json。
執行 build.py 後，文章、首頁、分類頁與搜尋資料自動更新。不要只改 docs 中的生成檔。
新增後執行 check.py、人工檢查畫面並更新 CHANGELOG.md，最後將來源與 docs 一起提交。

## 驗證與資料來源
各篇文章附有官方文件連結及支援範圍。尺寸與材料是自訂教學案例，幾何圖為原創示意，不是求解雲圖。
網站自動檢查不等於模擬實機驗證。只有完成操作並留有操作者、日期與證據，才能改成「實機驗證」。
本專案獨立整理，與 ANSYS 無隸屬關係。官方文件仍以其原始著作權與使用條款為準；不要上傳機密模型、授權檔或未經同意的研究資料。

## 圖解與風格參考
視覺節奏參考老師提供的 DiveAI 講義庫（https://diveai-lab.github.io/diveai-lessons/）中短段落、重點標記與圖文搭配的方式。本專案的內容、程式、梁形圖及配色元件獨立製作，未使用其角色圖、商標或講義原文。
梁理論來源與適用範圍見各篇參考來源，以及 DIAGRAMS.md。
