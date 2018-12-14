import cx_Oracle
import random
import re
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidElementStateException, TimeoutException, NoSuchElementException
import time
import datetime
from config import *
from apscheduler.schedulers.blocking import BlockingScheduler
from threading import Thread
from datetime import datetime
import logging


kwSet = set([])
dataList = []


def getTime(strTime):#得到linux时间戳以及structtime
    # soup = BeautifulSoup(browser.page_source, 'lxml')  # 为什么最好要加这个？
    # 2018-09-05 10:00:00
    structTime = time.strptime(strTime, '%Y-%m-%d %X')
    secs = time.mktime(structTime) * 1000  # *1000转为毫秒
    dt = datetime.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")
    return secs, dt


def intIndex(strIndex):#得到int类型的指数
    #2,287
    return int(strIndex.replace(',', ''))

def toIndex():#去往index首页
    while True:
        try:
            browser.get("http://index.baidu.com")  # http://index.baidu.com
            break
        except:
            print('================浏览器超时，重新加载====================')
            time.sleep(5)
            #browser.refresh()

def search(cookie1, cookie2, cookie3, kwList, wait):
    """

    :rtype: list of set
    """
    dataList.clear()
    browser.maximize_window()
    # browser.delete_all_cookies()
    toIndex()
    # browser.add_cookie(cookie1)
    # browser.add_cookie(cookie2)
    # browser.add_cookie(cookie3)
    time.sleep(5)
    # 因为需要等待浏览器的加载，判断已加载成功之后再进行下一步操作

    for kw in nestedL:
        i = 0
        validKW = kw
        district = '全国'
        if nestedL.index(validKW) != 0:#如果并非首次需要重新打开页面
            while True:
                try:
                    browser.get("http://index.baidu.com")  # http://index.baidu.com
                    break
                except:
                    print('================浏览器超时，重新加载====================')
                    time.sleep(5)
        time.sleep(2)
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#search-input-form > input.search-input"))
        )
        textIn =''#带传入输入框的文本
        for k in validKW:
            textIn = textIn + k +","
        input.send_keys(textIn)  # 输入查询关键字
        try:
            browser.find_element_by_class_name('search-input-cancle').click()  # 点击搜索
        except Exception:
            time.sleep(3)
            browser.find_element_by_id('schsubmit').click()  # 点击搜索
        if isElementExist('btnbtxt'):#如不存在相应百度指数，则直接进行下一次循环
            validKW = changeState(kw)
            if len(validKW) == 0:
                continue
            else:
                time.sleep(3)
                toIndex()
                newTextIn = ''
                for n in validKW:
                    newTextIn = newTextIn + n + ","
                input = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#search-input-form > input.search-input"))
                )
                input.send_keys(newTextIn)  # 输入查询关键字
                browser.find_element_by_class_name('search-input-cancle').click()  # 点击搜索
        


        while i < 3:
            if i == 1:
                locateGD()
                district = '广东'
            elif i == 2:
                locateSZ()
                district = '深圳'
            while True:
                try:#随着页面更改selector会变
                    #GD: class name: chartselectHours Xpath://*[@id="auto_gsid_15"]/div[1]/div[1]/a[1]
                    #QG: class name: chartselectHours Xpath://*[@id="auto_gsid_15"]/div[2]/div[1]/a[1]
                    byHour = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "chartselectHours")))
                    byHour.click()  # 切换成24h显示
                    time.sleep(2)
                    byHour.click()
                    time.sleep(5)
                    break
                except InvalidElementStateException as e:
                    print('切换24小时显示发生错误: ', repr(e))
                    print('再试一次')
                except TimeoutException as e:
                    print('切换24小时显示发生错误: ', repr(e))
                    print('再试一次')
                except Exception as e:
                    print('切换24小时显示发生错误: ', repr(e))
                    print('再试一次')


            # 使鼠标悬停
            #browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            chain = ActionChains(browser)
            # css: #trend > svg > rect:nth-child(12)
            #print(validKW)
            noIndex = len(validKW)
            moveElement = browser.find_elements_by_css_selector("#trend rect")[
                noIndex*2]  # 挪到坐标图，通过id名，trend的rect下面第三个##trend rect
            chain.move_to_element(moveElement).perform()
            # xOrdi = moveElement.location['x']
            # yOrdi = moveElement.location['y']
            width = moveElement.size['width']
            # height = moveElement.size['height']
            #print(xOrdi, yOrdi, width, height)#要是位置变了可能用到
            x_0 = 1210
            y_0 = 30# 1个数的时候是30，每增加1个词多51
            for axis in range(12):
                chain.move_to_element_with_offset(moveElement, x_0, y_0).perform()
                time.sleep(5)

                while True:
                    try:
                        imgelement = browser.find_element_by_xpath('//div[@id="viewbox"]')  # 找到悬浮出来的窗口，搜了一下关键字找到了
                        timeElement = browser.find_element_by_css_selector(
                            '#viewbox > div:nth-child(1) > div.view-table-wrap')#只有1个
                        theTime = timeElement.text
                        timeTuple = getTime(theTime)
                        print("时间: ", theTime)
                        indexName = browser.find_elements_by_class_name('view-label')#得到含指数名称的list
                        indexNumber = browser.find_elements_by_class_name('view-value')#得到含指数值的list
                        noIndex = len(indexName)
                        print("得到指数名和值")
                        locations = imgelement.location
                        x = locations["x"]
                        # browser.execute_script("return window.scrollY;")
                        if x != 0.0:
                            count = 0
                            while count < noIndex:
                                dataList.append((indexName[count].text, district, timeTuple[0], timeTuple[1], intIndex(indexNumber[count].text)))
                                count += 1
                            break
                        chain.move_to_element_with_offset(moveElement, x_0 + 8, y_0).perform()
                        chain.move_to_element_with_offset(moveElement, x_0, y_0).perform()
                    except Exception:
                        print("重新悬停鼠标")
                        chain.move_to_element_with_offset(moveElement, x_0, y_0).perform()
                x_0 = x_0 - width / 23
            i += 1
        time.sleep(2)
    browser.close()
    return dataList

