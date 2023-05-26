import time


class LambdaHelper:
    @staticmethod
    def handle_response(r):
        code = r['StatusCode']
        match code:
            case 200:
                data = r['Payload'].read().decode('utf-8')
                return data
            case 429:
                print("Bad API response: 429. Retrying...")
                time.sleep(2)
            case _:
                print(f"Bad API response: {code}")
