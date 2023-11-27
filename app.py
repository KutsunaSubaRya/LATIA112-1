import sys
import configparser
import typing

# Azure Text Analytics
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)

# Config Parser
config = configparser.ConfigParser()
config.read('config.ini')

# Config Azure Analytics
credential = AzureKeyCredential(config['AzureLanguage']['API_KEY'])

app = Flask(__name__)

channel_access_token = config['Line']['CHANNEL_ACCESS_TOKEN']
channel_secret = config['Line']['CHANNEL_SECRET']
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

handler = WebhookHandler(channel_secret)

configuration = Configuration(
    access_token=channel_access_token
)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):
    sentiment_result = azure_sentiment(event.message.text)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=sentiment_result)]
            )
        )


def azure_sentiment(user_input):
    text_analytics_client = TextAnalyticsClient(
        endpoint=config['AzureLanguage']['END_POINT'],
        credential=credential)
    documents = [user_input]
    response = text_analytics_client.analyze_sentiment(
        documents,
        show_opinion_mining=True,
        language="zh-Hant")
    docs = [doc for doc in response if not doc.is_error]
    ret = ""
    for idx, doc in enumerate(docs):
        ret += "------------------------------\n\n以下是分析句子中的情緒程度的綜合分數：\n\n"
        ret += "    正向程度分數："
        ret += str(int(doc.confidence_scores.positive * 100)) + "分\n"
        ret += "    負向程度分數："
        ret += str(int(doc.confidence_scores.negative * 100)) + "分\n"
        ret += "    中立程度分數："
        ret += str(int(doc.confidence_scores.neutral * 100)) + "分\n"
        ret += "\n\n------------------------------\n\n以下是分析句子中的實體情緒評級分類：\n\n"
        if doc.sentiment == "positive":
            ret += "    評級：正向\n"
        elif doc.sentiment == "negative":
            ret += "    評級：負向\n"
        else:
            ret += "    評級：中立\n"

    for idx, doc in enumerate(docs):
        ret += "\n\n------------------------------\n\n以下是分析句子中的關鍵主詞的評級與評分：\n\n"
        for sentence in doc.sentences:
            ret += f"    句子 '{sentence.text}' 的情緒分析結果為：\n"
            if sentence.sentiment == "positive":
                ret += "        評級：正向\n"
            elif sentence.sentiment == "negative":
                ret += "        評級：負向\n"
            else:
                ret += "        評級：中立\n"
            ret += "        正向程度分數：" + str(int(sentence.confidence_scores.positive * 100)) + "分\n"
            ret += "        負向程度分數：" + str(int(sentence.confidence_scores.negative * 100)) + "分\n"
            ret += "        中立程度分數：" + str(int(sentence.confidence_scores.neutral * 100)) + "分\n"

    ret += "\n------------------------------\n\n以下是分析句子中的實體：\n\n"

    result = text_analytics_client.recognize_entities(documents)
    result = [review for review in result if not review.is_error]
    for idx, review in enumerate(result):
        for entity in review.entities:
            tmp_str = ""
            if entity.category == "Person":
                tmp_str = "人名"
            elif entity.category == "Location":
                tmp_str = "地點"
            elif entity.category == "Organization":
                tmp_str = "組織"
            elif entity.category == "Product":
                tmp_str = "產品"
            elif entity.category == "DateTime":
                tmp_str = "時間"
            elif entity.category == "PersonType":
                tmp_str = "人物類型"
            elif entity.category == "Quantity":
                tmp_str = "數量"
            elif entity.category == "Event":
                tmp_str = "事件"
            elif entity.category == "Skill":
                tmp_str = "技能"
            elif entity.category == "URL":
                tmp_str = "網址"
            elif entity.category == "Email":
                tmp_str = "電子郵件"
            elif entity.category == "PhoneNumber":
                tmp_str = "電話號碼"
            elif entity.category == "Address":
                tmp_str = "地址"
            elif entity.category == "IP":
                tmp_str = "IP"
            ret += f"    該實體 '{entity.text}' 的分類為： '{tmp_str}'\n"
    return ret


if __name__ == "__main__":
    app.run(port=8000)
