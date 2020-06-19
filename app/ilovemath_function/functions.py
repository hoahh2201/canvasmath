import re
import base64
import cv2
import numpy as np
import imutils
import mahotas
import math


def findF(a, b, c):
    return ((3.0 * c / a) - ((b ** 2.0) / (a ** 2.0))) / 3.0


# Helper function to return float value of g.
def findG(a, b, c, d):
    return (((2.0 * (b ** 3.0)) / (a ** 3.0)) - ((9.0 * b * c) / (a **2.0)) + (27.0 * d / a)) /27.0


# Helper function to return float value of h.
def findH(g, f):
    return ((g ** 2.0) / 4.0 + (f ** 3.0) / 27.0)

def parse_image(imgData):
    imgstr = re.search(b"base64,(.*)", imgData).group(1)
    img_decode = base64.decodebytes(imgstr)
    with open("output.jpg", "wb") as file:
        file.write(img_decode)
    # print('test1')
    return img_decode

def deskew(image, width):
    (h, w) = image.shape[:2]
    moments = cv2.moments(image)

    skew = moments['mu11'] / moments['mu02']
    M = np.float32([[1, skew, -0.5*w*skew],
                    [0, 1, 0]])
    image = cv2.warpAffine(image, M, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)

    image = imutils.resize(image, width=width)

    return image

