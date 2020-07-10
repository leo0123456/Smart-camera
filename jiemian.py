from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from tkinter import *
import PIL

global path1_, path2_, rate, seg_img_path, path3_
from play_with_dlatent import main

class rongh():
    def startrong(self):
        self.root = Toplevel()
        self.root.title('计算机生成')
        self.root.geometry('700x500')
        # decoration = PIL.Image.open('bgm.png').resize((700, 500))
        # render = ImageTk.PhotoImage(decoration)
        # img = Label(image=render)
        # img.image = render
        # img.place(x=0, y=0)

        Button(self.root, text="选择生成器", command=self.show_original1_pic).place(x=50, y=170)
        # 原图2的展示
        Button(self.root, text="选择latent码", command=self.show_original2_pic).place(x=50, y=210)

        Button(self.root, text="选择模式", command=self.show_original3_pic).place(x=50, y=250)
        # 进行提取结果的展示
        Button(self.root, text="计算机生成", command=self.show_morpher_pic).place(x=50, y=300)
        Button(self.root, text="图片生成", command=self.omd).place(x=50, y=350)

        Button(self.root, text="退出软件", command=quit).place(x=600, y=40)

        Label(self.root, text="调整幅度", font=10).place(x=50, y=10)
        self.entry = Entry(self.root)
        self.entry.place(x=130, y=10)



        Label(self.root, text="计算机生成", font=10).place(x=420, y=120)
        self.cv_seg = Canvas(self.root, bg='white', width=270, height=270)
        self.cv_seg.create_rectangle(8, 8, 260, 260, width=1, outline='red')
        self.cv_seg.place(x=420, y=150)
        self.label_Img_seg = Label(self.root)
        self.label_Img_seg.place(x=420, y=150)
        self.root.mainloop()

    # 原图1展示
    def show_original1_pic(self):
        global path1_
        path1_ = askopenfilename(title='选择文件')
        print(path1_)


    # 原图2展示
    def show_original2_pic(self):
        global path2_
        path2_ = askopenfilename(title='选择文件')
        print(path2_)

    def show_original3_pic(self):
        global path3_
        path3_ = askopenfilename(title='选择文件')
        print(path3_)

    # 计算机合成效果展示
    def show_morpher_pic(self):

        main(path1_,path2_,path3_,int(self.entry.get()))
    def omd(self):
        a = "./results/000.png"
        Img = PIL.Image.open(r'{}'.format(a))
        Img = Img.resize((270, 270), PIL.Image.ANTIALIAS)  # 调整图片大小至256x256
        img_png_seg = ImageTk.PhotoImage(Img)
        self.label_Img_seg.config(image=img_png_seg)
        self.label_Img_seg.image = img_png_seg  # keep a reference

    def quit(self):
        self.root.destroy()

# mdo = rong()
# mdo.startrong()









