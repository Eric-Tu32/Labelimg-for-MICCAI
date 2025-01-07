## LabelImg 加入功能（詳細看Git紀錄）

- 滾動檢視
  1. 在./libs/canvas中的init和wheelEvent新增scrollNextRequest，快捷鍵是shift+滾輪
  2. 在./labelimg.py中加入相對應修正(他是從canvas emit event到main)

- 預設標籤
  1. 把預設標籤改成CMB，後續可以加入其他需要的，可以在.\data\predefined_classes.txt做修改
  2. 把使用預設標籤打開：self.use_default_label_checkbox.setChecked(True)

- 自動儲存/輸出格式
  1. 預設自動儲存：self.auto_saving.setChecked(True)