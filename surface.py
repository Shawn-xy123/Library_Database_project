import sys
from userface import Ui_Form
from signin import  Ui_Form1
from PyQt4.QtGui  import *
from PyQt4.QtCore import *

import tkinter.messagebox
from tkinter import *

import pymysql

# class MainWindow(QtGui.QWidget):
#     def __init__(self, parent=None):
#         QtGui.QWidget.__init__(self, parent)
#         self.ui = Ui_Form()
#         self.ui.setupUi(self)
#
def link_db(h,p,u,w,d):
    # conn = pymysql.connect(host='202.38.88.99',
    #                        port=1434,
    #                        user='student',
    #                        password='student',
    #                        db="student",
    #                        charset ='utf8')
    # conn = pymysql.connect(host='localhost',
    #                        port=3306,
    #                        user='root',
    #                        password='security',
    #                        db="test",
    #                        charset='utf8')
    conn = pymysql.connect(host=h,
                           port=p,
                           user=u,
                           password=w,
                           db=d,
                           charset='utf8')

    return conn

#默认连接
conn = link_db('localhost',3306,'root','security','test')
#conn = link_db('localhost',3306,'root','security','test')
cur = conn.cursor()
        #处理更新

#初始化
host=''
db=''
port=0
user=''
password=''
class MainWindow(QWidget,Ui_Form):
    #定义当前行,列
    currentrow=0
    currentcolumn=0
    #mode用来确认确定键时时修改还是增加1为增加，-1为修改ll
    mode=0
    #为修改记录数据
    title=''
    author=''
    title_id=''
    price=''
    press=''
    publish_time=''
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        #将一部分现在不用的按键无效
        self.pushButton_2.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        # 隐藏列表头
        self.tableWidget.verticalHeader().setVisible(False)
        #增加可以为真
        self.pushButton_3.setEnabled(True)
        #创建存储过程也是可以的
        self.pushButton_5.setEnabled(True)
        #清除内容也是可以的
        self.pushButton_6.setEnabled(True)
        self.pushButton_7.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        #执行存储过程也是可以的
        self.pushButton_9.setEnabled(True)

        #使表格无法编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.lineEdit.setPlaceholderText('请输入关键词')
        self.pushButton.clicked.connect(self.pushB_check_Clicked)
        self.pushButton_2.clicked.connect(self.pushB_delete_Clicked)
        self.pushButton_3.clicked.connect(self.pushB_add_Clicked)
        self.pushButton_4.clicked.connect(self.pushB_change_Clicked)
        self.pushButton_7.clicked.connect(self.pushB_assure_Clicked)
        self.pushButton_8.clicked.connect(self.pushB_cancel_Clicked)
        self.pushButton_5.clicked.connect(self.pushB_create_Clicked)
        self.pushButton_9.clicked.connect(self.pushB_excute_Clicked)
        self.pushButton_6.clicked.connect(self.pushB_clear_Clicked)


    #查询定义函数
    def pushB_check_Clicked(self):
        #读取选择的模式和关键词构造sql语句
        method = self.comboBox.currentText()
        if method=='查询所有':
            sql = "SELECT * FROM  xybook;"
        else:
            info = self.lineEdit.text()  # 读取输入的信息不能为空
            if info=='':
                # #清除表中已有数据
                self.tableWidget.clearContents()
                root1 = Tk()
                root1.withdraw()  # 隐藏主窗口
                tkinter.messagebox.showinfo(title='提示', message='请输入关键词')
                return 0
            if method=='任意词查询':
                sql = "SELECT * FROM xybook WHERE author like '%%%s%%' or title like '%%%s%%' or author like '%%%s%%' or price  like '%%%s%%' or press like '%%%s%%' or title_id like '%%%s%%' or publish_time like '%%%s%%'" % (
                info, info, info, info, info, info, info)

            elif method=='作者查询':
                sql = "SELECT * FROM xybook WHERE author like '%%%s%%'" % info
            elif method=="书名查询":
                sql = "SELECT * FROM xybook WHERE title like '%%%s%%'" % info

        #清除掉文本
        #self.lineEdit.clear()
        # 执行sql语句
        cur.execute(sql)
        data = cur.fetchall()
        rows=len(data)

        #自适应调整列宽度
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        #行不为0，则不是数据不为空
        if rows!=0:
            #隐藏表头的数字
            self.tableWidget.verticalHeader().setVisible(False)
            columns=len(data[0])
            self.tableWidget.setRowCount(rows)
            self.tableWidget.setColumnCount(columns+1)
            #使增删改按键有效
            self.pushButton_2.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            #将数据打印到相应的行列上
            for i in range(0,rows):
                item = QTableWidgetItem(str(i+1))
                self.tableWidget.setItem(i,0, item)
                for j in range(0,columns):
                    item=QTableWidgetItem(str(data[i][j]))
                    self.tableWidget.setItem(i,j+1,item)
        #未读取到任何数据
        else:
            # #清除表中已有数据
            self.tableWidget.clearContents()
            #使增删改无效
            self.pushButton_2.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            #将表格设置为0行0列
            # self.tableWidget.setRowCount(0)
            # self.tableWidget.setColumnCount(0)
            root = Tk()
            root.withdraw()  # 隐藏主窗口
            tkinter.messagebox.showinfo(title='提示', message='未查找到任何相关数据')

    #定义删除后的调序函数,输入参数是要删除的行
    def fixorder(self,row):
        totalrow=self.tableWidget.rowCount()
        for i in range(row,totalrow):
            item = QTableWidgetItem(str(i))
            self.tableWidget.setItem(i, 0, item)
        print('okfix')

    #定义删除
    def pushB_delete_Clicked(self):
        #获得本行本列
        self.currentrow = self.tableWidget.currentRow()
        print(self.currentrow)
        #若没有选中任何行提示
        if (self.currentrow==-1):
            root2 = Tk()
            root2.withdraw()
            tkinter.messagebox.showinfo(title='提示', message='请选择要删除的行')
            return 0
        currentcolumn=self.tableWidget.currentColumn()
        # self.tableWidget.removeRow(currentrow)
        # print(currentrow)  # 获取当前选中的列
        # print(currentcolumn)  # 获取当前选中的行


        #若是选中某行的第0列即选中的是序号 则直接删除本行的数据即可
        if currentcolumn==0:
            sql="delete from xybook where  title like '%s' and author like '%s' and  title_id like '%s' and price  like '%s' and press like '%s'  and publish_time like '%s'" % (
            self.tableWidget.item(self.currentrow,1).text(), self.tableWidget.item(self.currentrow,2).text(), self.tableWidget.item(self.currentrow,3).text(),
            self.tableWidget.item(self.currentrow,4).text(), self.tableWidget.item(self.currentrow,5).text(), self.tableWidget.item(self.currentrow,6).text())
            cur.execute(sql)
            self.fixorder(self.currentrow)
            self.tableWidget.removeRow(self.currentrow)

        #选中的是第一列
        elif currentcolumn==1:
            #删除数据库中相同的数据
            content=self.tableWidget.item(self.currentrow,1).text()#要删除的数据
            sql = "delete from xybook where  title like '%s'"%(content)
            cur.execute(sql)
            #删除那些与之相同在表中的数据
            totalrow=self.tableWidget.rowCount()
            j=0
            for i in range(0,totalrow):
                if (self.tableWidget.item(j,1).text())==content:
                    self.fixorder(j)
                    self.tableWidget.removeRow(j)
                else:
                    j=j+1
        #选中的是第二列
        elif currentcolumn == 2:
            # 删除数据库中相同的数据
            content = self.tableWidget.item(self.currentrow, 2).text()  # 要删除的数据
            sql = "delete from xybook where  author like '%s'" % (content)
            cur.execute(sql)
            # 删除那些与之相同在表中的数据
            totalrow = self.tableWidget.rowCount()
            j = 0
            for i in range(0, totalrow):
                if (self.tableWidget.item(j, 2).text()) == content:
                    self.fixorder(j)
                    self.tableWidget.removeRow(j)
                else:
                    j = j + 1
        #第三列的话
        elif currentcolumn== 3:
            # 删除数据库中相同的数据
            content = self.tableWidget.item(self.currentrow, 3).text()  # 要删除的数据
            sql = "delete from xybook where  title_id like '%s'" % (content)
            cur.execute(sql)
            # 删除那些与之相同在表中的数据
            totalrow = self.tableWidget.rowCount()
            #用j来控制删除的位置
            j = 0
            for i in range(0, totalrow):
                if (self.tableWidget.item(j, 3).text()) == content:
                    self.fixorder(j)
                    print(j)
                    self.tableWidget.removeRow(j)
                else:
                    j = j + 1


        # 第四列的话
        elif currentcolumn == 4:
            # 删除数据库中相同的数据
            content = self.tableWidget.item(self.currentrow, 4).text()  # 要删除的数据
            print(content)
            sql = "delete from xybook where  price like '%s'" % (content)
            cur.execute(sql)
            # 删除那些与之相同在表中的数据
            totalrow = self.tableWidget.rowCount()
            j = 0
            for i in range(0, totalrow):
                if (self.tableWidget.item(j, 4).text()) == content:
                    self.fixorder(j)
                    self.tableWidget.removeRow(j)
                else:
                    j = j + 1
        # 第五列的话
        elif currentcolumn== 5:
            # 删除数据库中相同的数据
            content = self.tableWidget.item(self.currentrow, 5).text()  # 要删除的数据
            sql = "delete from xybook where  press like '%s'" % (content)
            cur.execute(sql)
            # 删除那些与之相同在表中的数据
            totalrow = self.tableWidget.rowCount()
            j = 0
            for i in range(0, totalrow):
                if (self.tableWidget.item(j, 5).text()) == content:
                    self.fixorder(j)
                    self.tableWidget.removeRow(j)
                else:
                    j = j + 1
        # 第六列的话
        elif currentcolumn== 6:
            # 删除数据库中相同的数据
            content = self.tableWidget.item(self.currentrow, 6).text()  # 要删除的数据
            sql = "delete from xybook where  publish_time like '%s'" % (content)
            cur.execute(sql)
            # 删除那些与之相同在表中的数据
            totalrow = self.tableWidget.rowCount()
            j = 0
            for i in range(0, totalrow):
                if (self.tableWidget.item(j,6).text()) == content:
                    self.fixorder(j)
                    self.tableWidget.removeRow(j)
                else:
                    j = j + 1
        #当删除到没有的时候使增删改无效
        if self.tableWidget.rowCount()==0:
            # 将一部分现在不用的按键无效
            self.pushButton_2.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_3.setEnabled(False)

    #调整插入后的序号
    def add_fix_order(self,row):
        totalrow = self.tableWidget.rowCount()
        for i in range(row, totalrow):
            item = QTableWidgetItem(str(i+1))
            self.tableWidget.setItem(i, 0, item)

    #定义增加函数
    def pushB_add_Clicked(self):
        self.pushButton_2.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_7.setEnabled(True)
        self.pushButton_8.setEnabled(True)
        self.mode=1
        self.currentrow=self.tableWidget.currentRow()#获取当前选中的行
        #若没有选中时,默认为0
        if (self.currentrow==-1):
            self.currentrow=0
        #插入一行
        self.tableWidget.insertRow(self.currentrow)
        #全部初始化为0
        # item = QTableWidgetItem(str(''))
        # for i in range(1, 7):
        #     self.tableWidget.setItem(self.currentrow, i, item)
        #调整序号
        self.add_fix_order(self.currentrow)
        #设置双击时触发编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)

        # self.tableWidget.setItemDelegateForColumn(2, EmptyDelegate(self))
        #要设置其他行不可编辑只有该行可以编辑
        # item1 = QTableWidgetItem()
        # item1.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        # rows=self.tableWidget.rowCount()
        # for i in range(0,rows):
        #     if i!=self.currentrow:
        #         for j in range(0,7):
        #             self.tableWidget.setItem(i, j,item1)
        #     else:
        #        # QTableWidgetItem(self.tableWidget.item(i, 0)).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        #         self.tableWidget.setItem(i,0, item1)#设置序号不可编辑


        # item2 = QTableWidgetItem()
        # item2.setFlags(Qt.ItemFlag(63))
        # print(self.currentrow)
        # item1= QTableWidgetItem()
        # item1.setFlags(Qt.ItemFlag(63))
        # print('ok')
        # self.tableWidget.setItem(self.currentrow, 1, item1)
    #定义修改函数
    def pushB_change_Clicked(self):
        self.pushButton_2.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_7.setEnabled(True)
        self.pushButton_8.setEnabled(True)
        self.mode = -1
        self.currentrow= self.tableWidget.currentRow()  # 获取当前选中的行
        if self.currentrow==-1:
            #把按钮重置
            self.pushButton_2.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.pushButton_7.setEnabled(False)
            self.pushButton_8.setEnabled(False)
            root6= Tk()
            root6.withdraw()  # 隐藏主窗口
            tkinter.messagebox.showinfo(title='提示', message='请选择要修改的内容')
            return 0
        #获取当前列
        self.currentcolumn=self.tableWidget.currentColumn()
        #若为序号则无法修改
        if self.currentcolumn==0:
            # 把按钮重置
            self.pushButton_2.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.pushButton_7.setEnabled(False)
            self.pushButton_8.setEnabled(False)
            root8 = Tk()
            root8.withdraw()  # 隐藏主窗口
            tkinter.messagebox.showinfo(title='提示', message='无法修改序号列')
            return 0

        # 获取原来数据
        self.title = self.tableWidget.item(self.currentrow, 1).text()
        self.author = self.tableWidget.item(self.currentrow, 2).text()
        self.title_id = self.tableWidget.item(self.currentrow, 3).text()
        self.price = self.tableWidget.item(self.currentrow, 4).text()
        self.press = self.tableWidget.item(self.currentrow, 5).text()
        self.publish_time = self.tableWidget.item(self.currentrow, 6).text()
        # 设置双击时触发编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        #则只让一个单元格可修改

    # self.tableWidget.setItemDelegateForColumn(2, EmptyDelegate(self))
    # 要设置其他行不可编辑只有该行可以编辑
    # item1 = QTableWidgetItem()
    # item1.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
    # rows=self.tableWidget.rowCount()
    #
    # for i in range(0,rows):
    #     if i!=currentrow:
    #         for j in range(0,7):
    #             self.tableWidget.setItem(i, j,item1)
    # else:
    # QTableWidgetItem(self.tableWidget.item(i, 0)).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    # self.tableWidget.setItem(i,0, item1)#设置序号不可编辑
    def pushB_assure_Clicked(self):

        
        #是增加模式
        if self.mode==1:
            #提取数据
            try:
                title=self.tableWidget.item(self.currentrow,1).text()
                author=self.tableWidget.item(self.currentrow,2).text()
                title_id = self.tableWidget.item(self.currentrow,3).text()
                price = self.tableWidget.item(self.currentrow, 4).text()
                press = self.tableWidget.item(self.currentrow, 5).text()
                publish_time = self.tableWidget.item(self.currentrow, 6).text()
            # 若有数据是空的
            except Exception as err:
                root13 = Tk()
                root13.withdraw()  # 隐藏主窗口
                tkinter.messagebox.showinfo(title='提示', message='请将数据补充完整')
                return 0



            # if title=='' or author=='' or title_id=='' or price=='' or press=='' or publish_time=='':
            # 插入数据库中
            try:
                sql = "insert into xybook values('%s','%s','%s','%s','%s','%s')"% (title,author,title_id,price,press,publish_time)
                cur.execute(sql)

            except Exception as err:
                root4 = Tk()
                root4.withdraw()  # 隐藏主窗口
                tkinter.messagebox.showinfo(title='提示', message='新增数据失败!')
                return 0

            # 使表格无法编辑
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.pushButton_2.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            self.pushButton_7.setEnabled(False)
            self.pushButton_8.setEnabled(False)
            self.mode=0
        #是修改模式
        elif self.mode==-1:
            #提取数据
            try:
                #获取当前修改的内容
                content=self.tableWidget.item(self.currentrow,self.currentcolumn).text()
                #生成sql语句

                if self.currentcolumn == 1:
                    sql = "update xybook  set  title='%s' where  title like '%s' and author like '%s' and  title_id like '%s' and price  like '%s' and press like '%s'  and publish_time like '%s'" % \
                          (content,self.title,self.author,self.title_id,self.price,self.press,self.publish_time)
                    cur.execute(sql)
                elif self.currentcolumn ==2:
                    sql = "update xybook  set  author='%s' where  title like '%s' and author like '%s' and  title_id like '%s' and price  like '%s' and press like '%s'  and publish_time like '%s'" % \
                          (content,self.title,self.author,self.title_id,self.price,self.press,self.publish_time)
                    cur.execute(sql)
                if self.currentcolumn == 3:
                    sql = "update xybook  set  title_id='%s' where  title like '%s' and author like '%s' and  title_id like '%s' and price  like '%s' and press like '%s'  and publish_time like '%s'" % \
                          (content,self.title,self.author,self.title_id,self.price,self.press,self.publish_time)
                    cur.execute(sql)
                if self.currentcolumn == 4:
                    sql = "update xybook  set  price='%s' where  title like '%s' and author like '%s' and  title_id like '%s' and price  like '%s' and press like '%s'  and publish_time like '%s'" % \
                          (content,self.title,self.author,self.title_id,self.price,self.press,self.publish_time)
                    cur.execute(sql)
                if self.currentcolumn == 5:
                    sql = "update xybook  set  press='%s' where  title like '%s' and author like '%s' and  title_id like '%s' and price  like '%s' and press like '%s'  and publish_time like '%s'" % \
                          (content,self.title,self.author,self.title_id,self.price,self.press,self.publish_time)
                    cur.execute(sql)
                if self.currentcolumn == 6:
                    sql = "update xybook  set  publish_time='%s' where  title like '%s' and author like '%s' and  title_id like '%s' and price  like '%s' and press like '%s'  and publish_time like '%s'" % \
                          (content,self.title,self.author,self.title_id,self.price,self.press,self.publish_time)
                    cur.execute(sql)
                # 删除那些与之相同在表中的数据
            except Exception as err:
                root7 = Tk()
                root7.withdraw()  # 隐藏主窗口
                tkinter.messagebox.showinfo(title='提示', message='修改数据失败!')
                return 0

            # 使表格无法编辑
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.pushButton_2.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            self.pushButton_7.setEnabled(False)
            self.pushButton_8.setEnabled(False)
        #状态回归置0
        self.mode=0

    def pushB_cancel_Clicked(self):
        # 控制按钮
        self.pushButton_2.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(True)
        self.pushButton_7.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        #若是增加模式
        if self.mode==1:
            self.mode=0

            #删除该行
            self.fixorder(self.currentrow)
            self.tableWidget.removeRow(self.currentrow)
            # 使表格无法编辑
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        elif self.mode ==-1:
            self.mode = 0
            # 控制按钮
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            # 删除该行
            if self.currentcolumn==1:
                item = QTableWidgetItem(str(self.title))
            elif self.currentcolumn==2:
                item = QTableWidgetItem(str(self.author))
            elif self.currentcolumn == 3:
                item = QTableWidgetItem(str(self.title_id))
            elif self.currentcolumn == 4:
                item = QTableWidgetItem(str(self.price))
            elif self.currentcolumn == 5:
                item = QTableWidgetItem(str(self.press))
            elif self.currentcolumn == 6:
                item = QTableWidgetItem(str(self.publish_time))
            # 使表格无法编辑
            self.tableWidget.setItem(self.currentrow,self.currentcolumn, item)
    #创建存储过程
    def pushB_create_Clicked(self):
        #获取其中的内容
        sql =self.textEdit_2.toPlainText()
        # sql = "CREATE PROCEDURE demo_proc(IN p_in int,OUT p_out int)\
        # BEGIN \
        #      set p_out=2; \
        # END"
        sql.replace('\n', '\\')
        if sql=='':
            root11 = Tk()
            root11.withdraw()  # 隐藏主窗口
            tkinter.messagebox.showinfo(title='提示', message='创建的存储过程内容不能为空')
            return 0

        # cur.execute(sql)
        try:
            cur.execute(sql)
        except Exception as err:
            root12 = Tk()
            root12.withdraw()  # 隐藏主窗口
            tkinter.messagebox.showinfo(title='提示', message=err)
            return 0

        root12 = Tk()
        root12.withdraw()  # 隐藏主窗口
        tkinter.messagebox.showinfo(title='提示', message='创建成功！')
        return 0
    #执行存储过
    def pushB_excute_Clicked(self):
        # 获取其中的内容
        sql = self.textEdit_2.toPlainText()
        sql.replace('\n', '\\')
        if len(sql)==0:
            root22 = Tk()
            root22.withdraw()  # 隐藏主窗口
            tkinter.messagebox.showinfo(title='提示', message='执行不能为空!')
            return 0

        try:
            cur.execute(sql)
        except Exception as er:
            root21 = Tk()
            root21.withdraw()  # 隐藏主窗口
            tkinter.messagebox.showinfo(title='提示', message=er)
            return 0
        res = cur.fetchall()
        res=str(res)
        #         #将其打印在结果栏
        self.textEdit.setPlainText(res)
        #将其打印在结果栏



        # #首先判断语法是否正确
        # if len(sql)<=5 or sql[0]!='c' or sql[1]!='a' or sql[2]!='l' or sql[3]!='l' or sql[4]!=' ':
        #     root21 = Tk()
        #     root21.withdraw()  # 隐藏主窗口
        #     tkinter.messagebox.showinfo(title='提示', message='语法出现错误!')
        #     return 0
        #
        # #有括号的情况
        # if '(' in sql:
        #     #没有右括号
        #     if '(' not in sql:
        #         root23 = Tk()
        #         root23.withdraw()  # 隐藏主窗口
        #         tkinter.messagebox.showinfo(title='提示', message='语法出现错误!')
        #         return 0
        #     pl=sql.find('(')#左括号位置
        #     #提取过程名
        #     proc=sql[5:pl]
        #     #提取参数
        #     pr=sql.find(')')
        #     parameter=sql[pl+1:pr]
        #     if len(parameter)==0:
        #         #则不用参数
        #         #直接执行即可
        #         try:
        #             cur.callproc(proc)
        #         except EXCEPTION as er:
        #             root24 = Tk()
        #             root24.withdraw()  # 隐藏主窗口
        #             tkinter.messagebox.showinfo(title='提示', message=er)
        #             return 0
        #         res = cur.fetchall()
        #         #将其打印在结果栏
        #         self.textEdit.setPlainText(res)
        #     else:#有参数的情况
        #         #有多个参数的情况
        #         if ',' in parameter:
        #             paralist=parameter.split(',')
        #
        #
        #
        #
        #
        #
        #
        #     #有多个参数的情况
        #     if ',' in parameter:
        #     print(proc)
        #     print(parameter)





        # # 调用 p1 存储过程，传入4个参数
        # cusr.callproc('p1', args=(1, 2, 3, 4))
        #
        # # 返回获得的集合，即存储函数中的 SELECT * FROM tmp; 结果
        # res1 = cusor.fetchall()
        # print(res1)
        #
        # if sql == '':
        #     root11 = Tk()
        #     root11.withdraw()  # 隐藏主窗口
        #     tkinter.messagebox.showinfo(title='提示', message='创建的存储过程内容不能为空')
        #     return 0

        # cur.execute(sql)
        # try:
        #     cur.execute(sql)
        # except Exception as err:
        #     root12 = Tk()
        #     root12.withdraw()  # 隐藏主窗口
        #     tkinter.messagebox.showinfo(title='提示', message=err)
        #     return 0

        root12 = Tk()
        root12.withdraw()  # 隐藏主窗口
        tkinter.messagebox.showinfo(title='提示', message='执行成功！')
        return 0

