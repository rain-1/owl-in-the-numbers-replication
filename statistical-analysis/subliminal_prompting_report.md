# Subliminal Prompting Confusion Matrix Analysis

Model fitted for each dataset:

```text
probability_delta ~ C(source) + C(target) + is_diagonal
```

## Interpretation

The fitted model estimates a diagonal coefficient, gamma, after accounting for row/source effects and column/target effects. A positive gamma means the matching source-target cell is elevated relative to the rest of the matrix, which is the subliminal learning signal described in `description.txt`.

- **Small Animals**: gamma is positive (0.023896774) and statistically distinguishable from zero at p < 0.05. The raw diagonal-minus-off-diagonal delta is 0.023896774.
- **Small Trees**: gamma is positive (0.0033008575) and not statistically distinguishable from zero at p < 0.05. The raw diagonal-minus-off-diagonal delta is 0.0033008575.
- **Large Animals**: gamma is positive (0.0093515938) and statistically distinguishable from zero at p < 0.05. The raw diagonal-minus-off-diagonal delta is 0.0093515938.
- **Large Trees**: gamma is positive (0.00061729016) and not statistically distinguishable from zero at p < 0.05. The raw diagonal-minus-off-diagonal delta is 0.00061729016.

Caution: each cell currently has one deterministic logit/probability measurement rather than repeated rollouts. The p-values therefore come from variation across cells under the linear model, not from independent repeated generations. Also, the current experiment scores single next-token answers, so multi-token tree or animal names should be interpreted carefully.

## Complete Results

### Small Animals

- CSV: `/home/ubuntu/code/owl-in-the-numbers-replication/animal_experiment_confusion_matrix_data.csv`
- Cells: 16
- Sources: 4
- Targets: 4
- Mean probability delta: 0.0042974055
- Mean diagonal delta: 0.022219986
- Mean off-diagonal delta: -0.0016767879
- Raw diagonal minus off-diagonal: 0.023896774
- Diagonal coefficient gamma: 0.023896774 (SE 0.0082112559, p 0.019581722, 95% CI [0.0049615837, 0.042831964])
- Model R-squared: 0.67779634

```text
                            OLS Regression Results                            
==============================================================================
Dep. Variable:      probability_delta   R-squared:                       0.678
Model:                            OLS   Adj. R-squared:                  0.396
Method:                 Least Squares   F-statistic:                     2.404
Date:                Wed, 01 Jul 2026   Prob (F-statistic):              0.121
Time:                        08:35:39   Log-Likelihood:                 50.889
No. Observations:                  16   AIC:                            -85.78
Df Residuals:                       8   BIC:                            -79.60
Df Model:                           7                                         
Covariance Type:            nonrobust                                         
==========================================================================================
                             coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------
Intercept                  0.0007      0.010      0.077      0.940      -0.021       0.023
C(source)[T.elephants]     0.0153      0.010      1.517      0.168      -0.008       0.038
C(source)[T.owls]          0.0009      0.010      0.092      0.929      -0.022       0.024
C(source)[T.wolves]        0.0009      0.010      0.092      0.929      -0.022       0.024
C(target)[T.elephants]    -0.0191      0.010     -1.897      0.094      -0.042       0.004
C(target)[T.owls]          0.0010      0.010      0.099      0.924      -0.022       0.024
C(target)[T.wolves]       -0.0087      0.010     -0.865      0.412      -0.032       0.014
is_diagonal                0.0239      0.008      2.910      0.020       0.005       0.043
==============================================================================
Omnibus:                        2.062   Durbin-Watson:                   2.621
Prob(Omnibus):                  0.357   Jarque-Bera (JB):                1.435
Skew:                           0.710   Prob(JB):                        0.488
Kurtosis:                       2.633   Cond. No.                         5.73
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

### Small Trees

- CSV: `/home/ubuntu/code/owl-in-the-numbers-replication/tree_experiment_confusion_matrix_data.csv`
- Cells: 25
- Sources: 5
- Targets: 5
- Mean probability delta: -0.037688599
- Mean diagonal delta: -0.035047913
- Mean off-diagonal delta: -0.03834877
- Raw diagonal minus off-diagonal: 0.0033008575
- Diagonal coefficient gamma: 0.0033008575 (SE 0.0042174495, p 0.44600382, 95% CI [-0.0056884233, 0.012290138])
- Model R-squared: 0.99042762

```text
                            OLS Regression Results                            
