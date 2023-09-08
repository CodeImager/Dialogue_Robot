import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import RobotFunction as RF

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI() #主窗口
        self.Welcome_message() #欢迎语句
        self.sum = '0' #用于判断用户菜单选择 默认'0'代表还未选择使用哪个功能

    def initUI(self):
        #去除顶部栏
        self.setWindowFlag(Qt.FramelessWindowHint)
         
        #去除窗口外边框
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        #实例化盒子
        hbox = QHBoxLayout(self)

        #设置顶部栏
        self.top = QLabel("对话机器人")
        self.top.setFixedHeight(35)
        self.top.setAlignment(Qt.AlignCenter)
        self.top.setStyleSheet("background-color: #4f7da4;color: white;font-size:17px;") 

        #实例化子窗口
        self.topleft = QTextEdit(self)
        self.topleft.setReadOnly(True) #不可写入
        self.bottomleft = QTextEdit(self) #实例化文本框
        self.bottomleft.textChanged.connect(self.Enter_send) #绑定按下回车发送事件
        right = QLabel(self) #实例化标签

        #实例化分割线
        splitter1 = QSplitter(Qt.Vertical) #水平布局
        splitter1.addWidget(self.topleft) #添加topleft进splitter1
        splitter1.addWidget(self.bottomleft) #添加bottomleft进splitter1
        splitter1.setSizes([700,200])

        splitter2 = QSplitter(Qt.Horizontal) #垂直布局
        splitter2.addWidget(splitter1) #添加splitter1进splitter2
        splitter2.addWidget(right) #添加right进splitter2
        splitter2.setSizes([700,200])

        splitter3 = QSplitter(Qt.Vertical) #水平布局
        splitter3.addWidget(self.top) #添加top进splitter3
        splitter3.addWidget(splitter2) #添加splitter2进splitter3
        splitter3.setSizes([700,200])
        
        splitter3.setStyleSheet("border:0px")

        hbox.addWidget(splitter3) #把splitter添加进hbox
        self.setLayout(hbox)

        #加载机器人图片
        pixmap = QPixmap('image/robot.jpg')
        right.setStyleSheet("background-color:rgb(255,255,255)")
        #给right加入机器人图片
        right.setPixmap(pixmap)

        #实例化调色板
        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap('image/bg.jpg')))
        self.setPalette(window_pale)
        
        #添加发送按钮
        btn1=QPushButton('发送(S)',self)
        btn1.move(460,570)
        btn1.clicked.connect(self.sentButton)
        btn1.setStyleSheet("border-radius:3px;background-color: rgb(79, 125, 164);color: rgb(255, 255, 255);")

        #添加关闭按钮
        btn2=QPushButton('关闭(C)',self)
        btn2.move(340,570)
        btn2.clicked.connect(self.close)
        btn2.setStyleSheet("border-radius:3px;background-color: rgb(255, 255, 255);border: 1px solid #cdcfd0;")
        
        # #添加最小化按钮
        btn3=QPushButton('—',self)
        btn3.move(642,17)
        btn3.clicked.connect(self.showMinimized)
        btn3.setFixedSize(20,20)
        btn3.setStyleSheet("border-radius:1px;background-color: rgb(79, 125, 164);color: rgb(255, 255, 255);font-size:15px;")

        # #添加最大化按钮
        btn4=QPushButton('□',self)
        btn4.move(672,17)
        btn4.clicked.connect(self.showMaximized)
        btn4.setFixedSize(20,20)
        btn4.setStyleSheet("border-radius:1px;background-color: rgb(79, 125, 164);color: rgb(255, 255, 255);font-size:14px;")

        #添加右上角关闭按钮
        btn5=QPushButton('×',self)
        btn5.move(702,17)
        btn5.clicked.connect(self.close)
        btn5.setFixedSize(20,20)
        btn5.setStyleSheet("border-radius:1px;background-color: rgb(79, 125, 164);color: rgb(255, 255, 255);font-size:19px;")

        #窗口大小及屏幕坐标
        self.setGeometry(560,200,740,580)
        self.show()
                    

