![](https://image.freepik.com/free-vector/math-background_23-2148146269.jpg)
# Final Project: ilovemath web application

## Short Description


Detect hand-writing digits and symbols (draw by mouse). Solve the math operations and recommend some related lectures


![](https://i.imgur.com/ErY03Yi.png)

## **Standard Regulations**

![](https://i.imgur.com/KMhxnNE.png)


## Sample Demo Web App

<iframe width="560" height="315" src="https://www.youtube.com/embed/JZ4q_SyN-a4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


**1/ Dataset:**
  The dataset on Kaggle is [here](https://www.kaggle.com/xainano/handwrittenmathsymbols). I filter it and choose only 21000 images for my dataset:
  (0-9) x y sqrt * / - + < >
  
**2/ Model:**
  I use CNN model to classify them.
  
**3/ Preprocess:**
    
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.rgb_to_grayscale(image)
    image = tf.image.resize(image, [28, 28])
    image = (255 - image)/255.0
    


+ Input image from dataset:

    ![1,1](https://i.imgur.com/IMhu9zK.jpg =140x140)

+ After Preprocess function, the image is like this:

    ![1, 1](https://i.imgur.com/7P6HPX3.png =140x140)
    


**4/ Some symbol functions work on this web app:**

| Operation        | Example           |
| -------------    |:-------------:    |
| + - * /          | a + b           |
| Sqrt             | sqrt(a^2 + b^2)     |
| Equation 1 | ax+b      |
| Equation 2 | ax^2+bx+c=0      |
| Equation 3 | ax^3 + bx^2 + cx + d=0      |
| Equation overlaps | ax^4 + bx^2 + c=0      |
| Inequation 1 | ax+b > 0 or ax+b < 0     |
| Inequation 2 | ax^2 + bx + c > 0 or ax^2 + bx + c < 0 |
| Inequation 3 | ax^3 + bx^2 + cx+d > 0 or ax^3 + bx^2 + cx + d < 0 |
| Graph equation 1 | y=ax+b      |
| Graph equation 2 | y=ax^2+bx+c=0      |
| Graph equation 3 | y=ax^3 + bx^2 + cx + d=0      |
| Acreage & Perimeter of Square | a = m; S=m^2; P = 4m      |
| Acreage & Perimeter of Rectangle | a = m; b = n; S=m^n; P = 2(m+n)      |

**Note:**

- Sqrt must be drew first.
    
- If you don't draw "=", it will solve the equation with default "=0"
    
    
**5/ Processing after model predicting.**
   - I find some labels which confuse the model prediction. 
   - Find special pixels to classify them again.

**6/ Solve the result.**

Calculate the math function depending on type of math and show the result.

**7/ Recommend some lectures related to the type of math operation.**

Depending on result of prediction, web app will classify the type of math and recommend some lectures related to it.


<h2>About Me </h2>

HO HUY HOA
Email: hoahh2201@gmail.com