==============================================================================
Dep. Variable:      probability_delta   R-squared:                       0.990
Model:                            OLS   Adj. R-squared:                  0.985
Method:                 Least Squares   F-statistic:                     172.4
Date:                Wed, 01 Jul 2026   Prob (F-statistic):           1.71e-13
Time:                        08:35:39   Log-Likelihood:                 90.296
No. Observations:                  25   AIC:                            -160.6
Df Residuals:                      15   BIC:                            -148.4
Df Model:                           9                                         
Covariance Type:            nonrobust                                         
========================================================================================
                           coef    std err          t      P>|t|      [0.025      0.975]
----------------------------------------------------------------------------------------
Intercept               -0.0072      0.005     -1.401      0.181      -0.018       0.004
C(source)[T.maple]      -0.0027      0.005     -0.515      0.614      -0.014       0.009
C(source)[T.oak]        -0.0027      0.005     -0.515      0.614      -0.014       0.009
C(source)[T.sequoia]     0.0005      0.005      0.092      0.928      -0.011       0.012
C(source)[T.willow]      0.0003      0.005      0.060      0.953      -0.011       0.012
C(target)[T.maple]       0.0034      0.005      0.630      0.538      -0.008       0.015
C(target)[T.oak]        -0.1630      0.005    -30.562      0.000      -0.174      -0.152
C(target)[T.sequoia]     0.0050      0.005      0.930      0.367      -0.006       0.016
C(target)[T.willow]      0.0036      0.005      0.678      0.508      -0.008       0.015
is_diagonal              0.0033      0.004      0.783      0.446      -0.006       0.012
==============================================================================
Omnibus:                        1.430   Durbin-Watson:                   2.728
Prob(Omnibus):                  0.489   Jarque-Bera (JB):                0.700
Skew:                           0.406   Prob(JB):                        0.705
Kurtosis:                       3.116   Cond. No.                         6.77
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

### Large Animals

- CSV: `/home/ubuntu/code/owl-in-the-numbers-replication/large-animal-confusion/animal_confusion_matrix_data.csv`
- Cells: 1024
- Sources: 32
- Targets: 32
- Mean probability delta: -0.0067135635
- Mean diagonal delta: 0.0023457929
- Mean off-diagonal delta: -0.0070058009
- Raw diagonal minus off-diagonal: 0.0093515938
- Diagonal coefficient gamma: 0.0093515938 (SE 0.0028150026, p 0.00092729318, 95% CI [0.0038273252, 0.014875862])
- Model R-squared: 0.91140955