#更改区域为深圳
def locateSZ():
    try:
        browser.find_element_by_css_selector('#compOtharea > div > div.comBorderL > span.holdBox > i').click()
        time.sleep(2)
        browser.find_element_by_link_text("广东").click()  # 点击广东
        time.sleep(2)
        browser.find_element_by_link_text("深圳").click()  # 点击深圳
        time.sleep(2)
    except NoSuchElementException as e:
        print('选择深圳出错: ', repr(e))
        print('再试一次')
        locateSZ()
    except Exception as e:
        print('选择深圳出错: ', repr(e))
        print('再试一次')
        locateSZ()


#更改区域为广东
def locateGD():
    try:
        browser.find_element_by_css_selector(
            '#compOtharea > div > div.comBorderL > span.holdBox > i').click()  # 点击地区下拉按钮
        time.sleep(2)
        browser.find_element_by_link_text("广东").click()  # 点击广东
        time.sleep(2)
        browser.find_element_by_css_selector('#advSearchSubmit').click()  # 点击确定
        time.sleep(2)
    except NoSuchElementException as e:
        print('选择广东出错: ', repr(e))
        print('再试一次')
        locateGD()
    except Exception as e:
        print('选择广东出错: ', repr(e))
        print('再试一次')
        locateGD()


#进行账号登录
def getCookie(browser):
    bdUrl = 'http://www.baidu.com'

    browser.delete_all_cookies()
    while True:
        try:
            browser.get(bdUrl)
            break
        except Exception as e:
            logging.exception(e)
            print('================浏览器超时，重新加载====================')
    # print(driver.get_cookies())
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="u1"]/a[7]').click()  # 打开登陆框
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__footerULoginBtn"]').click()  # 打开账户密码登录
    time.sleep(5)
    browser.find_element_by_id('TANGRAM__PSP_10__userName').send_keys(userName)  # 输入账户名
    time.sleep(5)
    browser.find_element_by_id('TANGRAM__PSP_10__password').send_keys(passWord)  # 输入密码
    time.sleep(5)
    browser.find_element_by_id("TANGRAM__PSP_10__submit").click()  # 点击登陆
    time.sleep(10)
    cookies = browser.get_cookies()
    if cookies:
        print('得到cookie')
    time.sleep(5)
    return cookies

