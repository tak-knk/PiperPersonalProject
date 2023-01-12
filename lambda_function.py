import json
import boto3
import datetime

def lambda_handler(event, context):

    body = json.loads(event['body'])

    for event in body['events']:

        userId = event['source']['userId']  #userID取得
        timezone = datetime.timezone(datetime.timedelta(hours=9))
        nowtime = datetime.datetime.now(timezone)  #時刻
        timestamp = nowtime.strftime('%Y/%m/%d %H:%M:%S')
        get_date = nowtime.strftime('%Y/%m/%d')
        get_time = nowtime.strftime('%H:%M:%S')
        dynamoDB = boto3.resource("dynamodb")
        table = dynamoDB.Table("testdb")  # DynamoDBのテーブル名

        #失敗通知が来た時の処理
        if event['message']['type'] == 'text' and str(event['message']['text']) == '失敗':

            # DynamoDBへのPut処理実行
            table.put_item(
                Item={
                    "userid": str(userId),  # Partition Key
                    'timestamp' : timestamp, #Sort Key
                    'date' : get_date,
                    'time' : get_time,
                    "message": str(event['message']['text'])  #Text内容
                })
                
        END
