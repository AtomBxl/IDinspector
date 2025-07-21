import tkinter as tk
from tkinter import messagebox
import datetime as dt

#强制规则检查
def validate_id_card(idNum):
    if len(idNum) == 0:
        messagebox.showerror("错误", "身份证号不能为空")
        return False

    if len(idNum) != 18:
        messagebox.showerror("错误", "身份证号不符合规则(非18位)")
        return False

    if not idNum[:17].isdigit():
        messagebox.showerror("错误", "身份证号不符合规则(前17位存在非数字)")
        return False

    checkNum = idNum[17:18]
    if not checkNum.isdigit() and checkNum.lower() != "x":
        messagebox.showerror("错误", "身份证号不符合规则(校验码位非数字或X)")
        return False

    elist = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    checklist = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]
    sum = 0
    for i in range(17):
        sum += int(idNum[i]) * elist[i]
    rem = sum % 11
    access = checklist[rem]

    if checkNum.lower() != access.lower():
        messagebox.showerror("错误", "身份证号不符合规则(校验码错误)")
        return False

    return True

#省份判断
def prov_id_card(idNum):
    prov = idNum[0:2]
    city = idNum[2:4]
    dist = idNum[4:6]
    provDict = {
        "11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林", 
        "23": "黑龙江", "31": "上海", "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", 
        "37": "山东", "41": "河南", "42": "湖北", "43": "湖南", "44": "广东", "45": "广西", "46": "海南", 
        "50": "重庆", "51": "四川", "52": "贵州", "53": "云南", "54": "西藏", "61": "陕西", "62": "甘肃", 
        "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门"
    }
    pv = provDict.get(prov, "ERROR")
    if pv == "ERROR":
        messagebox.showerror("错误", "身份证号省份无效")
        return None, None, None
    return pv, city, dist

#性别判断
def gender_id_card(idNum):
    gender = idNum[16:17]
    num_gender = int(gender)
    if num_gender % 2 == 0:
        gender = "女"
    else:
        gender = "男"
    return gender

#生日计算
def birth_id_card(idNum):
    birthY = idNum[6:10]
    birthM = idNum[10:12]
    birthD = idNum[12:14]
    nian = int(birthY)
    cYear = dt.date.today().year
    cMonth = dt.date.today().month
    cDay = dt.date.today().day

    age = cYear - nian
    if cMonth < int(birthM) or (cMonth == int(birthM) and cDay < int(birthD)):
        age -= 1

    return birthY, birthM, birthD, age

#结果输出
def show_result():
    idNum = entry_id.get()  
    if validate_id_card(idNum):  
        pv, city, dist = prov_id_card(idNum)
        birthY, birthM, birthD, age = birth_id_card(idNum)
        gender = gender_id_card(idNum)
        if pv != "ERROR":
            label_result.config(text=f"省份：{pv}\n城市：{city}\n区/县：{dist}\n生日：{birthY}年{birthM}月{birthD}日\n性别：{gender} ({age}岁)")
        else:
            label_result.config(text="身份证号省份无效")
    else:
        label_result.config(text="")

root = tk.Tk()
root.title("身份证号码校验与信息提取器")
root.geometry("400x300")

# 创建标签、输入框和按钮
label_id = tk.Label(root, text="请输入身份证号码:")
label_id.pack(pady=10)

entry_id = tk.Entry(root, width=30)
entry_id.pack(pady=10)

button_check = tk.Button(root, text="校验", command=show_result)
button_check.pack(pady=20)

label_result = tk.Label(root, text="", justify=tk.LEFT)
label_result.pack(pady=10)

root.mainloop()
