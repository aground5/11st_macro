from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.remote_connection import LOGGER

from PIL import Image
import time
import base64
import io
import hashlib
import logging

LOGGER.setLevel(logging.WARNING)

url1 = "https://login.11st.co.kr/auth/login.tmall?returnURL=http%253A%252F%252Fm.11st.co.kr%252FMW%252FMyPage%252FmypageHome.tmall"
url2 = 'https://m.11st.co.kr/products/ma/4461632330'
ID = ''
PW = ''

options = Options()
options.add_experimental_option('debuggerAddress','127.0.0.1:9222')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 200)

try :
    driver.get(url1)
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.NAME, 'memId'))).send_keys(ID)
    driver.find_element(By.NAME, 'memPwd').send_keys(PW)
    login = driver.find_element(By.CLASS_NAME, "bbtn")
    driver.execute_script('arguments[0].click();', login)
    time.sleep(1)
except :
    pass

driver.get(url2)
while True:
    nowSales = wait.until(
        lambda driver: driver.find_elements(by=By.XPATH, value='//div[@class="buy"]/button')
         or driver.find_elements(By.CLASS_NAME, "no_sale"))[0]
    if nowSales.text == '현재 판매중인 상품이 아닙니다.':
        driver.refresh()
        now = time.localtime()
        print("판매중지, 새로고침: " + "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
        time.sleep(1)
    else :
        startTime = time.time()
        wait.until(EC.element_to_be_clickable(nowSales))
        driver.execute_script('arguments[0].click();', nowSales)
        try :
            i = 0
            while (True) :
                selectOpt = driver.find_element(By.XPATH, '//*[@id="optlst_{}"]/li[1]/a'.format(i))
                driver.execute_script('arguments[0].click();', selectOpt)
                time.sleep(0.2)
                i += 1
        except Exception as e:
            print(e)
        try :
            optConfirm = driver.find_element(By.XPATH, '//*[@id="inputOpt0"]/div[3]/button[1]')
            driver.execute_script('arguments[0].click();', optConfirm)
        except :
            pass
        while (True) :
            try :
                confirmBuy = driver.find_element(By.XPATH, '//*[@id="optionContainer"]//div[@class="buy"]/button')
                break
            except :
                driver.execute_script('arguments[0].click();', nowSales)
        driver.execute_script('arguments[0].click();', confirmBuy)
        try :
            writeFirstOpt = driver.find_element(By.ID, 'optionText_0_0').send_keys('아니요')
            writeSecondOpt = driver.find_element(By.ID, 'optionText_0_1').send_keys('기타')
            driver.execute_script('arguments[0].click();', confirmBuy)
        except Exception as e:
            print(e)
        break
print("옵션 선택된 시간: ", time.time() - startTime)

while (True) :
    try : 
        paymentStart = driver.find_element(By.CLASS_NAME, "btn_pay")
        break
    except :
        pass
print("결제 버튼 찾음: ",time.time() - startTime)

newframe = 0
for i in range(1000):
    try:
        newframe = driver.find_element(By.ID,'skpay-ui-frame')
    except:
        driver.execute_script("arguments[0].click();", paymentStart)
        pass
    else:
        driver.switch_to.frame(newframe)
        break
    
    print("sk pay 진입 시간: ",time.time() - startTime)
    takeImage = 0
for i in range(1000):
    try:
        takeImage = driver.find_element(By.XPATH,'//*[@id="keypad11pay-keypad-0"]/span')
        if takeImage == 0:
            print('0 come')
            continue
    except:
        driver.switch_to.default_content()
        driver.switch_to.frame(newframe)
        pass
    else:
        if takeImage == 0:
            continue
        break

if takeImage == 0:
    print("-------bbom--------")
    driver.switch_to.default_content()
    driver.switch_to.frame(newframe)
    takeImage = driver.find_element(By.XPATH,'//*[@id="keypad11pay-keypad-0"]/span')
incoded = takeImage.get_attribute('style')

decodedByte = base64.b64decode(incoded[57:-28])
keypad = Image.open(io.BytesIO(decodedByte))
each_key = []
img_bytes = []
for i in range(0, 11) :
    each_key.append(keypad.crop((i * 26, 0, (i + 1) * 26, 64)))
    img_byte_arr = io.BytesIO()
    each_key[i].save(img_byte_arr, format='PNG')
    img_bytes.append(img_byte_arr.getvalue())
    enc = hashlib.md5()
    enc.update(img_bytes[i])
    img_bytes[i] = enc.hexdigest()
    
md5_hash = ["f9ac4e252fbe47c4ae55d7321943854c",     # 0
            "528b09765e7eb3a676a782e213e956b6",     # 1
            "441db6adde4fcffaf3b0b3faf4c96176",     # 2
            "0336c5499940e4051fa2f606e0f44817",     # 3
            "3860457746c2bc8f0622c5ba764f7606",     # 4
            "a9c66ce6216d15c4827cd1c730167863",     # 5
            "cd7026729c25e773f6ef53a4268f401c",     # 6
            "43c217f443b7d78ca781afc33c3db944",     # 7
            "81e3e30b0b9784f7600b797ea5f1495a",     # 8
            "ff66a4a46b731989bf1904ff228662cc",     # 9
            "26b37a54e4ae5d45a4191e08d1884d34"]     # _

md5_hbsh = ["0e034aba96b61d35212b85b29e50642b",     # 0
            "45aaa2a81cd234d139d4396f164c2c81",     # 1
            "e8cb599728a70e3c4c8697b46b69c616",     # 2
            "75ca13311fad1050ea8fa4025634fde1",     # 3
            "3860457746c2bc8f0622c5ba764f7606",     # 4
            "e0d1501b121c6a0ed33061bfd2e3e414",     # 5
            "0f5de0c6a7b2edf52b6ccae55746340b",     # 6
            "1938da87e0020fb8a077b99ac3598da5",     # 7
            "a7012c21b410b05d136289a7c39f1959",     # 8
            "83f72d05a20c3bcfac853ac6edc7fa09",     # 9
            "260ff68d7b9a67fa53c911f502d7c82c"]     # _

keyPad = [0,0,0,0,0,0,0,0,0,0,0]

for i in range(len(img_bytes)) :
    if img_bytes[i] in md5_hash :
        idx = md5_hash.index(img_bytes[i])
        keyPad[idx] = i
    elif img_bytes[i] in md5_hbsh :
        idx = md5_hbsh.index(img_bytes[i])
        keyPad[idx] = i
    else :
        print("NOT FOUND!!: {}".format(img_bytes[i]))
        each_key[i].save("{}.png".format(i))
        print(each_key[i].size)
print(keyPad)
print("sk pay 복호화: ",time.time() - startTime)
buttons = list()
for i in keyPad:
    xpath = '//*[@id="keypad11pay-keypad-'
    xpath += str(i)
    xpath += '"]/span'
    buttons.append(driver.find_element(By.XPATH,xpath))

driver.execute_script('arguments[0].click();', buttons[0])
driver.execute_script('arguments[0].click();', buttons[0])
driver.execute_script('arguments[0].click();', buttons[1])
driver.execute_script('arguments[0].click();', buttons[1])
driver.execute_script('arguments[0].click();', buttons[0])
driver.execute_script('arguments[0].click();', buttons[0])

print("sk pay 패스워드 입력됨: ",time.time() - startTime)
ars = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="popup"]/div[3]/div/button')))
ars.click()
ars_request = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-req-auth"]')))
ars_request.click()

input()
print("주문이 완료되었습니다.")