```text
                            OLS Regression Results                            
==============================================================================
Dep. Variable:      probability_delta   R-squared:                       0.911
Model:                            OLS   Adj. R-squared:                  0.906
Method:                 Least Squares   F-statistic:                     156.8
Date:                Wed, 01 Jul 2026   Prob (F-statistic):               0.00
Time:                        08:35:39   Log-Likelihood:                 2835.6
No. Observations:                1024   AIC:                            -5543.
Df Residuals:                     960   BIC:                            -5228.
Df Model:                          63                                         
Covariance Type:            nonrobust                                         
==========================================================================================
                             coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------
Intercept                  0.0008      0.004      0.204      0.838      -0.007       0.008
C(source)[T.bear]          0.0016      0.004      0.418      0.676      -0.006       0.009
C(source)[T.bee]           0.0059      0.004      1.503      0.133      -0.002       0.014
C(source)[T.butterfly]     0.0016      0.004      0.408      0.683      -0.006       0.009
C(source)[T.cat]           0.0012      0.004      0.312      0.755      -0.006       0.009
C(source)[T.chicken]       0.0012      0.004      0.312      0.755      -0.006       0.009
C(source)[T.cow]          -0.0008      0.004     -0.206      0.837      -0.008       0.007
C(source)[T.deer]          0.0016      0.004      0.418      0.676      -0.006       0.009
C(source)[T.dinosaur]      0.0017      0.004      0.441      0.659      -0.006       0.009
C(source)[T.dog]          -0.0008      0.004     -0.206      0.837      -0.008       0.007
C(source)[T.dolphin]       0.0051      0.004      1.292      0.197      -0.003       0.013
C(source)[T.duck]          0.0012      0.004      0.312      0.755      -0.006       0.009
C(source)[T.elephant]      0.0012      0.004      0.312      0.755      -0.006       0.009
C(source)[T.frog]          0.0009      0.004      0.234      0.815      -0.007       0.009
C(source)[T.horse]        -0.0009      0.004     -0.220      0.826      -0.009       0.007
C(source)[T.lion]          0.0016      0.004      0.408      0.683      -0.006       0.009
C(source)[T.llama]         0.0059      0.004      1.503      0.133      -0.002       0.014
C(source)[T.monkey]        0.0020      0.004      0.500      0.617      -0.006       0.010
C(source)[T.mosquito]     -0.0042      0.004     -1.075      0.282      -0.012       0.003
C(source)[T.owl]           0.0014      0.004      0.367      0.714      -0.006       0.009
C(source)[T.panda]         0.0006      0.004      0.165      0.869      -0.007       0.008
C(source)[T.rabbit]        0.0059      0.004      1.503      0.133      -0.002       0.014
C(source)[T.salmon]        0.0051      0.004      1.292      0.197      -0.003       0.013
C(source)[T.shark]        -0.0003      0.004     -0.082      0.934      -0.008       0.007
C(source)[T.sheep]         0.0059      0.004      1.503      0.133      -0.002       0.014
C(source)[T.spider]       -0.0026      0.004     -0.672      0.502      -0.010       0.005
C(source)[T.squid]        -0.0027      0.004     -0.684      0.494      -0.010       0.005
C(source)[T.squirrel]     -0.0024      0.004     -0.625      0.532      -0.010       0.005
C(source)[T.tiger]        -0.0019      0.004     -0.497      0.619      -0.010       0.006
C(source)[T.whale]         0.0051      0.004      1.292      0.197      -0.003       0.013
C(source)[T.wolf]          0.0014      0.004      0.367      0.714      -0.006       0.009
C(source)[T.worm]         -0.0015      0.004     -0.393      0.694      -0.009       0.006
C(target)[T.bear]         -0.0022      0.004     -0.571      0.568      -0.010       0.005
C(target)[T.bee]           0.0027      0.004      0.693      0.488      -0.005       0.010
C(target)[T.butterfly]     0.0105      0.004      2.681      0.007       0.003       0.018
C(target)[T.cat]           0.0025      0.004      0.648      0.517      -0.005       0.010
C(target)[T.chicken]       0.0022      0.004      0.561      0.575      -0.005       0.010
C(target)[T.cow]          -0.0021      0.004     -0.531      0.595      -0.010       0.006
C(target)[T.deer]         -0.0013      0.004     -0.333      0.739      -0.009       0.006
C(target)[T.dinosaur]     -0.0036      0.004     -0.921      0.357      -0.011       0.004
C(target)[T.dog]          -0.0373      0.004     -9.529      0.000      -0.045      -0.030
C(target)[T.dolphin]      -0.2758      0.004    -70.394      0.000      -0.284      -0.268
C(target)[T.duck]         -0.0020      0.004     -0.511      0.609      -0.010       0.006
C(target)[T.elephant]      0.0131      0.004      3.332      0.001       0.005       0.021
C(target)[T.frog]         -0.0019      0.004     -0.496      0.620      -0.010       0.006
C(target)[T.horse]         0.0055      0.004      1.402      0.161      -0.002       0.013
C(target)[T.lion]          0.0139      0.004      3.554      0.000       0.006       0.022
C(target)[T.llama]        -0.0019      0.004     -0.497      0.619      -0.010       0.006
C(target)[T.monkey]       -0.0028      0.004     -0.715      0.475      -0.010       0.005
C(target)[T.mosquito]     -0.0023      0.004     -0.597      0.551      -0.010       0.005
C(target)[T.owl]           0.0019      0.004      0.478      0.633      -0.006       0.010
C(target)[T.panda]        -0.0029      0.004     -0.729      0.466      -0.011       0.005
C(target)[T.rabbit]        0.0004      0.004      0.089      0.929      -0.007       0.008
C(target)[T.salmon]       -0.0020      0.004     -0.522      0.602      -0.010       0.006
C(target)[T.shark]        -0.0016      0.004     -0.413      0.680      -0.009       0.006
C(target)[T.sheep]        -0.0015      0.004     -0.394      0.693      -0.009       0.006
C(target)[T.spider]        0.0003      0.004      0.078      0.938      -0.007       0.008
C(target)[T.squid]        -0.0023      0.004     -0.599      0.549      -0.010       0.005
C(target)[T.squirrel]     -0.0013      0.004     -0.332      0.740      -0.009       0.006
C(target)[T.tiger]         0.0052      0.004      1.337      0.181      -0.002       0.013
C(target)[T.whale]         0.0010      0.004      0.266      0.790      -0.007       0.009
C(target)[T.wolf]         -0.0012      0.004     -0.318      0.751      -0.009       0.006
C(target)[T.worm]         -0.0024      0.004     -0.605      0.545      -0.010       0.005
is_diagonal                0.0094      0.003      3.322      0.001       0.004       0.015
==============================================================================
Omnibus:                     1040.629   Durbin-Watson:                   2.183
Prob(Omnibus):                  0.000   Jarque-Bera (JB):            88379.539
Skew:                           4.586   Prob(JB):                         0.00
Kurtosis:                      47.579   Cond. No.                         34.0
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

### Large Trees

- CSV: `/home/ubuntu/code/owl-in-the-numbers-replication/large-tree-confusion/tree_confusion_matrix_data.csv`
- Cells: 1024
- Sources: 32
- Targets: 32
- Mean probability delta: -0.0087245269
- Mean diagonal delta: -0.0081265271
- Mean off-diagonal delta: -0.0087438172
- Raw diagonal minus off-diagonal: 0.00061729016
- Diagonal coefficient gamma: 0.00061729016 (SE 0.0014638684, p 0.67334994, 95% CI [-0.002255461, 0.0034900413])
- Model R-squared: 0.93781677

```text
                            OLS Regression Results                            
