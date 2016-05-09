import json
import requests
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.createWidgets()

    def createWidgets(self):
        grid_options = dict(sticky=tk.N+tk.E+tk.W, padx=3, pady=4)
        self.url_label = tk.Label(self, text="URL")
        self.url_label.grid(row=0, column=0, **grid_options)

        self.url = tk.Text(self, height=1)
        self.url.grid(row=0, column=1, **grid_options)
        self.url.insert(tk.INSERT, "http://")

        self.send_button = tk.Button(self)
        self.send_button["text"] = "Send Request"
        self.send_button["command"] = self.send_request
        self.send_button.grid(row=0, column=2, **grid_options)

        self.content_label = tk.Label(self, text="Request content")
        self.content_label.grid(row=1, column=0, **grid_options)

        self.content = tk.Text(self, height=10)
        self.content.grid(row=1, column=1, **grid_options)

        self.method_var = tk.StringVar()
        self.method_var.set("GET")
        self.method_frame = tk.Frame(self)
        self.method_frame.grid(row=1, column=2, **grid_options)

        for index, method in enumerate(["GET", "POST", "PUT", "DELETE"]):
            r = tk.Radiobutton(self.method_frame,
                               variable=self.method_var,
                               text=method,
                               value=method)
            r.grid(row=index, sticky=tk.W)

        self.output_label = tk.Label(self, text="Response output")
        self.output_label.grid(row=2, column=0, **grid_options)

        self.output = tk.Text(self, height=10)
        #self.output.config(state=tk.DISABLED)
        self.output.grid(row=2, column=1, sticky=tk.N+tk.S+tk.E+tk.W, padx=3, pady=4)

    def send_request(self):
        method = self.method_var.get().upper()
        url = self.url.get(1.0, tk.END)
        content = self.content.get(1.0, tk.END).strip()
        payload = {}
        if len(content) > 0:
            try:
                payload = json.loads(content)
            except Exception as e:
                self.output.delete(1.0, tk.END)
                self.output.insert(tk.INSERT, "Failed to parse request content")
                return
        if method == "GET":
            r = requests.get(url)
        elif method == "POST":
            r = requests.post(url, data=payload)
        elif method == "PUT":
            r = requests.put(url, data=payload)
        elif method == "DELETE":
            r = requests.delete(url)
        else:
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.INSERT, "Unknown request method selected")
            return

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, r.text)

root = tk.Tk()
root.wm_title("HTTP Request Client")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
app = Application(master=root)
app.mainloop()
