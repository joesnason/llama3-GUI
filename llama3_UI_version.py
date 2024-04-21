import tkinter as tk
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler




class LLMStreamingCallback(StreamingStdOutCallbackHandler):
    def __init__(self):
        super().__init__()
        #self.text = ""
    def on_llm_new_token(self, token: str, **kwargs: any):
        #self.text += token
        token= token.replace('\n', '')
        response["text"] = response["text"] + token
        #print(token)
        window.update()


def HelloMsg():
    system_prompt = textbox_systemprompt.get("1.0", tk.END)
    user_prompt = input_textedit.get()
    response["text"] = response["text"] + "\n" + "User: " + user_prompt
    prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),    
    ("user", user_prompt),
])
    chain = prompt | llm  
    context = response["text"] + "\n"  + "AI: " # +  chain.invoke({"user_prompt": user_prompt}) 
    response.config(text=context, anchor="nw")
    chain.invoke({"user_prompt": user_prompt})

window = tk.Tk()
window.title("Tkinter Test")
window.geometry("800x600")

llm = Ollama(model='llama3', callback_manager=CallbackManager([LLMStreamingCallback()]))


title = tk.Label(window, text="Local Llama3  test", font=("Arial", 24), bg="yellow")
title.pack()

textbox_systemprompt = tk.Text(window,  height=5, width=100, font=("Arial", 12))
textbox_systemprompt.insert(tk.END, "你是一個英翻中的專家。請翻譯下列英文句子成繁體中文")
textbox_systemprompt.pack()


#response = tk.Label(window, text="This is a long text that will be displayed from left to right and supports line breaks.", height=20, width=100, wraplength=2000 , font=("Arial", 12), bg="lightblue", anchor=tk.NW)
response = tk.Label(window, text="", height=20, width=100, wraplength=2000 , font=("Arial", 12), bg="lightblue", anchor="nw", justify="left")
response.pack()



input_frame = tk.Frame(window)
input_frame.pack()  

input_textedit = tk.Entry(input_frame, width=90, font=("Arial", 12))
input_textedit.pack(side=tk.LEFT)

btn=tk.Button(input_frame, text="send", command=HelloMsg)
btn.pack(side=tk.LEFT, padx=5)

input_textedit.focus_set()



window.update()

window.mainloop()


