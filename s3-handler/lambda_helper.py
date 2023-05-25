import time


class LambdaHelper:
    @staticmethod
    def handle_response(r):
        match r.status_code:
            case 200:
                data = r.json()
                return data
            case 429:
                print("Bad API response: 429. Retrying...")
                time.sleep(2)
            case 500:
                err = "Image doesn't contain a car"
                if r.json()['error'] == err:
                    print(err)
                else:
                    print(f"Bad API response: {r.status_code}")
            case _:
                print(f"Bad API response: {r.status_code}")
