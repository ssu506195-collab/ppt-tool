# 圖解的來源與範圍

本專案沒有執行 ANSYS 求解。assets/diagrams/ 的 23 張 SVG 是原創教學圖，動畫與配色是說明用呈現，沒有實測頻率、真實變形量或收斂數據。

## 彎曲振型
以 Euler–Bernoulli 均勻懸臂樑模型計算同方向前三個彎曲形狀：phi(x)=cosh(beta*x)-cos(beta*x)-sigma*(sinh(beta*x)-sin(beta*x))，其中 x 是 x/L，sigma=(cosh(beta)+cos(beta))/(sinh(beta)+sin(beta))。每個振型按自由端絕對值正規化；不輸出實際位移單位。
特徵根為 1.8751040687、4.6940911330、7.8547574382，符合 cosh(beta)*cos(beta)+1=0。
來源：https://lampz.tugraz.at/~hadley/memm/mechanics/cbeam.php
原廠理論教材：https://innovationspace.ansys.com/courses/courses/cantilever-beam-modal-analysis/lessons/pre-analysis-start-up-lesson-2-32/topic/pre-analysis/

## 時間與配色
動畫以共同的展示速度往返，不依真實頻率播放。展示倍率是視覺放大，不代表改變受迫振幅。藍色至橘色表示相對位移大小；正反向由形狀顯示，顏色不代表應力或位移正負。顏色使用該型態、該倍率在最大展示相位的最大位移作正規化，其他相位的顏色會隨瞬間位移縮小。側面使用固定淡綠填色輔助辨識厚度，只有上表面採相對位移色階。

## 側彎與扭轉
側向彎曲沿另一方向展示同一階梁理論形狀。扭轉使用 theta(x)=0.8*sin(pi*x/2)*phase*display_amplitude 的幾何插值，僅表達截面繞長軸旋轉，不描述真實扭轉特徵頻率或截面翹曲。A～E 不是任何 3D 模型的前五階排序。

## 其他概念圖
拘束、工作流程、剛體與彈性運動、網格細化及結果閱讀，皆為概念圖，不是軟體截圖。結果閱讀圖的頻率欄為「待求解」，網格圖不附造假的收斂曲線。

## 重建與測試
python scripts/make_diagrams.py 會重建 SVG；python scripts/build.py 也會先重建圖解。
node scripts/test_modes.cjs 檢查特徵根、固定端、自由端、內部節點與方向區別。

## V3 多物理圖解與互動
新增 10 張 SVG：電位與場、理想邊界、尖角、碰撞幾何、理想能量交換、求解步與輸出、流體域、速度剖面、收斂三向檢查與四專區入口。由 scripts/make_multiphysics_diagrams.py 重建，build.py 會一併呼叫。

- 電場互動：E = |ΔV|/d，d 從 mm 換 m；色帶以各次電位差正規化，箭頭不以長度代表場強。均勻介質、無空間電荷，不含邊緣效應。
- 碰撞互動：無阻尼的單自由度質量與只受壓彈簧，k = 10000 N/m，接觸前間隙 0.02 m。接觸時 δ = v/ω sin(ωτ)，ω = sqrt(k/m)，接觸持續 π/ω；K = mv²/2、U = kδ²/2。與三維方塊教學案例的材料、尺寸及波傳問題分開。
- 通道互動：充分發展平行板層流 u(η)=6 Umean η(1−η)，η=y/H；umax=1.5 Umean、Dh=2H、−dp/dx=12 μUmean/H²。圖的水平速度尺度按當次 umax 正規化；顯示值保留物理單位。粒子僅作慢放示意，不模擬入口發展。

理論與軟體依據見各篇文章的 sources。node scripts/test_labs.cjs 檢查單位、場強反比、剖面平均值與壁面零速度、壓降尺度、碰撞全程能量與接觸邊界。