def center_extent(image, size):
    (eW, eH) = size

    if image.shape[1] > image.shape[0]:
        image = imutils.resize(image, width=eW)
    else:
        image = imutils.resize(image, height=eH)

    extent = np.zeros((eH, eW), dtype='uint8')
    offsetX = (eW - image.shape[1]) // 2
    offsetY = (eH - image.shape[0]) // 2
    extent[offsetY:offsetY + image.shape[0], offsetX:offsetX+image.shape[1]] = image

    CM = mahotas.center_of_mass(extent)
    (cY, cX) = np.round(CM).astype("int32")

    # ret, thresh = cv2.threshold(image, 127, 255, 0)
    # contours, hierarchy = cv2.findContours(thresh, 1, 2)

    # cnt = contours[0]
    # M = cv2.moments(cnt)
    # cX = int(M['m10'] / M['m00'])
    # cY = int(M['m01'] / M['m00'])


    (dX, dY) = ((size[0]//2) - cX, (size[1] // 2) - cY)
    M = np.float32([[1, 0, dX], [0, 1, dY]])
    extent = cv2.warpAffine(extent, M, size)

    return extent

def getabcd(val):
    math = val.split("=")[0]
    a=0
    b=0
    c=0
    d=0
    print(math)
    if "x**3" in math:  

        index0=math.index("x**3")
    #     print(index0)
        if index0!=0: 
            a=(math[0:index0])
            if a == "": a="1"
            if a =="-": a="-1"
        else: a="1"

    #     print(a)
        if a=="1": math1=math.replace("x**3","")
        if a=="-1": math1=math.replace("-"+"x**3","")    
        if a!="1" and a!="-1": math1=math.replace(a+"x**3","")
        if math1[0]=='+': math1=math1.replace(math1[0],"",1)

        # print("math1", math1)

        if "x**2" in math1:

            index2 = math1.index("x**2")
            # print("index2",index2)
            if index2 != 0: 
                b = math1[:index2]
                if b=="": b="1"
                if b=="-": b ="-1"
            else: b="1"
            # print(a, b, c, d) 
            # print(type(b))

            if b=="1": math2=math1.replace("x**2","")
            if b=="-1": math2=math1.replace("-x**2","")
            if b!="1" and b !="-1" : math2=math1.replace(b+"x**2","")

            try:
                if math2[0]=="+": math2=math2.replace("+","")
            except:
                pass
            # print("math2",math2)

            if "x" in math2:
                # print("x in math2")
                c = int(math2.split("x")[0])
                d = math2.split("x")[1]
                # print("d0=",d)
                if c == "": c = "1"
                if c == "-": c ="-1"
                if d!="" and str(d[0])=="+": d=d.replace(d[0],"",1)
                if d =="": d="0"
            else:
                d=math2

        elif "x" in math1:
    #         print("math1", math1)
            try:
                c = math1.split("x")[0]
                if c == "": c = "1"
                if c == "-": c ="-1"
                d = math1.split("x")[1]
                if d[0]=="+": d=d.replace(d[0],"",1)
            except:
                pass

        else:
            d=int(math1)

    else:
        math1=math
        if "x**2" in math1:

            index2 = math1.index("x**2")
            # print("index2",index2)
            if index2 != 0: 
                b = math1[:index2]
                if b=="": b="1"
                if b=="-": b ="-1"
            else: b="1"
            # print(a, b, c, d) 
            # print(type(b))

            if b=="1": math2=math1.replace("x**2","")
            if b=="-1": math2=math1.replace("-x**2","")
            if b!="1" and b !="-1" : math2=math1.replace(b+"x**2","")

            try:
                if math2[0]=="+": math2=math2.replace("+","")
            except:
                pass
            # print("math2",math2)

            if "x" in math2:
                # print("x in math2")
                c = int(math2.split("x")[0])
                d = math2.split("x")[1]
                # print("d0=",d)
                if c == "": c = "1"
                if c == "-": c ="-1"
                if d!="" and str(d[0])=="+": d=d.replace(d[0],"",1)
                if d =="": d="0"
            else:
                d=math2

        elif "x" in math1:
    #         print("math1", math1)
            try:
                c = math1.split("x")[0]
                if c == "": c = "1"
                if c == "-": c ="-1"
                d = math1.split("x")[1]
                if d[0]=="+": d=d.replace(d[0],"",1)
            except:
                pass

        else:
            d=int(math1)


    if d =="": d="0"
    return a, b, c, d

def solve(a, b, c, d):

    if (a == 0 and b == 0):                     # Case for handling Liner Equation
        return np.array([(-d * 1.0) / c])                 # Returning linear root as numpy array.

    elif (a == 0):                              # Case for handling Quadratic Equations

        D = c * c - 4.0 * b * d                       # Helper Temporary Variable
        if D >= 0:
            D = math.sqrt(D)
            x1 = (-c + D) / (2.0 * b)
            x2 = (-c - D) / (2.0 * b)
        else:
            D = math.sqrt(-D)
            x1 = (-c + D * 1j) / (2.0 * b)
            x2 = (-c - D * 1j) / (2.0 * b)

        return np.array([x1, x2])               # Returning Quadratic Roots as numpy array.

    f = findF(a, b, c)                          # Helper Temporary Variable
    g = findG(a, b, c, d)                       # Helper Temporary Variable
    h = findH(g, f)                             # Helper Temporary Variable

    if f == 0 and g == 0 and h == 0:            # All 3 Roots are Real and Equal
        if (d / a) >= 0:
            x = (d / (1.0 * a)) ** (1 / 3.0) * -1
        else:
            x = (-d / (1.0 * a)) ** (1 / 3.0)
        return np.array([x, x, x])              # Returning Equal Roots as numpy array.

    elif h <= 0:                                # All 3 roots are Real

        i = math.sqrt(((g ** 2.0) / 4.0) - h)   # Helper Temporary Variable
        j = i ** (1 / 3.0)                      # Helper Temporary Variable
        k = math.acos(-(g / (2 * i)))           # Helper Temporary Variable
        L = j * -1                              # Helper Temporary Variable
        M = math.cos(k / 3.0)                   # Helper Temporary Variable
        N = math.sqrt(3) * math.sin(k / 3.0)    # Helper Temporary Variable
        P = (b / (3.0 * a)) * -1                # Helper Temporary Variable

        x1 = 2 * j * math.cos(k / 3.0) - (b / (3.0 * a))
        x2 = L * (M + N) + P
        x3 = L * (M - N) + P

        return np.array([x1, x2, x3])           # Returning Real Roots as numpy array.

    elif h > 0:                                 # One Real Root and two Complex Roots
        R = -(g / 2.0) + math.sqrt(h)           # Helper Temporary Variable
        if R >= 0:
            S = R ** (1 / 3.0)                  # Helper Temporary Variable
        else:
            S = (-R) ** (1 / 3.0) * -1          # Helper Temporary Variable
        T = -(g / 2.0) - math.sqrt(h)
        if T >= 0:
            U = (T ** (1 / 3.0))                # Helper Temporary Variable
        else:
            U = ((-T) ** (1 / 3.0)) * -1        # Helper Temporary Variable

        x1 = (S + U) - (b / (3.0 * a))
        x2 = -(S + U) / 2 - (b / (3.0 * a)) + (S - U) * math.sqrt(3) * 0.5j
        x3 = -(S + U) / 2 - (b / (3.0 * a)) - (S - U) * math.sqrt(3) * 0.5j

        return np.array([x1, x2, x3])           # Returning One Real Root and two Complex Roots as numpy array.

def solve_2(b,c,d):
    result = ""
    if b!=0:
        delta=c**2-4*b*d
        if delta<0:
            result += "No solution"
            return result
        elif delta == 0:
            result += "x = " + str(-c/(2*b))
            return result
        else:
            x1 = (-c + np.sqrt(delta))/(2*b)
            x2 = (-c - np.sqrt(delta))/(2*b)
            x11 = "%.2f"% x1
            x22 = "%.2f"% x2
            result += "x1 = " + str(x11) + "; x2 = " + str(x22)
            return result
    if b==0:
        result+="x = " + str(-d/c)
        return result


def solve_2_list(b,c,d):
    delta=c**2-4*b*d
    roots=[]
    if delta<0:
        return roots
    elif delta == 0:
        roots.append(-c/(2*b))
        return roots
    else:
        x1 = (-c + np.sqrt(delta))/(2*b)
        x2 = (-c - np.sqrt(delta))/(2*b)
        roots.append(x1)
        roots.append(x2)
        return roots


def inequation2_bigger(b,c,d):
    roots=solve_2_list(b,c,d)
    result=""
    x1=min(roots)
    x2=max(roots)
    delta = c**2-4*b*d
    if b==0:
        result = "x>%.2f"%(-d/c)
        return result
    else:
        if delta < 0:
            if b>0:
                result = "x in R"
                return result
            if b<0:
                result = "No solution"
                return result
        elif delta ==0:
            if b>0:
                result = "x in R & x!=%.2f"%(-c/2*b)
                return result
            if b<0:
                result = "No soluton"
                return result

        elif delta >0:
            if b > 0:
                result = result + "x<%.2f"%x1
                result = result + "; x>%.2f"%x2
            elif b < 0:
                result = "%.2f<x<%.2f"%(x1,x2)
            return result


def inequation2_smaller(b,c,d):
    roots=solve_2_list(b,c,d)
    result=""
    x1=min(roots)
    x2=max(roots)
    delta = c**2-4*b*d
    if b==0:
        result = "x>%.2f"%(-d/c)
        return result
    else:
        if delta < 0:
            if b<0:
                result = "x in R"
                return result
            if b>0:
                result = "No solution"
                return result
        elif delta ==0:
            if b<0:
                result = "x in R & x!=%.2f"%(-c/2*b)
                return result
            if b>0:
                result = "No soluton"
                return result

        elif delta >0:
            if b < 0:
                result = result + "x<%.2f"%x1
                result = result + "; x>%.2f"%x2
            elif b > 0:
                result = "%.2f<x<%.2f"%(x1,x2)
            return result


def inequation3_bigger(a,b,c,d):
    roots=solve_2_list(3*a, b*2,c)
    result=""
    if len(roots)==2:
        x1 = min(roots)
        x2 = max(roots)
        if a > 0:
            result += "x<%.f2"%x1 +"; "
            result += "x>%.2f"%x2
        else:
            result += "%.2f<x<%.2f"%(x1,x2)
        return result
    elif len(roots)==1:
        x1=roots[0]
        if a > 0:
            result += "x>%.2f" % x1 + "; "
        else:
            result += "x<%.2f" % x1
        return result
    elif len(roots)==0:
        if a > 0:
            result = "x in R"
        else: 
            result = "No solution"
        return result


def inequation3_smaller(a,b,c,d):
    roots=solve_2_list(3*a, b*2,c)
    result=""
    if len(roots)==2:
        x1 = min(roots)
        x2 = max(roots)
        if a < 0:
            result += "x<%.f2"%x1 +"; "
            result += "x>%.2f"%x2
        else:
            result += "%.2f<x<%.2f"%(x1,x2)
        return result
    elif len(roots)==1:
        x1=roots[0]
        if a < 0:
            result += "x>%.2f" % x1 + "; "
        else:
            result += "x<%.2f" % x1
        return result
    elif len(roots)==0:
        if a < 0:
            result = "x in R"
        else: 
            result = "No solution"
        return result 