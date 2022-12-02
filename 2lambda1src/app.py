from email.quoprimime import body_check
import json
import pymysql

endpoint = 'vital-xr-db1.cp5uk2brweds.us-east-1.rds.amazonaws.com'
username = 'admin'
password = 'vitalxr1234'
database_name = 'vitalxr'

#connection
connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    body = {}
    body["event"] = event

    result = []

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM organizations")

    rows = cursor.fetchall()

    for row in rows:
        result.append(row)


    response = {
        "statusCode": 200,
        "isBase64Encoded": False,
        "headers": {"x-test-header" : "foobar"},
        "body": json.dumps(result),
    }

    return response


def lambda_two_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    data = json.loads(event['body'])
    cursor = connection.cursor()

    sql = """INSERT INTO organizations(
   name, concurrent_users, total_users, isDeleted)
   VALUES  (%s, %s, %s, %s)"""
    val = (data["name"], data["concurrent_users"], data["total_users"], data["isDeleted"])

    try:
    # Executing the SQL command
        cursor.execute(sql, val)

    # Commit your changes in the database
        connection.commit();

    except:
    # Rolling back in case of error
        connection.rollback()

    # Closing the connection
# import requests
    response = {
        "statusCode": 200,
        "isBase64Encoded": False,
        "headers": {"x-test-header" : "foobar"},
        "body": json.dumps(data),
    }

    return response