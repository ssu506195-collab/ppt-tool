# ANSYS Lab Notes — AI 開發與內容規則

## 1. 專案目的與讀者
建立可傳承的實驗室模擬學習站，讓初學者依序理解觀念、完成操作、排除問題。目前包含 2024 R2 的 Mechanical 模態分析、Maxwell 靜電場、LS-DYNA 顯式碰撞與 Fluent 層流入門。Mechanical、LS-DYNA 與 Fluent 從 Workbench 進入；Maxwell 在 Electronics Desktop 操作，不混用各軟體選單。不要將本網站寫成已獲 ANSYS 認證的官方教材。

## 2. 每次工作先讀
先讀本檔、README.md、content/schema.md，再查看最接近的既有文章與 templates/article.json。先確認修改範圍；保留無關內容。沒有實機驗證證據時，不得標記為已操作成功。

## 3. 檔案結構與唯一資料來源
- content/articles/*.json：文章原始資料，一篇一檔。英文小寫 kebab-case 檔名必須等於 slug，例如 modal-mesh-check.json。
- content/modules.json：軟體分類。category 必須是此檔已宣告的 id。
- content/schema.md：欄位與區塊規格。
- templates/article.json：新增文章模板，不會發佈成文章。
- assets/style.css、assets/app.js、assets/beam.svg：全站共用樣式、互動與原創幾何示意圖。
- scripts/build.py：使用 Python 標準函式庫產生網站及檢查內容。
- docs/：生成的完整靜態網站，供 GitHub Pages 發佈；不可只修改此處而不改來源。
- README.md、SUBMISSION.md：操作部署說明與作業說明。

## 4. 語言與教學規則
全文用繁體中文。介面項目每次出現時寫作 English（中文名稱），例如 Fixed Support（固定支撐）。中文是理解用譯名，不宣稱為官方中文介面字串。版本固定 2024 R2；引用其他版本時必須註明差異。
操作步驟必須交代：所在應用程式／樹狀項目、操作路徑、選取對象、設定數值與單位、用途與檢查結果。不得只寫「設定好接觸」。Workbench、Mechanical、DesignModeler 的步驟必須區分。

## 5. 文章格式
所有文章填寫 slug、category、kind、title、summary、version、level、minutes、updated、verification、prerequisites、tags、sections、sources、related。
- concept（觀念）：學習目標、核心觀念、範例、常見誤解、重點整理。
- tutorial（操作）：學習目標、前置條件、案例參數、操作步驟、結果檢查、重點整理。
- troubleshooting（問題）：問題現象、適用情境、檢查順序、處理方式、完成條件、重點整理。
sources 與 related 是每篇必備欄位；related 為已存在 slug。未完成內容不要用空白頁充數；未建置分類以「規劃中」標示並可閱讀其規劃。

## 6. 技術內容與證據
優先引用 ANSYS 同版本官方文件；必要時使用原始論文或原廠教材。來源要寫名稱、URL、版本及支援範圍，不得編造引用。文獻說明、教學自訂設定、理論估算、實機結果須明確分開。
verification 僅可為「文件查證／待實機驗證」或「實機驗證」，後者必須提供 tested_by、tested_on 與 evidence（對應可存取的截圖或紀錄路徑）。沒有求解就不能填入看似實際的固有頻率、收斂表或振型雲圖。原創示意圖必須註明非求解結果。
每個案例提供幾何、材料、單位、拘束、網格、分析假設。模態振型的顯示振幅不可解釋為實際受迫振幅；近零頻率須依拘束與連通性判斷，不得自動當成錯誤。網格比較須追蹤相同振型，不能只比階數。
未公開研究資料、姓名、授權檔、API key、機密幾何與未經同意的截圖不可加入公開網站。

## 7. 視覺與互動
採用輕鬆的工程學習手帳風格：暖白點陣背景、深綠文字、天空藍／杏橘／淡黃／粉紫重點色，大標題、圓角卡片與可辨識的重點標記。保留共用 CSS 變數與版型。導覽、字級、最大閱讀寬度保持一致。支援 360px 手機到桌面、鍵盤操作、可見焦點、表格橫向捲動與減少動態效果偏好。搜尋、分類篩選、手機導覽、學習進度、列印必須保持可用。不要加入 API、登入、第三方追蹤或外部字型依賴。

## 8. 新增一篇文章的確切流程
1. 複製 templates/article.json 至 content/articles/<slug>.json，依 schema.md 填妥內容。
2. 設定 category、kind 與 related；閱讀並查證來源。在 content/modules.json 的 route 指定閱讀順序；新增分類時填妥 id、name、tool、desc、ready、route、lab、cover、environment。
3. 執行 python scripts/build.py。生成器會自動更新首頁、分類頁、搜尋資料及文章頁，不可手動複製多份導覽。
4. 執行 python scripts/check.py。錯誤必須修正再交付。
5. 執行 python -m http.server 8000 --directory docs，以瀏覽器確認新增文章、搜尋、相關文章連結與手機顯示。無法進行瀏覽器檢查時須如實回報。
6. 更新 CHANGELOG.md，說明修改與查證狀態；將來源與 docs 一起提交。

## 9. 完成與交付標準
不需要安裝前端套件。GitHub Pages 使用 main 分支 /docs。所有站內 URL 用相對路徑；不得硬編碼網域或根路徑 /assets，須支援 repository 子目錄部署。所有頁面必須有返回入口、來源、更新日期與適用版本。
提交前檢查 JSON、必要段落、參照、HTML 本機連結與資源完整性。檢查工具通過不代表 ANSYS 模擬已驗證。交付報告須清楚區分網站驗證與模擬驗證，且不可宣稱尚未完成的 GitHub 上傳或公開發佈已成功。

## 10. 圖解與互動教學規則（2026-11-16 更新）
每篇至少一個與內容直接相關的圖解或互動元件；整個網站不可重複使用同一張懸臂樑圖取代所有說明。先以一句話摘要帶入，再用觀察提示引導讀圖，必要時用可展開區塊補充推導。使用 **粗體** 與 ==螢光標記== 強調少量關鍵詞，禁止整段標色。
彎曲振型依 Euler–Bernoulli 解析式繪製，固定端位移與斜率須為零；較高同方向彎曲振型須呈現相應內部節點。Y 向與 Z 向彎曲、不同彎曲階次與扭轉概念要區分，不可直接將圖例 A～E 宣稱為 3D ANSYS 前五階排序。扭轉若只是概念插值，明確寫「概念示意」。
模態互動圖明列來源、展示放大與時間縮放；顏色表示正規化相對位移，不是真實 mm、應力或求解結果。無 ANSYS 結果時，圖例統一寫「教學示意」，不套用假的 ANSYS 介面、結果頻率或日期。自動動畫預設暫停，使用者按播放才啟動，提供暫停／型態切換／展示倍率／相位控制，支援減少動態與列印靜態圖。
可用的新內容區塊：spotlight、figure、modes、compare、details、checkpoint；規格見 content/schema.md，渲染邏輯集中在 scripts/visuals.py。assets/diagrams/ 是可重建的原創 SVG，scripts/make_diagrams.py 管理幾何與振型數學。

## 11. 多物理專區規則（V3）
四個分類都必須有明確入門順序、觀念、可重建操作案例與排錯文章，不得僅切換分類標籤或重用懸臂樑內容。新增分類資料由 content/modules.json 驅動，首頁、搜尋與分類頁不得寫死為模態分析。
每個專區至少一個相關互動：模態振型、理想平行板電場、單自由度彈簧接觸能量、平行板通道解析速度剖面。所有公式與顯示值清楚標記為解析或簡化模型，不宣稱為 ANSYS 結果。
Maxwell 分開說明電位與電場，E=ΔV/d 僅適用於本文理想化均勻間隙；不可把所有外邊界稱作接地。LS-DYNA 使用其 Workbench 系統，區分初始速度與持續施加的速度拘束，區分求解時間步與輸出間隔；不用質量縮放掩蓋不合理結果。Fluent 本例是平面平行板流而非圓管，充分發展層流中心速度為平均的 1.5 倍，入口發展段不直接套用全長壓降公式。
新互動集中在 scripts/labs.py、assets/labs.js 與 assets/lab-math.js；圖解由 scripts/make_multiphysics_diagrams.py 產生。新增互動須驗證物理不變量與單位轉換。

修改振型或新互動後，分別執行 node scripts/test_modes.cjs 與 node scripts/test_labs.cjs。lab 區塊僅允許 electrostatic、impact、channel，透過共用渲染器產生。圖例需說清楚顏色、箭頭與正規化的意義。
