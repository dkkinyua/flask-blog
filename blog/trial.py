from itsdangerous import URLSafeTimedSerializer

secret_key = 'secreT_key'
serializer = URLSafeTimedSerializer(secret_key)
token = serializer.dumps({'user_id': 1}).encode('utf-8')
print(token)