#清除存储过程
    def pushB_clear_Clicked(self):
        self.textEdit.clear()
        self.textEdit_2.clear()

#定义登录界面的类
class SignWindow(QWidget, Ui_Form1):
    def __init__(self, parent=None):
        super(SignWindow, self).__init__()
        self.setupUi(self)
        # 使按键使能
        self.pushButton_2.setEnabled(True)
        self.pushButton.setEnabled(True)
        self.pushButton.clicked.connect(self.pushB_sign_Clicked)
        self.pushButton_2.clicked.connect(self.pushB_exit_Clicked)
        self.pushButton_3.clicked.connect(self.pushB_clear_Clicked)
        

    def pushB_sign_Clicked(self):

        host=self.lineEdit.text()  # 读取输入的信息不能为空
        port=self.lineEdit_3.text()
        user=self.lineEdit_2.text()  # 读取输入的信息不能为空
        password=self.lineEdit_4.text()  # 读取输入的信息不能为空
        db=self.lineEdit_5.text()  # 读取输入的信息不能为空
        if host=='' or port=='' or user=='' or password=='' or db=='':
            root31 = Tk()
            root31.withdraw()  # 隐藏主窗口
            tkinter.messagebox.showinfo(title='提示', message='请将登录信息填完整!')
            return 0
        else:
            try:
                conn = link_db(host,int(port), user, password,db)
                cur = conn.cursor()
            except Exception as er:
                root32 = Tk()
                root32.withdraw()  # 隐藏主窗口
                tkinter.messagebox.showinfo(title='提示', message=er)
                return 0
        root33 = Tk()
        root33.withdraw()  # 隐藏主窗口
        tkinter.messagebox.showinfo(title='提示', message='登录成功!')
        myapp.close()
        return 0
    #清空
    def pushB_clear_Clicked(self):

        self.lineEdit.clear()  #
        self.lineEdit_3.clear()
        self.lineEdit_2.clear()  #
        self.lineEdit_4.clear()  #
        self.lineEdit_5.clear()  #


#退出
    def pushB_exit_Clicked(self):
        sys.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # myapp=SignWindow()
    #显示登录界面
    myapp = SignWindow()
    myapp.show()
    app.exec_()
    #显示管理系统界面
    myapp1 = MainWindow()
    myapp1.show()
    app.exec_()

conn.commit()
cur.close()
conn.close()


