from platform import system
from tkinter import HORIZONTAL, Tk, Toplevel, END
from tkinter import messagebox, filedialog
from tkinter import Checkbutton, Button, scrolledtext, OptionMenu, Text
from tkinter import Label, font, BooleanVar, DoubleVar, Scale
from huoZiYinShua import *
from multiprocessing import Process, freeze_support
from PIL import ImageTk, Image
import json


#新建活字印刷类实例
HZYS = huoZiYinShua("./settings.json")
#播放音频的进程
myProcess = Process()



#主框架
#-------------------------------------------
mainWindow = Tk()



#动作
#-------------------------------------------
#直接播放的监听事件
def onDirectPlay():
	global myProcess
	#停止播放按钮上次点击时播放的音频
	try:
		myProcess.terminate()
	except:
		pass
	#播放
	textToRead = textArea.get(1.0, 'end')
	myProcess = Process(target=HZYS.directPlay,
						kwargs={"rawData": textToRead,
								"inYsddMode": inYsddMode.get(),
								"pitchMult": pitchMultOption.get(),
								"speedMult": speedMultOption.get(),
								"norm": normAudio.get(),
								"reverse": reverseAudio.get()})
	myProcess.start()


#导出的监听事件
def onExport():
	textToRead = textArea.get(1.0, 'end')
	outputFile = filedialog.asksaveasfilename(title="选择导出路径",filetypes = (("wav音频文件", "*.wav"),))
	
	if(outputFile != ""):
		if not outputFile.endswith(".wav"):
			outputFile += ".wav"
		HZYS.export(textToRead,
					filePath=outputFile,
					inYsddMode=inYsddMode.get(),
					pitchMult=pitchMultOption.get(),
					speedMult=speedMultOption.get(),
					norm=normAudio.get(),
					reverse=reverseAudio.get())
		messagebox.showinfo("疑似是成功了", "已导出到" + outputFile +"下")


#读取设定文件
def readConfig():
	#若./settings.json存在
	try:
		configFile = open("./settings.json", "r", encoding="utf8")
		configuration = json.load(configFile)
		configFile.close()
		return configuration
	#若不存在
	except:
		configuration = {
			"sourceDirectory": "",
			"ysddSourceDirectory": "",
			"dictFile": "",
			"ysddTableFile": ""
		}
		return configuration


#更改设定
def setConfig(option, texts, configWindow):
	#读取当前设定
	configuration = readConfig()
	userConfig = ""
	#让用户选择文件或目录
	if (option == "sourceDirectory" or option == "ysddSourceDirectory"):
		directory_path = filedialog.askdirectory(parent=configWindow, title="选择文件夹")
		if directory_path:
			userConfig = directory_path + "/"
		else:
			return
	elif (option == "dictFile" or option == "ysddTableFile"):
		file_path = filedialog.askopenfilename(parent=configWindow, title="选择文件",filetypes = (("json配置文件", "*.json"),))
		if file_path:
			userConfig = file_path
		else:
			return
	#写入
	configuration[option] = userConfig
	configFile = open("./settings.json", "w", encoding="utf8")
	json.dump(configuration, configFile, ensure_ascii=False, indent="\t")
	configFile.close()
	#更新配置窗口
	optionArray = ["sourceDirectory", "ysddSourceDirectory", "dictFile", "ysddTableFile"]
	texts[optionArray.index(option)].configure(text=configuration[option])
	#更新活字印刷实例配置
	global HZYS
	HZYS = huoZiYinShua("./settings.json")



