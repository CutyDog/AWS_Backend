import json
import boto3

from boto3.dynamodb.conditions import Key	#Keyオブジェクトを利用できるようにする

dynamodb = boto3.resource('dynamodb')	#Dynamodbアクセスのためのオブジェクト取得
table = dynamodb.Table("demo-person")	#指定テーブルのアクセスオブジェクト取得

# テーブルスキャン
def operation_scan():
    scanData = table.scan()	#scan()メソッドでテーブル内をscan。一覧を取得
    items=scanData['Items']	#応答からレコード一覧を抽出
    print(items)	#レコード一覧を表示
    return scanData

# レコード検索
def operation_query(partitionKey):
    queryData = table.query(	#query()メソッドでテーブル内を検索
        KeyConditionExpression = Key("person_id").eq(partitionKey)	#検索キー(person_id)を設定
    )
    items=queryData['Items']	#応答から取得レコードを抽出
    print(items)	#取得レコードを表示
    return queryData
    
# レコード追加・更新
def operation_put(partitionKey, name):
    putResponse = table.put_item(	#put_item()メソッドで追加・更新レコードを設定
        Item={	#追加・更新対象レコードのカラムリストを設定
            'person_id': partitionKey,
            'name': name,
        }
    )
    if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:	#HTTPステータスコードが200 OKでないか判定
        print(putResponse)	#エラーレスポンスを表示
    else:
        print('PUT Successed.')
    return putResponse

# レコード削除
# def operation_delete(partitionKey, sortKey):
#     delResponse = table.delete_item(	//delete()メソッドで指定テーブルを削除
#       key={	//Keyオブジェクトで削除対象レコードのキー設定
#           'DeviceID': partitionKey,
#           'SensorID': sortKey
#       }
#     )
#     if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:	//HTTPステータスコードが200 OKでないか判定
#         print(delResponse)	//エラーレスポンスを表示
#     else:
#         print('DEL Successed.')
#     return delResponse

def lambda_handler(event, context):	#Lambdaから最初に呼びされるハンドラ関数
    print("Received event: " + json.dumps(event))	#引数：eventの内容を表示
    OperationType = event['OperationType']	#引数から操作タイプを取得
    try:
        if OperationType == 'SCAN':	#OperationTypeが'SCAN'か判定
            return operation_scan()
        PartitionKey = event['Keys']['person_id']	#引数からDeviceIDの値を取得
        if OperationType == 'QUERY':	#OperationTypeが'QUERY'か判定
            return operation_query(PartitionKey)
        elif OperationType == 'PUT':	#OperationTypeが'PUT'か判定
            Name = event['Keys']['name']	#引数からnameの値を取得
            return operation_put(PartitionKey, Name)
        # elif OperationType == 'DELETE':	//OperationTypeが'DELETE'か判定
        #     return operation_delete(PartitionKey, SortKey)
    except Exception as e:
        print("Error Exception.")
        print(e)