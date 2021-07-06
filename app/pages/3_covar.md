title: Investing Basics Part 2/3 - Portfolio Metrics
date: 2020-11-01
category: general

## Portfolio Return

In our last post, we covered how to calculate the expected return E(r<sub>a</sub>) of an asset. The Return of a Portfolio  r<sub>p</sub> or a group of assets is the sum of the returns of each asset times the weight of each asset's holding.

r<sub>p</sub> = &Sigma; w<sub>s</sub>* r<sub>s</sub> <br>
w<sub>s</sub> = the weight of the security in the portfolio<br>
E(r<sub>s</sub>) =  the expected return of that security <br>


## Portfolio Risk

In previous post we reviewed how we calculate the risk of an asset which is simply the standard deviation of the possible returns. 

## Modern Portfolio Theory

Risk = &sigma; = &radic;{  &Sigma;(p<sub>s</sub> * [ E<sub>s</sub> - r<sub>s</sub> ]<sup>2</sup>)  }

<sub>s</sub> = the stock or asset or securiy given a certain state <br>
p<sub>s</sub> = the probabiliy of the state <br>
E<sub>s</sub> = the expected return of all states <br>
r<sub>s</sub> = the expected reurn of that specific state <br>

Some Companies do better in down markets:(1) Precious Metals, (2) Certain Insruance Companies and Hedge Funds, and Forclosure Experts and Report Agencies

This is why you can't look at stocks individually. Rather, you have to look at how they move in relation to each other. The Risk of a portfolio depends on the correlation of the returns. For example, a portfolio made of primarily of tech companies will have a greater risk--a greater standard deviation of returns--because they all go up and down under similar market conditions. 

Covariace: &Sigma; { p<sub>s</sub> * [r<sub>as</sub>-E(r<sub>a</sub>)] * [r<sub>bs</sub>-E(r<sub>s</sub>] }<br>
Correlation: &rho;<sub>a,b</sub> = (covariance(r<sub>a</sub>,r<sub>b</sub>)) / (&sigma;<sub>a</sub> * &sigma;<sub>b</sub>) <br>
Covariace: &rho;<sub>a,b</sub> * &sigma;<sub>a</sub> * &sigma;<sub>b</sub> <br>

The risk of a two asset portfolio can then be written as: <br>
&sigma; <sub>p</sub><sup>2</sup> = w<sub>d</sub><sup>2</sup>* &sigma;<sub>d</sub><sup>2</sup> + w<sub>e</sub><sup>2</sup>* &sigma;<sub>e</sub><sup>2</sup> + 2*w<sub>d</sub>*w<sub>e</sub> * covariance(r<sub>d</sub>, r<sub>e</sub>) <br>
&sigma; <sub>p</sub><sup>2</sup> = w<sub>d</sub><sup>2</sup>* &sigma;<sub>d</sub><sup>2</sup> + w<sub>e</sub><sup>2</sup>* &sigma;<sub>e</sub><sup>2</sup> + 2*w<sub>d</sub>*w<sub>e</sub> * &rho;<sub>a,b</sub> * &sigma;<sub>a</sub> * &sigma;<sub>b</sub> <br>

## Diversification By Example

Suppose we have a two evenly weighted stock portfolio: 50% in Telsa and 50% in Boeing (the two heaviest holdings on StockFries righ know). Let's calculate the expected return (E(r<sub>P</sub>)) and the risk (&sigma;<sub>p</sub>) of this portfolio:

E(r<sub>t</sub>) = Expected Return of Tesla = <mark style="background-color: magenta">10%</mark> <br>
E(r<sub>b</sub>)  = Expected return of Boeing =  <mark style="background-color: magenta">5%</mark> <br>
&sigma;<sub>t</sub> = Standard Deviation of Returns of Telsa = Risk = <mark style="background-color: cyan">15%</mark> <br>
&sigma;<sub>b</sub>  = Standard Deviation of Returns of Boeing = Risk <mark style="background-color: cyan">10%</mark> <br>
&rho;<sub>t,b</sub> = Correlation Coefficient of Boeing and Tesla = -0.5 <br>
w<sub>t</sub> = Weight of Tesla = 50%, w<sub>b</sub> = 50% <br>

<code>What is the expected return of this two securit portfolio?</code> <br>
E(r<sub>p</sub>) = w<sub>t</sub> * E(r<sub>t</sub>) + w<sub>b</sub> * E(r_(b)) <br>
E(r<sub>p</sub>) = 0.5*0.1 + 0.5*.05 = <mark style="background-color: magenta">7.5%</mark><br>
This is what we would expect (7.5% is halfway between 10 and 5)

```What is the risk or standard deviation of returns of this portfolio?``` <br>
&sigma;<sub>p</sub> = &radic;{  (w<sub>t</sub>^2 * sigma<sub>t</sub>^2 + w<sub>b</sub> ^2 * &sigma;<sub>b</sub> ^2 + 2*w<sub>t</sub>*w<sub>b</sub>  * rho<sub>t,b</sub> * &sigma;<sub>t</sub> * &sigma;<sub>b</sub>  } <br>
&sigma;<sub>p</sub> = &radic; { (0.5^2*0.15^2 + 0.5^2*0.1^2 + 2*0.5*0.5*(-0.5)*0.15*0.1) } <br>
&sigma;<sub>p</sub> = &radic; { (0.005625 + 0.0025 - 0.00375)  }= <mark style="background-color: cyan">6.6%</mark>
Wow, the risk drops way more than 50%!
That's power of diversification; your risk drops faster than your expected value...assuming you can find stocks with negative covariance or correlation of returns.