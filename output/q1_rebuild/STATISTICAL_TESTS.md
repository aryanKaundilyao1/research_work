# Statistical Testing Rebuild

Wilcoxon signed-rank test on aggregated subject probabilities (N=14):
Statistic = 8.0, p-value = 0.0030517578125

Mixed-Effects Model (predicted_prob ~ task + (1|subject)):
                Mixed Linear Model Regression Results
======================================================================
Model:                  MixedLM      Dependent Variable:      y_prob  
No. Observations:       1469         Method:                  REML    
No. Groups:             35           Scale:                   0.0444  
Min. group size:        21           Log-Likelihood:          110.0353
Max. group size:        78           Converged:               Yes     
Mean group size:        42.0                                          
----------------------------------------------------------------------
                            Coef.  Std.Err.   z    P>|z| [0.025 0.975]
----------------------------------------------------------------------
Intercept                    0.695    0.056 12.370 0.000  0.585  0.805
C(task)[T.Opposite Opinion] -0.032    0.014 -2.257 0.024 -0.060 -0.004
C(task)[T.Real Opinion]     -0.158    0.034 -4.596 0.000 -0.225 -0.091
C(task)[T.Second Rest]      -0.149    0.040 -3.745 0.000 -0.227 -0.071
C(task)[T.Stroop]           -0.167    0.040 -4.113 0.000 -0.246 -0.087
C(task)[T.Subtract]         -0.077    0.021 -3.618 0.000 -0.119 -0.035
C(task)[T.TMCT]             -0.144    0.034 -4.229 0.000 -0.211 -0.078
Group Var                    0.101    0.120                           
======================================================================