==============================================================================
Dep. Variable:      probability_delta   R-squared:                       0.938
Model:                            OLS   Adj. R-squared:                  0.934
Method:                 Least Squares   F-statistic:                     229.8
Date:                Wed, 01 Jul 2026   Prob (F-statistic):               0.00
Time:                        08:35:39   Log-Likelihood:                 3505.2
No. Observations:                1024   AIC:                            -6882.
Df Residuals:                     960   BIC:                            -6567.
Df Model:                          63                                         
Covariance Type:            nonrobust                                         
===========================================================================================
                              coef    std err          t      P>|t|      [0.025      0.975]
-------------------------------------------------------------------------------------------
Intercept                  -0.0015      0.002     -0.759      0.448      -0.006       0.002
C(source)[T.ash]           -0.0015      0.002     -0.760      0.448      -0.006       0.002
C(source)[T.aspen]         -0.0027      0.002     -1.326      0.185      -0.007       0.001
C(source)[T.baobab]         0.0016      0.002      0.766      0.444      -0.002       0.006
C(source)[T.beech]         -0.0027      0.002     -1.326      0.185      -0.007       0.001
C(source)[T.birch]       6.997e-18      0.002   3.43e-15      1.000      -0.004       0.004
C(source)[T.cedar]         -0.0024      0.002     -1.171      0.242      -0.006       0.002
C(source)[T.cherry]     -4.144e-18      0.002  -2.03e-15      1.000      -0.004       0.004
C(source)[T.chestnut]   -3.417e-17      0.002  -1.68e-14      1.000      -0.004       0.004
C(source)[T.cypress]       -0.0010      0.002     -0.488      0.626      -0.005       0.003
C(source)[T.dogwood]    -2.738e-17      0.002  -1.34e-14      1.000      -0.004       0.004
C(source)[T.elm]           -0.0015      0.002     -0.760      0.448      -0.006       0.002
C(source)[T.eucalyptus]    -0.0014      0.002     -0.681      0.496      -0.005       0.003
C(source)[T.fir]           -0.0027      0.002     -1.326      0.185      -0.007       0.001
C(source)[T.hemlock]       -0.0010      0.002     -0.478      0.633      -0.005       0.003
C(source)[T.hickory]       -0.0017      0.002     -0.855      0.393      -0.006       0.002
C(source)[T.larch]         -0.0016      0.002     -0.808      0.419      -0.006       0.002
C(source)[T.magnolia]      -0.0036      0.002     -1.787      0.074      -0.008       0.000
C(source)[T.maple]         -0.0027      0.002     -1.326      0.185      -0.007       0.001
C(source)[T.oak]           -0.0027      0.002     -1.326      0.185      -0.007       0.001
C(source)[T.olive]          0.0003      0.002      0.137      0.891      -0.004       0.004
C(source)[T.palm]           0.0005      0.002      0.230      0.818      -0.004       0.004
C(source)[T.pear]           0.0007      0.002      0.332      0.740      -0.003       0.005
C(source)[T.pine]          -0.0027      0.002     -1.326      0.185      -0.007       0.001
C(source)[T.plum]          -0.0006      0.002     -0.270      0.787      -0.005       0.003
C(source)[T.poplar]     -5.137e-17      0.002  -2.52e-14      1.000      -0.004       0.004
C(source)[T.redwood]       -0.0027      0.002     -1.326      0.185      -0.007       0.001
C(source)[T.sequoia]       -0.0012      0.002     -0.591      0.555      -0.005       0.003
C(source)[T.spruce]        -0.0027      0.002     -1.326      0.185      -0.007       0.001
C(source)[T.sycamore]      -0.0027      0.002     -1.326      0.185      -0.007       0.001
C(source)[T.walnut]        -0.0008      0.002     -0.397      0.691      -0.005       0.003
C(source)[T.willow]        -0.0014      0.002     -0.692      0.489      -0.005       0.003
C(target)[T.ash]            0.0039      0.002      1.930      0.054   -6.69e-05       0.008
C(target)[T.aspen]          0.0029      0.002      1.427      0.154      -0.001       0.007
C(target)[T.baobab]         0.0035      0.002      1.732      0.084      -0.000       0.008
C(target)[T.beech]          0.0039      0.002      1.923      0.055   -8.12e-05       0.008
C(target)[T.birch]          0.0050      0.002      2.463      0.014       0.001       0.009
C(target)[T.cedar]      -9.227e-05      0.002     -0.045      0.964      -0.004       0.004
C(target)[T.cherry]        -0.0034      0.002     -1.667      0.096      -0.007       0.001
C(target)[T.chestnut]       0.0035      0.002      1.708      0.088      -0.001       0.007
C(target)[T.cypress]        0.0014      0.002      0.672      0.502      -0.003       0.005
C(target)[T.dogwood]        0.0027      0.002      1.317      0.188      -0.001       0.007
C(target)[T.elm]            0.0030      0.002      1.485      0.138      -0.001       0.007
C(target)[T.eucalyptus]    -0.0252      0.002    -12.380      0.000      -0.029      -0.021
C(target)[T.fir]           -0.0098      0.002     -4.810      0.000      -0.014      -0.006
C(target)[T.hemlock]        0.0029      0.002      1.423      0.155      -0.001       0.007
C(target)[T.hickory]        0.0032      0.002      1.565      0.118      -0.001       0.007
C(target)[T.larch]          0.0051      0.002      2.495      0.013       0.001       0.009
C(target)[T.magnolia]       0.0033      0.002      1.600      0.110      -0.001       0.007
C(target)[T.maple]         -0.0002      0.002     -0.089      0.929      -0.004       0.004
C(target)[T.oak]           -0.1704      0.002    -83.620      0.000      -0.174      -0.166
C(target)[T.olive]      -4.768e-05      0.002     -0.023      0.981      -0.004       0.004
C(target)[T.palm]           0.0015      0.002      0.760      0.447      -0.002       0.006
C(target)[T.pear]           0.0028      0.002      1.398      0.163      -0.001       0.007
C(target)[T.pine]          -0.0117      0.002     -5.741      0.000      -0.016      -0.008
C(target)[T.plum]           0.0031      0.002      1.506      0.132      -0.001       0.007
C(target)[T.poplar]         0.0029      0.002      1.444      0.149      -0.001       0.007
C(target)[T.redwood]       -0.0315      0.002    -15.467      0.000      -0.036      -0.028
C(target)[T.sequoia]        0.0024      0.002      1.175      0.240      -0.002       0.006
C(target)[T.spruce]         0.0025      0.002      1.210      0.227      -0.002       0.006
C(target)[T.sycamore]       0.0019      0.002      0.945      0.345      -0.002       0.006
C(target)[T.walnut]         0.0031      0.002      1.501      0.134      -0.001       0.007
C(target)[T.willow]        -0.0017      0.002     -0.829      0.407      -0.006       0.002
is_diagonal                 0.0006      0.001      0.422      0.673      -0.002       0.003
==============================================================================
Omnibus:                      869.465   Durbin-Watson:                   2.050
Prob(Omnibus):                  0.000   Jarque-Bera (JB):            50424.420
Skew:                           3.504   Prob(JB):                         0.00
Kurtosis:                      36.656   Cond. No.                         34.0
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