#创建设定窗口
def createConfigWindow():
	#窗口属性
	configWindow = Toplevel(mainWindow)
	configWindow.geometry("500x480")
	configWindow.title("设定")
	configWindow.resizable(True, False)
	try:
		img = ImageTk.PhotoImage(Image.open("./didu.ico"))
		configWindow.tk.call('wm', 'iconphoto', configWindow._w, img)
	except:
		messagebox.showwarning("警告", "缺失图标")

	mainWindow.attributes('-disabled', True)
	configWindow.protocol("WM_DELETE_WINDOW",
				lambda: [configWindow.destroy(), mainWindow.attributes('-disabled', False), mainWindow.lift()])
		
	#读取设置
	configuration = readConfig()

	#文字
	text1_1 = Label(configWindow, text="活字印刷单字音频存放文件夹：",
					font=font.Font(family="微软雅黑", size=14))
	text1_2 = Label(configWindow, text=configuration["sourceDirectory"],
					font=font.Font(family="微软雅黑", size=14))
	text2_1 = Label(configWindow, text="活字印刷原声大碟音频存放文件夹：",
					font=font.Font(family="微软雅黑", size=14))
	text2_2 = Label(configWindow, text=configuration["ysddSourceDirectory"],
					font=font.Font(family="微软雅黑", size=14))
	text3_1 = Label(configWindow, text="非中文字符读法字典文件：",
					font=font.Font(family="微软雅黑", size=14))
	text3_2 = Label(configWindow, text=configuration["dictFile"],
					font=font.Font(family="微软雅黑", size=14))
	text4_1 = Label(configWindow, text="原声大碟关键词与音频对照表：",
					font=font.Font(family="微软雅黑", size=14))
	text4_2 = Label(configWindow, text=configuration["ysddTableFile"],
					font=font.Font(family="微软雅黑", size=14))
	texts = [text1_2, text2_2, text3_2, text4_2]

	#按钮
	configButton1 = Button(configWindow, text="选择目录", command=lambda: setConfig("sourceDirectory", texts, configWindow),
					height=1, width=8, font=font.Font(family="微软雅黑", size=14))
	configButton2 = Button(configWindow, text="选择目录", command=lambda: setConfig("ysddSourceDirectory", texts, configWindow),
					height=1, width=8, font=font.Font(family="微软雅黑", size=14))
	configButton3 = Button(configWindow, text="选择文件", command=lambda: setConfig("dictFile", texts, configWindow),
					height=1, width=8, font=font.Font(family="微软雅黑", size=14))
	configButton4 = Button(configWindow, text="选择文件", command=lambda: setConfig("ysddTableFile", texts, configWindow),
					height=1, width=8, font=font.Font(family="微软雅黑", size=14))

	#位置
	text1_1.place(x=5, y=0)
	text1_2.place(x=5, y=30)
	text2_1.place(x=5, y=120)
	text2_2.place(x=5, y=150)
	text3_1.place(x=5, y=240)
	text3_2.place(x=5, y=270)
	text4_1.place(x=5, y=360)
	text4_2.place(x=5, y=390)
	configButton1.place(x=5, y=60)
	configButton2.place(x=5, y=180)
	configButton3.place(x=5, y=300)
	configButton4.place(x=5, y=420)



#创建原声大碟一览窗口
def createYsddWindow():
	#窗口属性
	ysddWindow = Toplevel(mainWindow)
	ysddWindow.geometry("480x480")
	ysddWindow.title("原声大碟文本一览")
	ysddWindow.minsize(width=480,height=480)
	ysddWindow.resizable(True, True)
	try:
		img = ImageTk.PhotoImage(Image.open("./didu.ico"))
		ysddWindow.tk.call('wm', 'iconphoto', ysddWindow._w, img)
	except:
		messagebox.showwarning("警告", "缺失图标")


	ysddList = scrolledtext.ScrolledText(ysddWindow,width=40, height=8,
					font=font.Font(family="微软雅黑", size=16))
	
	#读取设置
	configuration = readConfig()
	with open(configuration["ysddTableFile"], encoding="utf8") as ysddTableFile:
		ysddTable = json.load(ysddTableFile)

	ysddKey = '\n'.join(ysddTable.keys())
	ysddList.insert(END,ysddKey)
	ysddList.config(state='disable')
	

	#位置
	ysddList.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
	ysddWindow.grid_columnconfigure(0,weight=1)
	ysddWindow.grid_rowconfigure(0,weight=1)

	



#储存生成选项的变量
#-------------------------------------------
inYsddMode = BooleanVar()
normAudio = BooleanVar()
reverseAudio = BooleanVar()
pitchMultOption = DoubleVar()
speedMultOption = DoubleVar()



#GUI元素
#-------------------------------------------
#文本框
textArea = scrolledtext.ScrolledText(mainWindow, width=50, height=8,
					font=font.Font(family="微软雅黑", size=16))


#按钮们
#播放按钮
playButton = Button(mainWindow, text="直接播放", command=onDirectPlay, height=1, width=9,
					font=font.Font(family="微软雅黑", size=14))


#导出按钮
exportButton = Button(mainWindow, text="导出", command=onExport, height=1, width=9,
					font=font.Font(family="微软雅黑", size=14))


#原声大碟一览按钮
ysddChekButton = Button(mainWindow, text="原声大碟一览", command=createYsddWindow, height=1, width=9,
					font=font.Font(family="微软雅黑", size=14))

