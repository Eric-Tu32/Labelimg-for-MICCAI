## LabelImg 加入功能（詳細看Git紀錄）

- 滾動檢視
  1. 在./libs/canvas中的init和wheelEvent新增scrollNextRequest，快捷鍵是shift+滾輪
  2. 在./labelimg.py中加入相對應修正(他是從canvas emit event到main)

- 預設標籤
  1. 把預設標籤改成CMB，後續可以加入其他需要的，可以在.\data\predefined_classes.txt做修改
  2. 把使用預設標籤打開：self.use_default_label_checkbox.setChecked(True)

- 自動儲存/輸出格式
  1. 預設自動儲存：self.auto_saving.setChecked(True)
  2. 因為設定是在更改顯示圖片時自動儲存，因此最後一張可能要手動儲存(ctrl+s)，但關閉程式時應該會有提醒

- 同時標注前後圖片（快捷鍵：W進繪圖模式，按住Ctrl開啟同步標注）
  1. 改邊框顏色：canvas裡的set_last_label()和其他東東，如果有按Ctrl繪圖邊框變色，存檔後顏色恢復
  2. 儲存：修改save_file和_save_file
  3. 對Shape class和在paintEvent加入is_diffuse，但按Ctrl的時候滑鼠要是移動狀態