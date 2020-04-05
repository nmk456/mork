import json
import os

import markovify
import pandas as pd


def get_channels():
    return [os.path.splitext(x)[0] for x in os.listdir("data")]


def load_data(limit=None):
    if limit:
        channels = get_channels()[:limit]
    else:
        channels = get_channels()
    return [pd.read_json(f"data/{channel}.json", orient='records', convert_dates=["time"]) for channel in
            channels]


def get_text(data):
    text = ""
    for channel in data:
        text += "\n".join(channel["content"].tolist())

    return text


class Morkov:
    def __init__(self):
        with open("morkov.json", 'r') as f:
            self.model = markovify.NewlineText.from_json(json.load(f))
        # self.data = load_data()
        # self.text = get_text(self.data)
        #
        # self.model = markovify.NewlineText(self.text)
        #
        # self.model_json = self.model.to_json()
        #
        # with open("morkov.json", 'w') as f:
        #     json.dump(self.model_json, f)

    def get_sentence(self):
        return self.model.make_sentence()


if __name__ == '__main__':
    Morkov()
