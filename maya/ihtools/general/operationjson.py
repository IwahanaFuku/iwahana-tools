import json, os

class Commomn():
    def convert_None(self):
        dict = {
        "aaa": 123,
        "bbb": "123",
        "ccc": "あいうえお",
        "ddd": "一二三",
        }

        basepath = r"C:\Users\iwahana\Documents\maya\scripts"
        json_file_name = 'test.json'
        path = os.path.join(basepath, json_file_name)
        print(path)

        with open(path, mode = "w", encoding = "utf-8") as f:
            json.dump(dict, f, indent=2, ensure_ascii=False)