def isElementExist(element):#根据class判断某元素是否存在，如果element存在就返回True
    token = False
    try:
        browser.find_element_by_class_name(element)
        return True
    except:
        return token
    
    

def changeState(ls):#对不存在百度指数的关键字，将其在数据库的状态改为1
    #outKW长这样，“ 小桃子,大桃子,甜茶的桃 ” 并且在elements里还有换行和空格
    outKW = browser.find_element_by_css_selector('body > div.mw1300.wrapper > div:nth-child(1) > span').text
    outKW = outKW[1:-1].replace(' ','').replace('\n','')#从左到右按顺序执行
    outList = outKW.split(',')
    for i in outList:
        ls.remove(i)

    try:
        conn = cx_Oracle.connect('wechat/wechat123@10.153.122.25:1521/SZQX')
        version = conn.version

        if version:
            print('更改state时，关键字数据库连接成功')
        cursor = conn.cursor()
        for i in outList:
            cursor.execute("UPDATE CLIMATE_INDEXKW SET STATE = 1 WHERE KW = :1", (i,))
        print('已更改state')
        cursor.close()  # 关闭cursor
        conn.commit()
        conn.close()  # 关闭连接
    except cx_Oracle.DatabaseError as e:
        print('数据库连接错误: ', repr(e))
        changeState()
    print(ls)
    return ls#返回有效的关键词



#从数据库获取关键字
def getKW():
    print('获取关键字')
    try:
        conn = cx_Oracle.connect('wechat/wechat123@10.153.122.25:1521/SZQX')
        version = conn.version

        if version:
            print('关键字数据库连接成功')
        cursor = conn.cursor()
        cursor.execute("SELECT KW FROM CLIMATE_INDEXKW WHERE STATE = 0")
        kws = cursor.fetchall()
        for kw in kws:
            kwSet.add(kw[0])
        cursor.close()  # 关闭cursor
        conn.commit()
        conn.close()  # 关闭连接
    except cx_Oracle.DatabaseError as e:
        print('数据库连接错误: ', repr(e))
        getKW()

#将数据存入数据库
def storeData(dic):
    try:
        conn = cx_Oracle.connect('wechat/wechat123@10.153.122.25:1521/SZQX')
        version = conn.version
        if version:
            print('存数据的数据库连接成功')
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO CLIMATE_INDEX(KW, AREA, TIME, DATETIME, INDEXNUMBER) VALUES(:1, :2, :3, :4, :5)", dic)
        cursor.close()#关闭cursor
        conn.commit()
        conn.close()#关闭连接
        print("数据插入成功")
        print("========================等待12小时继续爬取============================")
    except cx_Oracle.DatabaseError as e:
        print('数据库连接错误: ', repr(e))


def timedTask(browser, wait):

    print(time.asctime(), "开始获取数据")
    cookies = getCookie(browser)
    cookie1 = cookies[-3]
    cookie2 = cookies[-2]
    cookie3 = cookies[-1]

    result = search(cookie1, cookie2, cookie3, kwList, wait)  # 得到的text
    print("=======================待传入数据=======================\n", result)
    storeData(result)

def splitL(ls):
    nestedL=[]
    for i in range(0,len(ls),5):
        smallL = ls[i:i+5]
        nestedL.append(smallL)
    return nestedL



def job():
    getKW()
    kwList = list(kwSet)
    print("搜索关键字：", kwList)
    nestedL = splitL(kwList)#获取切分为5个1组的list
    var = random.random()
    print("随机睡0-60秒")
    time.sleep(var * 60)  # 先返回了0到1的随机数，再乘以1分钟
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(
        '"User-Agent"="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15"')
    browser = webdriver.Chrome()
    browser.set_page_load_timeout(10)  # 给浏览器设置超时
    browser.implicitly_wait(10)
    wait = WebDriverWait(browser, 15)
    timedTask(browser, wait)

if __name__ == '__main__':
    print('程序启动时间', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron',  hour='1, 12', minute='30')
    scheduler.start()


# 怎么用cookie登录百度
# https://blog.csdn.net/maybe_frank/article/details/77881009
# selenium官方文档
# https://selenium-python.readthedocs.io/navigating.html#filling-in-forms
# 获取图片参考
# https://blog.csdn.net/qq_26877377/article/details/80860722
