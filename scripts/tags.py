import json
import gradio as gr
from modules import script_callbacks

handle_js_clipboard = '(text) => {console.log("text", text);try {if (navigator.clipboard){ navigator.clipboard.writeText(text);} else {let textarea = document.createElement("textarea");document.body.appendChild(textarea);textarea.style.position = "fixed";textarea.style.clip = "rect(0 0 0 0)";textarea.style.top = "10px";textarea.value = text;textarea.select();document.execCommand("copy", true);document.body.removeChild(textarea);}} catch (e) {console.error("复制剪切板发生异常", e);}}'
# 源数据
# data = []
# 选定数据
select_data = []

# json 源数据 文件路径
origin_file_path = './tags.json'
# 导入文件
with open(origin_file_path, 'r', encoding='utf-8') as fp:
    data = json.load(fp)
fp.close()


def handle_change_origin_data(x, d):
    # 输出
    # print(x)
    # print(d)
    if d in select_data:
        select_data.remove(d)
    else:
        select_data.append(d)
    return ','.join(select_data)


# 界面显示
def draw_main():
    with gr.Blocks(css="#real_data {width: 25%}") as app:
        with gr.Row():
            text_input = gr.Textbox(label='已选择内容')
        with gr.Row():
            copy_button = gr.Button(value='复制', variant='primary')
            copy_button.click(fn=None, _js=handle_js_clipboard, inputs=text_input, outputs=None)
        with gr.Row() as select_data_tabs:
            # 第一级大类型
            for types in data:
                # print(types['name'])
                with gr.Tab(types['name']):
                    # 第二级类型
                    for types2 in types['typeList']:
                        with gr.Tab(types2['name']):
                            with gr.Row():
                                # 第三级别核心内容循环
                                for real_data in types2['data']:
                                    is_in_side = False
                                    if real_data['englishname'] in select_data:
                                        is_in_side = True
                                    origin_data_cb = gr.Checkbox(
                                        value=is_in_side,
                                        label=real_data['englishname'] + '[' + real_data['chinesename'] + ']',
                                        show_label=True
                                    )
                                    real_name = real_data['englishname']
                                    origin_data_cb.change(fn=lambda x, r_n=real_name: handle_change_origin_data(x, d=r_n), inputs=origin_data_cb, outputs=text_input)


# app.launch()
def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as my_tags:
        draw_main()
    return (my_tags, "标签查询", "my_tags"),


script_callbacks.on_ui_tabs(on_ui_tabs)
