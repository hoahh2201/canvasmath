"""
This module is the main flask application.
"""


# import firebase_admin
from flask import Flask, request, render_template
from blueprints import *
import cv2
import numpy as np
import tensorflow as tf
from ilovemath_function import functions

# Initialize Firebase Admin SDK.
# See https://firebase.google.com/docs/admin/setup for more information.

# firebase = firebase_admin.initialize_app()

app = Flask(__name__)
app.secret_key = b'A Super Secret Key'


model = tf.keras.models.load_model('static/y_v1.h5')
label_names = ['0', '1', '13', '17', '19', '2', '20', '23', '25', '27', '28', '3',
       '4', '5', '6', '7', '8', '9']



app.register_blueprint(home_page)


@app.route("/upload/", methods=["POST"])
def upload_file():
    img_raw = functions.parse_image(request.get_data())
    nparr = np.fromstring(img_raw, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    edged = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in  cnts], key=lambda x: x[1])

    math_detect = []
    canw=0
    for (c, _) in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w >=5 and h>5:
            roi = edged[y:y+int(1.2*h), x:x+w]
            thresh = roi.copy()
            # img_roi = Image.fromarray(roi)
            # img_roi.save("./saveroi/9/9_" + str(x+y*2+w+h) + ".jpg")
            # print("save oke")
            thresh = functions.deskew(thresh, 28)
            thresh = functions.center_extent(thresh, (28, 28))
            thresh = np.reshape(thresh, (28, 28, 1))
            thresh = thresh / 255
            predictions = model.predict(np.expand_dims(thresh, axis=0))
            digit = np.argmax(predictions[0])
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(image, label_names[digit], (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)

            if (label_names[digit] == "20" and y<100):
                math_detect.append("sqrt(")
                canw = w

            elif (label_names[digit] == "0" and y<100):
                math_detect.append("sqrt(")
                canw = w

            elif label_names[digit] == "1":
                countt = 0
                mem = []
                for i in range(len(thresh[9])):
                    if thresh[9][i] > 0: 
                        countt +=1
                        mem.append(i)
                if countt > 3 :
                    if x<canw: 
                        math_detect.append("love1")
                        
                    else: 
                        math_detect.append("1")

                elif countt == 3:
                    if mem[1] + 1 != mem[2]: 
                        if x<canw: 
                            math_detect.append("love1")

                        else: 
                            math_detect.append("1")

                else:
                        if x<canw: 
                            math_detect.append("love/")

                        else: 
                            math_detect.append("/")

            elif label_names[digit] == "13":
                countt = 0
                mem99 = []
                countt_test=True
                for i99 in range(len(thresh[9])):
                    if thresh[20][i99] > 0: 
                        countt +=1
                        mem99.append(i99)

                if countt > 4 :
                    math_detect.append("*")

                elif (countt == 3) or (countt == 4):
                    for mem_mem in range(len(mem99)-1):
                        if mem99[mem_mem]+1!=mem99[mem_mem+1]:
                            countt_test = False
                            break

                        else:
                            countt_test = True

                    if countt_test==True:
                        math_detect.append("y")

                    else:
                        math_detect.append("*")

                elif countt < 4:
                        math_detect.append("y")



            elif label_names[digit] == "8":
                count2w = 0
                for px in range(len(thresh[10])):
                    if thresh[16][px] > 0:
                        count2w +=1

                if count2w > 3 :
                    if x<canw: 
                        if y<75: 
                            math_detect.append("love**8")

                        else: 
                            math_detect.append("love8")

                    else: 
                        if y<75: 
                            math_detect.append("**8")

                        else: 
                            math_detect.append("8")

                else: 
                    if x<canw: 
                        if y<75: 
                            math_detect.append("love**3")

                        else: 
                            math_detect.append("love3")

                    else: 
                        if y<75: 
                            math_detect.append("**3")

                        else: 
                            math_detect.append("3")



            elif (label_names[digit] == "9") and (h>100):
                count2q = 0
                for px in range(len(thresh[10])):
                    if thresh[12][px] > 0:
                        count2q +=1


                count3q = 0
                for px in range(len(thresh[10])):
                    if thresh[16][px] > 0:
                        count3q +=1

                if (count2q > 3) and (count3q <4) :
                    if x<canw: 
                        if y<75: 
                            math_detect.append("love**9")

                        else: 
                            math_detect.append("love9")
                    else: 
                        if y<75: 
                            math_detect.append("**9")

                        else: 
                            math_detect.append("9")

                elif (count2q > 3) and (count3q >3) :
                    if x<canw: 
                        if y<75: 
                            math_detect.append("love**8")

                        else: 
                            math_detect.append("love8")

                    else: 
                        if y<75: 
                            math_detect.append("**8")

                        else: 
                            math_detect.append("8")

                else: 
                    if x<canw: 
                        if y<75: 
                            math_detect.append("love**3")

                        else: 
                            math_detect.append("love3")

                    else: 
                        if y<75: 
                            math_detect.append("**3")

                        else: 
                            math_detect.append("3")



            elif (label_names[digit] == "9") and (h<150):
                count222 = 0
                count222_list=[]
                count222_test = True
                for px in range(len(thresh[10])):
                    if thresh[8][px] > 0:
                        count222 +=1
                        count222_list.append(px)
                for px2 in range(len(count222_list)-1):
                    if count222_list[px2]+1!=count222_list[px2+1]:
                        count222_test=False
                    else:
                        count222_test=True


                count333 = 0
                count333_list=[]
                count333_test=True
                for px in range(len(thresh[10])):
                    if thresh[20][px] > 0:
                        count333 +=1
                        count333_list.append(px)
                
                for px3 in range(len(count222_list)-1):
                    if count222_list[px3]+1!=count222_list[px3+1]:
                        count222_test=False
                    else:
                        count222_test=True                

                if (count222 > 4) and (count333 <4) :
                    if x<canw: 
                        if y<75: 
                            math_detect.append("love**9")

                        else: 
                            math_detect.append("love9")

                    else: 
                        if y<75: 
                            math_detect.append("**9")

                        else: 
                            math_detect.append("9")

                elif (count222 > 4) and (count333 >4) :
                    if x<canw: 
                        if y<75: 
                            math_detect.append("love**8")

                        else: 
                            math_detect.append("love8")

                    else: 
                        if y<75: 
                            math_detect.append("**8")

                        else: 
                            math_detect.append("8")

                elif (count222 ==4) and (count333_test == True) and (count333_test==True) :
                    if x<canw: 
                        if y<75: 
                            math_detect.append("love**3")
                        else: 
                            math_detect.append("love3")

                    else: 
                        if y<60: 
                            math_detect.append("**3")

                        else: 
                            math_detect.append("3")

                else: 
                    if x<canw: 
                        if y<75: 
                            math_detect.append("love**3")

                        else: 
                            math_detect.append("love3")

                    else: 
                        if y<75: 
                            math_detect.append("**3")

                        else: 
                            math_detect.append("3")


            elif (label_names[digit] == "2") and (h<150):
                count2112 = 0
                count2212_list =[]
                test_2212 = True
                for px in range(len(thresh[6])):
                    if thresh[12][px] > 0:
                        count2112 +=1
                        count2212_list.append(px)



                if count2112 > 4 :
                    if x<canw: 
                        if y<75: 
                            math_detect.append("love**8")
                        else: 
                            math_detect.append("love8")

                    else: 
                        if y<75: 
                            math_detect.append("**8")

                        else: 
                            math_detect.append("8")
                
                if count2112 == 4:
                    for px2 in range(len(count2212_list)-1):
                        
                        try:
                            if count2212_list[px]+1!=count2212_list[px+1]:
                                test_2212 = False
                                break

                            else:
                                test_2212 = True
                        except:
                            pass
                        
                    if test_2212==True:
                        if x<canw:
                            if y<75: 
                                math_detect.append("love**2")

                            else: 
                                math_detect.append("love2")

                        else: 

                            if y<75: 
                                math_detect.append("**2")
                            else: 
                                math_detect.append("2") 

                    elif test_2212==False:
                        if x<canw: 
                            if y<75: 
                                math_detect.append("love**8")
                            else: 
                                math_detect.append("love8")

                        else: 
                            if y<75: 
                                math_detect.append("**8")

                            else: 
                                math_detect.append("8")                                                 




                if count2112 < 4:
                    if x<canw: 
                        if y<75: 
                            math_detect.append("love**2")

                        else: 
                            math_detect.append("love2")

                    else: 
                        if y<75: 
                            math_detect.append("**2")

                        else: 
                            math_detect.append("2")


            elif (label_names[digit] == "2") and (h>150):
                count22 = 0
                for px in range(len(thresh[10])):
                    if thresh[10][px] > 0:
                        count22 +=1


                if count22 > 3 :
                    if x<canw: 
                        if y<75: 
                            math_detect.append("love**8")
                        else: 
                            math_detect.append("love8")
                    else: 
                        if y<75: 
                            math_detect.append("**8")
                        else: 
                            math_detect.append("8")
                else: 
                    if x<canw: 
                        if y<75: 
                            math_detect.append("love**2")
                        else: 
                            math_detect.append("love2")
                    else: 
                        if y<75: 
                            math_detect.append("**2")
                        else: 
                            math_detect.append("2")




            elif y < 75 and label_names[digit] in ["0","1","2","3","4","5","6","7","8","9"]:

                    if x<canw: 
                        math_detect.append("love**" + label_names[digit])

                    else: 
                        math_detect.append("**" + label_names[digit])

            elif y>=75:

                    if x<canw: 
                        math_detect.append("love" + label_names[digit])

                    else: 
                        math_detect.append(label_names[digit])


    def convert_math(math_detect):
        for j in range(0, len(math_detect)-1):        
            if "love" in math_detect[j] and "love" in math_detect[j+1]: 
                math_detect[j]=math_detect[j].split("ve")[1]
        for jj in range(0, len(math_detect)):        
            if "love" in math_detect[jj]:
                math_detect[jj]=math_detect[jj].split("ve")[1] + ")"
        for i in range(0, len(math_detect)):

            if math_detect[i] == '18':
                math_detect[i] = '/'
            elif math_detect[i] == '13':
                math_detect[i] = '*'
            elif math_detect[i] == '23':
                math_detect[i] = '+'
            elif math_detect[i] == '20':
                math_detect[i] = '-'
            elif math_detect[i] == '19':
                math_detect[i] = 'x'
            elif math_detect[i] == '27':
                math_detect[i] = '<'
            elif math_detect[i] == '25':
                math_detect[i] = '>'
            elif math_detect[i] == '28':
                math_detect[i] = 'y'

            elif math_detect[i] == '18)':
                math_detect[i] = '/'
            elif math_detect[i] == '13)':
                math_detect[i] = '*'
            elif math_detect[i] == '23)':
                math_detect[i] = '+'
            elif math_detect[i] == '20)':
                math_detect[i] = '-'
            elif math_detect[i] == '19)':
                math_detect[i] = 'x'
            elif math_detect[i] == '27)':
                math_detect[i] = '<'
            elif math_detect[i] == '25)':
                math_detect[i] = '>'
            elif math_detect[i] == '28)':
                math_detect[i] = 'y'
        return math_detect


    def calculate_string(math_detect):
        math_detect = convert_math(math_detect)
        calculator = ''.join(str(item) for item in math_detect)
        result = calculator
        b=0
        if "---" in result: result=result.replace("---","=-",1)

        if "--" in result:
            result=result.replace("--","=",1)
        if ("sqrt(" in result) and (")" not in result):
            a = int(result.split("sqrt(")[0])
            try:
                b = int(result.split("sqrt(")[1])
            except:
                pass
            if (b == 0) or (a==b):
                result = "Squares: a = %d"%a
            if (b!=a) and (b!=0):
                result = "Rectangle: a = %d; b = %d" %(a,b)    

        return result

    result = calculate_string(math_detect)

    return result


@app.route("/calcu/", methods=["POST"])
def calcu():
    val = request.get_data()
    val = str(request.get_data())
    val1=val[2:-1]

    if ("sqrt" in val1) and (")" not in val1):
        if (val1[-4:-1] == ")=-") or (val1[-5:-2] == ")=-") or (val1[-6:-3] == ")=-"):
            return "No solution"
        
    elif "Squares" in val1:
        a = int(val1.split(" ")[-1])
        kq1 = "S = %d^2 = %d; P = 4*%d = %d" %(a,a**2,a,4*a)
        return kq1

    elif "Rectangle" in val1:
        b = int(val1.split(" ")[-1])
        a = int(val1.split(" ")[-4][:-1])
        kq1 = "S = %d*%d = %d; P = (%d+%d)*2 = %d" %(a, b, a*b, a, b, (a+b)*2)
        return kq1

    elif "y" in val1:
        return val1
    elif "=" in val1: 
        val2=val1
        degit_mem1=int(eval(val2.split("=")[1]))
        val_phu=val2.split("=")[0]

        if degit_mem1 == 0:
            val1=val_phu
        elif degit_mem1 > 0:
            val1=val_phu + "-"+str(degit_mem1)

        else:
            val1=val_phu + str(abs(degit_mem1))



    kq1=''
    if ("sqrt" in val1) and ("x" not in val1) and (")" in val1):
        degit_mem = val1.split(")")[1]
        can_so = val1.split(")")[0]
        if degit_mem != "": degit_mem=eval(degit_mem)
        else: degit_mem=0
        kq = np.sqrt(eval(can_so[5:])) + (degit_mem)
        return (str(kq))

    

    
    if ("<" in val1):
        val2=val1

        degit_mem1=int(eval(val2.split("<")[1]))
        val_phu=val2.split("<")[0]

        if degit_mem1 == 0:
            val1=val_phu

        elif degit_mem1 > 0:
            val1=val_phu + "-"+str(degit_mem1)

        else:
            val1=val_phu + str(abs(degit_mem1))

        for ele in range(len(val1)):
            if (val1[ele] == "x") and (val1[ele+1]!="*"):
                index5=ele
                break

        val1=val1[:index5+1]+str(eval(val1[index5+1:]))  



        a,b,c,d=functions.getabcd(val1)
        a=int(a)
        b=int(b)
        c=int(c)
        d=int(d)
        if a == 0:
            if (c**2-4*b*d)<0:
                if b<0:
                    kq1 = "x = R"
                if b>0:
                    kq1 = "No solution"
            else:

                kq1=functions.inequation2_smaller(b,c,d)

                return kq1
        else:
            kq1=functions.inequation3_smaller(a,b,c,d)
            return kq1

    elif (">" in val1):
        val2=val1

        degit_mem1=int(eval(val2.split(">")[1]))
        val_phu=val2.split(">")[0]

        index55=0
        if degit_mem1 == 0:
            val1=val_phu

        elif degit_mem1 > 0:
            val1=val_phu + "-"+str(degit_mem1)

        else:
            val1=val_phu + str(abs(degit_mem1))

        if val1[-1] !="x":
            for ele in range(len(val1)-1):
                if (val1[ele] == "x") and (val1[ele+1]!="*"):
                    index55=ele

                    break
            if index55 !=0: val1=val1[:index55+1]+str(eval(val1[index55+1:]))    

        a,b,c,d=functions.getabcd(val1)
        a=int(a)
        b=int(b)
        c=int(c)
        d=int(d)
        if a ==0:
            if (c**2-4*b*d)<0:
                if b<0:
                    kq1 = "x = R"
                if b>0:
                    kq1 = "No solution"
            else:
                kq1=functions.inequation2_bigger(b,c,d)

                return kq1
        else:
            kq1 = functions.inequation3_bigger(a,b,c,d)
            return kq1
   


    elif ("x**4" in val1) and ("x**2" in val1) and ("x**3" not in val1):

        if val1[-1] == "x":
            return(val1)
        else:
            for i in range(len(val1)-1):
                if val1[i] == "x" and val1[i+1] != "*":
                    return(val1)
            else:

                val1=val1.replace("x**2","x",1)
                val1=val1.replace("x**4","x**2",1)

                a , b, c, d = functions.getabcd(val1)

                d=int(d)
                b=int(b)
                c=int(c)
                result = ""
                if b!=0:
                    delta=c**2-4*b*d
                    if delta<0:
                        result += "No solution"
                        return result
                    elif (delta == 0) and (-c/(2*b) >=0):
                        xx = np.sqrt(-c/(2*b))
                        xx_1 = "%.2f" % xx
                        result += "x = +-" + str(xx_1)
                        return result
                    else:
                        roots_2=[]
                        x1 = (-c + np.sqrt(delta))/(2*b)
                        x2 = (-c - np.sqrt(delta))/(2*b)
                        if x1>0:
                            xx_1=np.sqrt(x1)
                            roots_2.append(xx_1)
                            roots_2.append(-xx_1)

                        if x2>=0:
                            xx_2=np.sqrt(x2)
                            roots_2.append(xx_2)
                            roots_2.append(-xx_2)

                        if x1==0:
                            xx_1=np.sqrt(x1)
                            roots_2.append(xx_1)

                        if x2==0:
                            xx_2=np.sqrt(x2)
                            roots_2.append(xx_2)


                        if x1<0 and x2<0:
                            result += "No solution"
                            return result
                        
                        for i1 in range(len(roots_2)):
                            xx_5 = "%.2f"% roots_2[i1]
                            kq1 += "x" + str(i1+1) + " = " + str(xx_5) + "; " 
                        
                        return(kq1)

                if b==0:
                    result+="x = " + str(-d/c)
                    return result            
                        
        return(kq1)
                

    elif ("sqrt" in val1) and ("x" in val1) and (")" in val1):

        degit_mem = val1.split(")")[1]
        can_so = val1.split(")")[0]

        if degit_mem != "": 
            degit_mem=int(eval(degit_mem))

        else: 
            degit_mem=0

        can_so=can_so[5:]
        a, b, c , d = functions.getabcd(can_so)

        if a!=0:
            roots = functions.solve(int(a), int(b), int(c), int(d)-degit_mem**2)
            for i in range(len(roots)):
                kq_str_mem = str(roots[i])

                if (kq_str_mem[-3]=="0") or (kq_str_mem[-4]=="0"):
                    xx = "%.2f"%roots[i]
                    kq1 += "x" + str(i+1) + " = " + str(xx) + "; "  

            return(kq1)

        else:

            kq1=functions.solve_2(int(b),int(c),int(d)-degit_mem**2)
            return kq1


    elif ("x" not in val1):
        kq=eval(val1)
        return(str(kq))

    else:
        a, b, c, d = functions.getabcd(val1)

        if a!=0:
            roots = functions.solve(int(a), int(b), int(c), int(d))

            for i in range(len(roots)):
                kq_str_mem = str(roots[i])

                if  ("j" not in kq_str_mem):
                    xx = "%.2f"%roots[i]
                    kq1 += "x" + str(i+1) + " = " + str(xx) + "; "

                elif (kq_str_mem[-3]=="0") and ("j" in kq_str_mem):
                    xx = "%.2f"%roots[i]
                    kq1 += "x" + str(i+1) + " = " + str(xx) + "; "


            if "x3 = -0.00;"  in kq1: 
                kq1=kq1.replace("x3 = -0.00;","",1)
            
            if "x2 = -0.00;"  in kq1: 
                kq1=kq1.replace("x2 = -0.00;","",1)

            if "x1 = -0.00;"  in kq1: 
                kq1=kq1.replace("x1 = -0.00;","",1)

            if ("x1 = 0.00;" in kq1) and  ("x2 = 0.00;" in kq1): 
                kq1=kq1.replace("x2 = 0.00;","",1)

            if ("x1 = 0.00;" in kq1) and  ("x3 = 0.00;" in kq1): 
                kq1=kq1.replace("x3 = 0.00;","",1)

            if ("x2 = 0.00;" in kq1) and  ("x3 = 0.00;" in kq1): 
                kq1=kq1.replace("x3 = 0.00;","",1)
            return(kq1)
        else:
            kq1=functions.solve_2(int(b), int(c), int(eval(d)))

            return kq1

@app.route("/get_abcd_graph/", methods=["POST"])
def get_abcd_graph():
    val = request.get_data()
    val = str(request.get_data())
    val1=val[2:-1]
    res = ''

    if "y" in val1:
        val2=val1.split("=")[1]
        a, b, c, d = functions.getabcd(val2)
        res = str(d)+','+str(c)+','+str(b)+','+str(a)
        return res

    else: 
        return res


@app.route("/get_type_math/", methods=["POST"])
def get_type_math():
    val = request.get_data()
    # kq = eval(val)
    # return(str(kq))
    val = str(request.get_data())
    val1=val[2:-1]
    if ("x" not in val1) and ("Square:" not in val1) and ("Rectangle" not in val1):
            return "https://www.youtube.com/embed/Sch0tzp-N64;https://www.youtube.com/embed/43a9jRSczt4;https://www.youtube.com/embed/8fKDstky1Kw;https://www.youtube.com/embed/hcXELKSHthM;https://www.youtube.com/embed/fdEcZqJQoaA"
    
    else:

        if ("x**4" not in val1) and ("x**3" not in val1) and ("x**2" not in val1) and ("sqrt" not in val1) and ("y" not in val1) and ("<" not in val1) and (">" not in val1) and ("Square:" not in val1) and ("Rectangle" not in val1):
            return "https://www.youtube.com/embed/iDh3x4wSMpU;https://www.youtube.com/embed/P6g8rFOKMcU;https://www.mathletics.com/us/for-schools/;https://en.wikipedia.org/wiki/Linear_equation"
        
        if ("x**4" not in val1) and ("x**3" not in val1) and ("sqrt" not in val1) and ("y" not in val1) and ("<" not in val1) and (">" not in val1) and ("Square:" not in val1) and ("Rectangle" not in val1):
            return "https://www.youtube.com/embed/8_NH_2-nDVc;https://www.youtube.com/embed/Cn1aFaxRyeU;https://www.youtube.com/embed/DJMH2F3GuIc;https://en.wikipedia.org/wiki/Quadratic_equation"
        
        if ("x**4" not in val1) and ("sqrt" not in val1) and ("y" not in val1) and ("<" not in val1) and (">" not in val1) and ("Square:" not in val1) and ("Rectangle" not in val1):
            return "https://www.youtube.com/embed/Zca-gVo-cPU;https://www.youtube.com/embed/hXXdCRsNYOU;https://www.wikihow.com/Solve-a-Cubic-Equation;https://en.wikipedia.org/wiki/Cubic_function"
        
        if ("sqrt" not in val1) and ("y" not in val1) and ("<" not in val1) and (">" not in val1) and ("Square:" not in val1) and ("Rectangle" not in val1):
            return "https://www.youtube.com/embed/1fbKaIAUTyY;https://www.youtube.com/embed/GNln3GbJJH0;https://brilliant.org/wiki/factor-polynomials-ax4-bx2-c/;https://www.tiger-algebra.com/drill/ax~4_bx~2_c=0/"
        
        if ("sqrt" in val1) and ("y" not in val1) and ("<" not in val1) and (">" not in val1) and ("Square:" not in val1) and ("Rectangle" not in val1):
            return "https://www.youtube.com/embed/wSBxW7LW3DA;https://www.youtube.com/embed/g3rzuggIgIw;https://www.youtube.com/embed/0gicD4STzpg;https://www.youtube.com/embed/Ymcf14wC9Ck;https://www.youtube.com/embed/B4zejSI8zho;https://en.wikipedia.org/wiki/Square_root"
        
        if ("<" in val1) or (">" in val1) and ("Square:" not in val1) and ("Rectangle" not in val1):
            return "https://www.youtube.com/embed/0X-bMeIN53I;https://www.youtube.com/embed/Fd5ys4PQ-aM;https://www.youtube.com/embed/SJo4wl0kfCw;https://www.youtube.com/embed/mwJbxQmaM7g;https://www.youtube.com/embed/D95yyCJhXK4;https://en.wikipedia.org/wiki/Inequation"
        
        if ("y" in val1) and ("**" not in val1) and ("Square:" not in val1) and ("Rectangle" not in val1):
            return "https://www.youtube.com/embed/vkTXDGpzy3U;https://www.youtube.com/embed/kgD48XXVT1c;https://www.youtube.com/embed/avuIdZ3nn1Y;https://www.mathplanet.com/education/algebra-1/quadratic-equations/the-graph-of-y-ax-2-plus-bx-plus-c;https://en.wikipedia.org/wiki/Linear_equation"
        
        if ("y" in val1) and ("x**3" not in val1) and ("Square:" not in val1) and ("Rectangle" not in val1):
            return "https://www.youtube.com/embed/Cn1aFaxRyeU;https://www.youtube.com/embed/Hq2Up_1Ih5E;https://www.youtube.com/embed/Xolb1TuC1Y4;https://www.youtube.com/embed/2cp0SyK5blY;https://en.wikipedia.org/wiki/Quadratic_equation"
        
        if ("y" in val1) and ("x**3" in val1) and ("Square:" not in val1) and ("Rectangle" not in val1):
            return "https://www.youtube.com/embed/Lj3uV8HfkSg;https://www.youtube.com/embed/KSQNk_B11ko;https://www.youtube.com/embed/vUNgcN6MbjA;https://www.youtube.com/embed/gmNunmyzZ3E;https://www.youtube.com/embed/zXKk7ZBCpAw;http://jwilson.coe.uga.edu/EMAT6680Fa07/Morgan/mlmass3/assingment3.html"
        
        if "Squares" in val1:
            return "https://www.youtube.com/embed/mJbUDSoe2_Q;https://www.youtube.com/embed/MTlsJ4uO18I;https://www.youtube.com/embed/ei5FAinKXoY;https://www.khanacademy.org/math/pre-algebra/pre-algebra-measurement/pre-algebra-area/v/measuring-area-with-partial-unit-squares-math-3rd-grade-khan-academy"    

        if "Rectangle" in val1:
            return "https://www.youtube.com/embed/U-goOl49wRo;https://www.youtube.com/embed/UfUwTtaHyp8;https://www.youtube.com/embed/MLpMVJgl2v8;https://www.youtube.com/embed/ECJfSyg_Obo"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)