#----------------------------------------- 菜单选择、用户输入、机器人回复 ----------------------------------------- 

    # 获取当前时间函数
    def Current_time(self):
        #实例化定时器
        self.timer=QTimer()
        #获取系统当前时间
        time=QDateTime.currentDateTime()
        #设置时间格式
        timeDisplay=time.toString('hh:mm:ss')
        return timeDisplay
        
    # 初始菜单栏选择提示语
    def Welcome_message(self):
        if self.bottomleft.toPlainText() == "":
            self.Robot_reply(
                                '欢迎使用基于Pyqt5开发的聊天对话机器人，本机器人有以下功能，也可以自由聊天：'+'\n'+
                                '1.天气查询'+'\n'+
                                '2.疫情查询'+'\n'+
                                '3.汇率兑换'+'\n'+
                                '4.讲个笑话'+'\n'+
                                '5.NBA今日东西部排名'+'\n'+
                                '6.脑筋急转弯'+'\n')
        else:
            self.Robot_reply(
                                '1.天气查询'+'\n'+
                                '2.疫情查询'+'\n'+
                                '3.汇率兑换'+'\n'+
                                '4.讲个笑话'+'\n'+
                                '5.NBA今日东西部排名'+'\n'+
                                '6.脑筋急转弯'+'\n')

    # 判断用户菜单选择
    def Menu_selection(self,U_message):
        if U_message == '天气查询':
            self.Robot_reply('请问想要查询哪个城市的天气呢？')
            self.sum = '1'
        elif U_message == '疫情查询':
            self.Robot_reply('请问想要查询哪个省份的情况呢？')
            self.sum = '2'
        elif U_message == '汇率兑换':
            self.Robot_reply('请输入带单位货币的金额： ')
            self.sum = '3'
        elif U_message == '笑话':
            self.Robot_reply(RF.Joke(U_message))
            self.sum = '4'
        elif U_message == '脑筋急转弯':
            self.Robot_reply('准备好后请输入"开始"：')
            self.sum = '5'
        elif U_message == 'NBA':
            self.Robot_reply(RF.NBA_rank())
        elif U_message == '菜单':
            self.Welcome_message()
        else:
            self.Robot_reply(RF.XY(U_message))
        self.bottomleft.clear()
    
    # 用户发送
    def User_send(self,message):
        self.topleft.setText(self.topleft.toPlainText()+'\n'+'\n'+'User\t'+self.Current_time()+'\n'+message+'\n')

    # 机器人回复
    def Robot_reply(self,event):
        self.topleft.setText(self.topleft.toPlainText()+'\n'+'\n'+'Robot\t'+self.Current_time()+'\n'+event)

#----------------------------------------- 按钮事件和其他事件 ----------------------------------------- 
    
    # 发送按钮事件
    def sentButton(self):
        U_message = self.bottomleft.toPlainText()
        self.User_send(U_message)
        if self.sum == '0':
            self.Menu_selection(U_message)
        elif self.sum == '1':
            self.Robot_reply(RF.act_weater(U_message))
            self.sum = '0'
        elif self.sum == '2':
            self.Robot_reply(RF.province_check(U_message))
            self.sum = '0'
        elif self.sum == '3':
            self.Robot_reply(RF.Get_huilv(U_message))
            self.sum = '0'
        elif self.sum == '4':
            if RF.Joke(U_message) == '0':
                self.Robot_reply('笑话已结束，如果想听笑话请输入“笑话”就可以了')
                self.sum = '0'
            else:
                self.Robot_reply(RF.Joke(U_message))    
        elif self.sum == '5':
            if RF.Brain_twists(U_message) == '0':
                self.Robot_reply('脑筋急转弯已结束，如果想再玩请输入“脑筋急转弯”就可以了')
                self.sum = '0'
            else:
                self.Robot_reply(RF.Brain_twists(U_message))
        else:
            self.Robot_reply(RF.XY(U_message))
            self.sum = '0'
        self.bottomleft.clear()
        self.topleft.moveCursor(QTextCursor.End) # topleft的滚动条置底
        
    # 按下回车发送
    def Enter_send(self):
        msg = self.bottomleft.toPlainText()
        if '\n' in msg:     
            msg = msg.replace('\n','')  #将文本框中的\n删除
            self.bottomleft.setText(msg)  #将处理后的内容重新放入文本框
            self.sentButton()   #执行发送按钮

    #Esc键程序退出
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    # 定义一个关闭事件，若输入框还有文字未发送进行提示
    def closeEvent(self, event):
        if self.bottomleft.toPlainText() != "":
            #消息盒子的信息
            reply = QMessageBox.question(self, '提示',
                "输入框内有文字未发送，是否关闭？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore() 
        elif self.bottomleft.toPlainText() == "":
            self.close() 

if __name__=='__main__':
    #创建一个应用
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
