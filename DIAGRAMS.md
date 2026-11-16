# 圖解的來源與範圍

本專案沒有執行 ANSYS 求解。assets/diagrams/ 的 13 張 SVG 是原創教學圖，動畫與配色是說明用呈現，沒有實測頻率、真實變形量或收斂數據。

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