#设置按钮
configButton = Button(mainWindow, text="设置", command=createConfigWindow, height=1, width=9,
					font=font.Font(family="微软雅黑", size=14))


#原声大碟复选框
ysddCkBt = Checkbutton(mainWindow, text="匹配到特定文字时使用原声大碟",
						variable=inYsddMode, onvalue=True, offvalue=False,
                       font=font.Font(family="微软雅黑", size=14))


#标准化音频复选框
normCkBt = Checkbutton(mainWindow, text="统一每个字和每条原声大碟句子的音量",
						variable=normAudio, onvalue=True, offvalue=False,
						font=font.Font(family="微软雅黑", size=14))


#倒放音频复选框
reverseCkBt = Checkbutton(mainWindow, text="频音的成生放倒",
						variable=reverseAudio, onvalue=True, offvalue=False,
						font=font.Font(family="微软雅黑", size=14))


#音调偏移文本
pitchMultLabel = Label(mainWindow, text="音调偏移：",
						font=font.Font(family="微软雅黑", size=14))


#音调偏移滑块
pitchMultScale = Scale(mainWindow, from_=0.5, to=2.0, orient=HORIZONTAL, width=18, length=300,
						resolution=0.1, variable=pitchMultOption,
						font=font.Font(family="微软雅黑", size=14))


#播放速度文本
speedMultLable = Label(mainWindow, text="播放速度：",
						font=font.Font(family="微软雅黑", size=14))


#播放速度滑块
speedMultScale = Scale(mainWindow, from_=0.5, to=2.0, orient=HORIZONTAL, width=18, length=300,
						resolution=0.1, variable=speedMultOption,
						font=font.Font(family="微软雅黑", size=14))


#原作者声明文本
originalDeveloperLable = Label(mainWindow, text="\n程序原作者：DSP-8192",
						font=font.Font(family="微软雅黑", size=14))


#主函数
#-------------------------------------------
if __name__ == "__main__":
	#multiprocess和Windows的兼容
	freeze_support()
	#匹配DPI
	if (system() == "Windows"):
		from ctypes import windll
		windll.shcore.SetProcessDpiAwareness(1)

	#主窗口
	#-----------------------------
	mainWindow.geometry("600x620")
	mainWindow.title("潮语四散物")
	mainWindow.resizable(False, False)
	
	#窗口图标
	try:
		img = ImageTk.PhotoImage(Image.open("./didu.ico"))
		mainWindow.tk.call('wm', 'iconphoto', mainWindow._w, img)
	except:
		messagebox.showwarning("警告", "缺失图标")

	#元素属性
	#-----------------------------
	textArea.grid(row=0, column=0, columnspan=5, padx=15, pady=10, sticky="nsew")

	playButton.grid(row=1, column=0, padx=12, pady=10, sticky="nsew")
	exportButton.grid(row=1, column=1, padx=12, pady=10, sticky="nsew")
	ysddChekButton.grid(row=1, column=2, padx=12, pady=10, sticky="nsew")
	configButton.grid(row=1, column=3, padx=12, pady=10, sticky="nsew")

	ysddCkBt.grid(row=2, column=0, columnspan=5, padx=10, pady=3, sticky="w")
	normCkBt.grid(row=3, column=0, columnspan=5, padx=10, pady=3, sticky="w")
	reverseCkBt.grid(row=4, column=0, columnspan=5, padx=10, pady=3, sticky="w")

	pitchMultLabel.grid(row=5, column=0, padx=10, pady=5, sticky="sw")
	pitchMultOption.set(1)
	pitchMultScale.grid(row=5, column=1, columnspan=3, sticky="nw")

	speedMultLable.grid(row=6, column=0, padx=10, pady=5, sticky="sw")
	speedMultOption.set(1)
	speedMultScale.grid(row=6, column=1, columnspan=3, sticky="nw")

	originalDeveloperLable.grid(row=7, column=0, columnspan=4, padx=15, sticky="e")


	for i in range(4):
		mainWindow.grid_columnconfigure(i,weight=1)



	#检查活字印刷实例是否配置正确
	if not HZYS.configSucceed():
		messagebox.showwarning("初始化活字印刷实例失败", "请检查设置的文件路径是否正确")
	
	#启动主窗口
	mainWindow.mainloop()

	#退出
	try:
		myProcess.terminate()
	except:
		pass
