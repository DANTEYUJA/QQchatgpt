import openai

def chatgpt(raw_message):
    # 这里需要输入我们api_key
    openai.api_key = "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"

    model_engine = "text-davinci-002"
    # 这里是我们需要输入问题
    prompt = raw_message[3:]
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message

import json
from sanic import Sanic

app = Sanic('qqbot')


@app.websocket('/qqbot')
async def qqbot(request, ws):
    """QQ机器人"""

    while True:
        data = await ws.recv()
        data = json.loads(data)
        print(json.dumps(data, indent=4, ensure_ascii=False))
        # if 判断是群消息且文本消息不为空
        if data.get('message_type') == 'group' and data.get('raw_message'):
            raw_message = data['raw_message']
            msg = raw_message[::-1]

            ret = {
                'action': 'send_group_msg',
                'params': {
                    'group_id': data['group_id'],
                    'message': msg,
                }
            }
            await ws.send(json.dumps(ret))
            '''当机器人收到gpt开始的消息后，机器人将后面的消息以参数传递到gpt这个方法结果，并把问的答案返回给msg。
            那么这里raw_message就是我们收到的消息，msg就是我们希望机器人发送的消息'''
        elif "chatgpt" in raw_message and raw_message.index("chatgpt") == 0:
            msg = chatgpt(raw_message[3:1])
            continue

if __name__ == '__main__':
    app.run(debug=True, auto_reload=True)
