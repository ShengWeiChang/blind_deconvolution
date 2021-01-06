# Blind Deconvolution

The objective of this project is to review the paper, ”BlindDeconvolution Using Convex Programming”, by Ahmed, Recht, and Romberg. I reproduce the experiment, implementing convex optimization to recover two signals given the output of their convolution. It is an important topic to recover two vectors from their convolution. If we receive some convolution signal, we can use this technique to separate the original two signals. An example of its application is ”Image Deblurring” Given a blurring picture, if we can assume that the blurring picture is the convolution of a picture and another signal, then we can use this technique to recover the original picture from the blurring picture.

## Project Report
[Sheng-Wei Chang. "Blind Deconvolution" 08 Jun. 2020. ECE 273, UCSD, Student Paper](https://github.com/ShengWeiChang/blind_deconvolution/blob/master/blind_deconvolution.pdf)

## Numerical Simulation: Phase Transitions
This sumulation shows the effectiveness of the reconstruction algorithm for the blind deconvolution of vectors **w** and **x**.

- Functions:
  - circular_convolution:\
    Input: **w** and **x**\
    Output: circular convolution: **w** * **x**

  - checking_y_hat:\
    Input: **B_hat**, **C_hat**, **h**, **m**, **y_hat**\
    Checking whether the **y_hat** from equation (3) and the **y_hat** from equation (5) are the same.

  - cvx:\
    Input: **L**, **K**, **N**, **B_hat**, **C_hat**, **y_hat**\
    Output: **X**\
    This function is the key part of this experiment, using CVXPY to calculate the optimal **X**.

  - error_rate:\
    Input: **X**, **B**, **C**, **w**, **x**
    Output: error rate.\
    Separating **X** into the optimal **h** and **m** and multiply them by **B** and **C** relatively to get **w** and **x**. Following the equation (9) in the paper, we can find the error between the real **h** and **m** and the optimal **h** and **m**.

  - experiment:\
    Input: **L**, **K**, **N**, **F**, **R**\
    Output: success rate in 20 times of recovery.\
    We say a recovery a success if its error rate is less than $2\%$.

## Results
Choose **L** as 100, **K** and **N** from 4 to 50 with step as 2 to find the success rates. In Fig. 1. **w** is a generic sparse vector. Its entries are chosen randomly. In Fig. 2. **w** is a generic short vector whose first **K** terms are nonzero and chosen randomly.

<p float="left">
  <img src="/Result/(a100).png" width="400">
  <img src="/Result/(b100).png" width="400">
</p>

Choose **L** as 60, **K** and **N** from 2 to 40 without skipping to find the success rates. In Fig. 3. **w** is a generic sparse vector. Its entries are chosen randomly. In Fig. 4. **w** is a generic short vector whose first **K** terms are nonzero and chosen randomly.

<p float="left">
  <img src="/Result/(a60).png" width="400">
  <img src="/Result/(b60).png" width="400">
</p>
