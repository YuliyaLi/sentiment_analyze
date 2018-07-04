
import tkinter as tk
from tkinter import *
import random
from sentiment_token_grg import Score
import jieba
from PIL import Image, ImageTk


def main(text):
    sentiment_dict_path = "./sentiment_words_chinese.tsv"  #/sentiment_words_chinese.tsv
    degree_dict_path = "./degree_dict.txt"
    stop_dict_path = "./stop_words.txt"
    score = Score(sentiment_dict_path, degree_dict_path, stop_dict_path )
    # 分句功能， 否定词程度词位置判断，
    text = [text]
    for temp in text:
        words = [x for x in jieba.cut(temp)]
        print(words)
        words_ = score.remove_stopword(words)
        result = score.get2score_position(words_)
    return result


class Guidemo(object):
    def __init__(self):
        self.result = 0.0
        window = tk.Tk()

        window.title("情感分析")
        self.canvas = Canvas(window, height=400, width=400)
        self.canvas.pack()
        # 利用画布的create_arc画饼形，(400,400)和(100,100)为饼形外围的矩形,
        # start=角度起始，extent=旋转的度数，fill=填充的颜色
        master = Frame(window)
        master.pack()
        var = tk.IntVar()
        row_num = 0

        url_tv_column_span = 100
        all_direction = tk.E + tk.N + tk.W + tk.S

        global inputtext_tv, score_tv
        inputtext_tv = tk.StringVar()
        score_tv = tk.DoubleVar()

        #tk.Label(master, text="请输入文本内容：", bg="white", font=("Arial", 12), width=20, height=2 ).grid(sticky=E)
        tk.Label(master, text="请输入文本内容：", bg="white", font=("Arial", 12)).grid(padx=10, pady=10, row=0, column=0, sticky=all_direction) #提示
        e1 = tk.Entry(master, textvariable=inputtext_tv).grid(padx=10, pady=10, row=0, column=3, columnspan=url_tv_column_span , sticky=all_direction ) #文本输入框
        button1 = Button(master, text='分析', command=self.analyse_button_event).grid(padx=0, pady=5, row=0, column=4, sticky=E) # 按钮
        #inputtext = inputtext_tv.get()
        #e1.set('input your text here')
        tk.Label(master, text="情 感 分 数 是：", bg="white", font=("Arial", 12)).grid( padx=10, pady=10, row=1, column=0, sticky=E)
        e2 = tk.Entry(master, textvariable=score_tv).grid(padx=10, pady=10, row=1, column=3, sticky=E)
        window.mainloop()
        #mainloop()

    def analyse_button_event(self):
        #prompt_text.set("正在爬取评论，请稍等......")
        #t = Thread(target=get_result)
        #t.start()
        inputtext = inputtext_tv.get()
        try:
            self.result = main(inputtext)
            score_tv.set(self.result)
            self.draw_piechart()
        except ValueError:
            inputtext_tv.set("请输入有效的中文文本...")

    def draw_piechart(self):
        #
        # 将分数转换为度数
        neg = -40
        pos = 40

        if self.result == 0:
            neg_extent = 180
            pos_extent = 180
            neg_per = pos_per = 50
        elif self.result>0:
            pos_per = self.result/pos *100 +50
            neg_per = 100 - pos_per

        else:
            neg_per = abs(self.result)/abs(neg) *100 +50
            pos_per = 100 - neg_per

        neg_extent = neg_per * 360.0/100
        pos_extent = pos_per * 360.0/100


        # (左上角坐标, 右上角坐标)start为开始的度数，extent为要转的度数.全部以逆时针为正方向，0为x轴正方向
        self.canvas.create_arc(50, 50, 350, 350, start=0, extent= neg_extent, fill="yellow")
        #self.canvas.create_arc(400, 400, 100, 100, start=36, extent=72, fill="green")
        self.canvas.create_arc(50, 50, 350, 350, start=neg_extent, extent=pos_extent, fill="green")
        #self.canvas.create_arc(400, 400, 100, 100, start=216, extent=144, fill="blue")
        # 为各个扇形添加内容，圆心为（250，250）
        self.canvas.create_text(200, 100, text= '负面情绪：'+ str(neg_per), font=("华文新魏", 20))
        #self.canvas.create_text(330, 100, text="72°", font=("华文新魏", 20))
        self.canvas.create_text(200, 300, text= '正面情绪：'+ str(pos_per), font=("华文新魏", 20))
        #self.canvas.create_text(390, 370, text="144°", font=("华文新魏", 20))


        image = Image.open("img.jpg")
        im = ImageTk.PhotoImage(image)

        canvas.create_image(300, 50, image=im)  # 使用create_image将图片添加到Canvas组件中

##https://www.cnblogs.com/libra-yong/p/6250183.html
if __name__ == '__main__':
    #main()
    guidemo = Guidemo()