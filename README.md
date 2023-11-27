# LATIA112-1 HW03

## TODO
- [x] Part 1 (寫在 README 下面)
  - [x] 先了解Azure語言服務有哪些
  - [x] 請試著規劃一個運用語言服務的教育應用
  - [x] 做一個小實作
- [x] Part 2
  - [x] 顯示分數
  - [x] 中文：正向/中性/負向
  - [x] 把取得的主詞也顯示出來
    - [x] 主詞
    - [x] 該主詞的分數與情緒分向

## Part 1 的回答
* 先了解Azure語言服務有哪些
  * Ans: 我發現該套件包 `TextAnalyticsClient` 還有抓出關鍵詞的種類的 api [recognize_entities](https://learn.microsoft.com/zh-tw/python/api/azure-ai-textanalytics/azure.ai.textanalytics.textanalyticsclient?view=azure-python#azure-ai-textanalytics-textanalyticsclient-recognize-entities) 可以使用，這個 api 提供我們將文字中的「實體」識別並「分類」為人員、地點、組織、日期/時間、數量、百分比、貨幣等等。
* 請試著規劃一個運用語言服務的教育應用
  * 使用上述的 api，可以給予其一篇文章，如教科書的文章或閱讀題，將所有「實體的分類」標記出來，以方便快速地了解整篇文章或閱讀題的「實體」，以提供初步構思時的畫面呈現。
* 做一個小實作
  * 寫在 `app.py` `azure_sentiment` function 的下面，約第 125 行的位置。

## Virtual Environment

Recommend to use venv to isolate your environment.

```bash
$ python3.9 -m venv venv
$ source venv/bin/activate
```

## Dependancy

* Requirements.txt

  * ```bash
    $ pip install -r requirements.txt
    ```


## How To Use My Code

1. Install the dependancies
2. Note that I have set the port in my code, which is `8000`
3. ```py
   $ python app.py
   ```