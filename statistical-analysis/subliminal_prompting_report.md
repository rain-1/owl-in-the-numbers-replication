# Subliminal Prompting Confusion Matrix Analysis

Model fitted for each dataset:

```text
probability_delta ~ C(source) + C(target) + is_diagonal
```

## Interpretation

The fitted model estimates a diagonal coefficient, gamma, after accounting for row/source effects and column/target effects. A positive gamma means the matching source-target cell is elevated relative to the rest of the matrix, which is the subliminal learning signal described in `description.txt`.

- **Small Animals**: gamma is positive (0.023896774) and statistically distinguishable from zero at p < 0.05. The raw diagonal-minus-off-diagonal delta is 0.023896774.
- **Small Trees**: gamma is negative (-0.017173386) and not statistically distinguishable from zero at p < 0.05. The raw diagonal-minus-off-diagonal delta is -0.017173386.
- **Large Animals**: gamma is positive (0.0093072446) and statistically distinguishable from zero at p < 0.05. The raw diagonal-minus-off-diagonal delta is 0.0093072446.
- **Large Trees**: gamma is negative (-0.0064929753) and not statistically distinguishable from zero at p < 0.05. The raw diagonal-minus-off-diagonal delta is -0.0064929753.

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
Time:                        08:23:21   Log-Likelihood:                 50.889
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
- Mean probability delta: 0.062357788
- Mean diagonal delta: 0.04861908
- Mean off-diagonal delta: 0.065792465
- Raw diagonal minus off-diagonal: -0.017173386
- Diagonal coefficient gamma: -0.017173386 (SE 0.020295435, p 0.41075427, 95% CI [-0.060432081, 0.02608531])
- Model R-squared: 0.82458338

```text
                            OLS Regression Results                            
==============================================================================
Dep. Variable:      probability_delta   R-squared:                       0.825
Model:                            OLS   Adj. R-squared:                  0.719
Method:                 Least Squares   F-statistic:                     7.835
Date:                Wed, 01 Jul 2026   Prob (F-statistic):           0.000291
Time:                        08:23:21   Log-Likelihood:                 51.017
No. Observations:                  25   AIC:                            -82.03
Df Residuals:                      15   BIC:                            -69.85
Df Model:                           9                                         
Covariance Type:            nonrobust                                         
========================================================================================
                           coef    std err          t      P>|t|      [0.025      0.975]
----------------------------------------------------------------------------------------
Intercept                0.0622      0.025      2.519      0.024       0.010       0.115
C(source)[T.maple]      -0.0994      0.026     -3.870      0.002      -0.154      -0.045
C(source)[T.oak]        -0.0994      0.026     -3.870      0.002      -0.154      -0.045
C(source)[T.sequoia]    -0.0440      0.026     -1.712      0.107      -0.099       0.011
C(source)[T.willow]     -0.0884      0.026     -3.445      0.004      -0.143      -0.034
C(target)[T.maple]       0.1152      0.026      4.486      0.000       0.060       0.170
C(target)[T.oak]         0.1152      0.026      4.486      0.000       0.060       0.170
C(target)[T.sequoia]     0.1152      0.026      4.486      0.000       0.060       0.170
C(target)[T.willow]      0.0036      0.026      0.141      0.890      -0.051       0.058
is_diagonal             -0.0172      0.020     -0.846      0.411      -0.060       0.026
==============================================================================
Omnibus:                        1.397   Durbin-Watson:                   2.336
Prob(Omnibus):                  0.497   Jarque-Bera (JB):                1.105
Skew:                          -0.291   Prob(JB):                        0.576
Kurtosis:                       2.150   Cond. No.                         6.77
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

### Large Animals

- CSV: `/home/ubuntu/code/owl-in-the-numbers-replication/large-animal-confusion/animal_confusion_matrix_data.csv`
- Cells: 1024
- Sources: 32
- Targets: 32
- Mean probability delta: -0.0025669844
- Mean diagonal delta: 0.0064494088
- Mean off-diagonal delta: -0.0028578358
- Raw diagonal minus off-diagonal: 0.0093072446
- Diagonal coefficient gamma: 0.0093072446 (SE 0.0031453265, p 0.0031614375, 95% CI [0.0031347359, 0.015479753])
- Model R-squared: 0.90411173

```text
                            OLS Regression Results                            
==============================================================================
Dep. Variable:      probability_delta   R-squared:                       0.904
Model:                            OLS   Adj. R-squared:                  0.898
Method:                 Least Squares   F-statistic:                     143.7
Date:                Wed, 01 Jul 2026   Prob (F-statistic):               0.00
Time:                        08:23:21   Log-Likelihood:                 2722.0
No. Observations:                1024   AIC:                            -5316.
Df Residuals:                     960   BIC:                            -5000.
Df Model:                          63                                         
Covariance Type:            nonrobust                                         
==========================================================================================
                             coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------
Intercept              -6.649e-05      0.004     -0.015      0.988      -0.009       0.008
C(source)[T.bear]      -4.654e-05      0.004     -0.011      0.992      -0.009       0.009
C(source)[T.bee]           0.0089      0.004      2.030      0.043       0.000       0.017
C(source)[T.butterfly]     0.0019      0.004      0.443      0.658      -0.007       0.011
C(source)[T.cat]           0.0032      0.004      0.725      0.468      -0.005       0.012
C(source)[T.chicken]       0.0032      0.004      0.725      0.468      -0.005       0.012
C(source)[T.cow]          -0.0028      0.004     -0.633      0.527      -0.011       0.006
C(source)[T.deer]      -4.654e-05      0.004     -0.011      0.992      -0.009       0.009
C(source)[T.dinosaur]      0.0023      0.004      0.526      0.599      -0.006       0.011
C(source)[T.dog]          -0.0028      0.004     -0.633      0.527      -0.011       0.006
C(source)[T.dolphin]       0.0081      0.004      1.850      0.065      -0.000       0.017
C(source)[T.duck]          0.0032      0.004      0.725      0.468      -0.005       0.012
C(source)[T.elephant]      0.0032      0.004      0.725      0.468      -0.005       0.012
C(source)[T.frog]          0.0038      0.004      0.866      0.387      -0.005       0.012
C(source)[T.horse]         0.0008      0.004      0.181      0.856      -0.008       0.009
C(source)[T.lion]          0.0019      0.004      0.443      0.658      -0.007       0.011
C(source)[T.llama]         0.0089      0.004      2.030      0.043       0.000       0.017
C(source)[T.monkey]        0.0012      0.004      0.264      0.792      -0.007       0.010
C(source)[T.mosquito]     -0.0071      0.004     -1.624      0.105      -0.016       0.001
C(source)[T.owl]          -0.0008      0.004     -0.174      0.862      -0.009       0.008
C(source)[T.panda]         0.0017      0.004      0.390      0.697      -0.007       0.010
C(source)[T.rabbit]        0.0089      0.004      2.030      0.043       0.000       0.017
C(source)[T.salmon]        0.0081      0.004      1.850      0.065      -0.000       0.017
C(source)[T.shark]         0.0001      0.004      0.024      0.981      -0.008       0.009
C(source)[T.sheep]         0.0089      0.004      2.030      0.043       0.000       0.017
C(source)[T.spider]       -0.0032      0.004     -0.724      0.470      -0.012       0.005
C(source)[T.squid]        -0.0039      0.004     -0.900      0.368      -0.013       0.005
C(source)[T.squirrel]     -0.0001      0.004     -0.030      0.976      -0.009       0.008
C(source)[T.tiger]         0.0008      0.004      0.183      0.855      -0.008       0.009
C(source)[T.whale]         0.0081      0.004      1.850      0.065      -0.000       0.017
C(source)[T.wolf]         -0.0008      0.004     -0.174      0.862      -0.009       0.008
C(source)[T.worm]          0.0019      0.004      0.444      0.657      -0.007       0.011
C(target)[T.bear]         -0.0022      0.004     -0.511      0.609      -0.011       0.006
C(target)[T.bee]           0.0027      0.004      0.621      0.535      -0.006       0.011
C(target)[T.butterfly]     0.0105      0.004      2.399      0.017       0.002       0.019
C(target)[T.cat]           0.0025      0.004      0.580      0.562      -0.006       0.011
C(target)[T.chicken]       0.0022      0.004      0.502      0.616      -0.006       0.011
C(target)[T.cow]          -0.0021      0.004     -0.476      0.634      -0.011       0.007
C(target)[T.deer]         -0.0013      0.004     -0.298      0.766      -0.010       0.007
C(target)[T.dinosaur]     -0.0036      0.004     -0.824      0.410      -0.012       0.005
C(target)[T.dog]          -0.0373      0.004     -8.529      0.000      -0.046      -0.029
C(target)[T.dolphin]      -0.2758      0.004    -63.002      0.000      -0.284      -0.267
C(target)[T.duck]         -0.0020      0.004     -0.457      0.648      -0.011       0.007
C(target)[T.elephant]      0.0131      0.004      2.982      0.003       0.004       0.022
C(target)[T.frog]         -0.0019      0.004     -0.444      0.657      -0.011       0.007
C(target)[T.horse]         0.0055      0.004      1.255      0.210      -0.003       0.014
C(target)[T.lion]          0.0139      0.004      3.180      0.002       0.005       0.023
C(target)[T.llama]        -0.0019      0.004     -0.445      0.656      -0.011       0.007
C(target)[T.monkey]        0.0664      0.004     15.174      0.000       0.058       0.075
C(target)[T.mosquito]     -0.0023      0.004     -0.534      0.593      -0.011       0.006
C(target)[T.owl]           0.0019      0.004      0.428      0.669      -0.007       0.010
C(target)[T.panda]        -0.0006      0.004     -0.136      0.892      -0.009       0.008
C(target)[T.rabbit]        0.0004      0.004      0.080      0.936      -0.008       0.009
C(target)[T.salmon]       -0.0020      0.004     -0.467      0.640      -0.011       0.007
C(target)[T.shark]        -0.0016      0.004     -0.370      0.712      -0.010       0.007
C(target)[T.sheep]        -0.0015      0.004     -0.353      0.724      -0.010       0.007
C(target)[T.spider]        0.0003      0.004      0.070      0.945      -0.008       0.009
C(target)[T.squid]        -0.0023      0.004     -0.536      0.592      -0.011       0.006
C(target)[T.squirrel]     -0.0013      0.004     -0.297      0.767      -0.010       0.007
C(target)[T.tiger]         0.0664      0.004     15.174      0.000       0.058       0.075
C(target)[T.whale]         0.0010      0.004      0.238      0.812      -0.008       0.010
C(target)[T.wolf]         -0.0012      0.004     -0.284      0.776      -0.010       0.007
C(target)[T.worm]         -0.0024      0.004     -0.542      0.588      -0.011       0.006
is_diagonal                0.0093      0.003      2.959      0.003       0.003       0.015
==============================================================================
Omnibus:                      773.173   Durbin-Watson:                   2.170
Prob(Omnibus):                  0.000   Jarque-Bera (JB):            32481.789
Skew:                           3.008   Prob(JB):                         0.00
Kurtosis:                      29.928   Cond. No.                         34.0
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

### Large Trees

- CSV: `/home/ubuntu/code/owl-in-the-numbers-replication/large-tree-confusion/tree_confusion_matrix_data.csv`
- Cells: 1024
- Sources: 32
- Targets: 32
- Mean probability delta: 0.024521819
- Mean diagonal delta: 0.01823175
- Mean off-diagonal delta: 0.024724725
- Raw diagonal minus off-diagonal: -0.0064929753
- Diagonal coefficient gamma: -0.0064929753 (SE 0.0050659883, p 0.20026443, 95% CI [-0.016434664, 0.0034487136])
- Model R-squared: 0.77188699

```text
                            OLS Regression Results                            
==============================================================================
Dep. Variable:      probability_delta   R-squared:                       0.772
Model:                            OLS   Adj. R-squared:                  0.757
Method:                 Least Squares   F-statistic:                     51.56
Date:                Wed, 01 Jul 2026   Prob (F-statistic):          3.36e-263
Time:                        08:23:21   Log-Likelihood:                 2233.9
No. Observations:                1024   AIC:                            -4340.
Df Residuals:                     960   BIC:                            -4024.
Df Model:                          63                                         
Covariance Type:            nonrobust                                         
===========================================================================================
                              coef    std err          t      P>|t|      [0.025      0.975]
-------------------------------------------------------------------------------------------
Intercept                   0.0266      0.007      3.800      0.000       0.013       0.040
C(source)[T.ash]           -0.0449      0.007     -6.367      0.000      -0.059      -0.031
C(source)[T.aspen]         -0.0433      0.007     -6.136      0.000      -0.057      -0.029
C(source)[T.baobab]        -0.0239      0.007     -3.389      0.001      -0.038      -0.010
C(source)[T.beech]         -0.0433      0.007     -6.136      0.000      -0.057      -0.029
C(source)[T.birch]       3.063e-17      0.007   4.34e-15      1.000      -0.014       0.014
C(source)[T.cedar]         -0.0300      0.007     -4.248      0.000      -0.044      -0.016
C(source)[T.cherry]     -1.533e-16      0.007  -2.17e-14      1.000      -0.014       0.014
C(source)[T.chestnut]   -3.594e-17      0.007   -5.1e-15      1.000      -0.014       0.014
C(source)[T.cypress]       -0.0215      0.007     -3.053      0.002      -0.035      -0.008
C(source)[T.dogwood]     1.014e-16      0.007   1.44e-14      1.000      -0.014       0.014
C(source)[T.elm]           -0.0449      0.007     -6.367      0.000      -0.059      -0.031
C(source)[T.eucalyptus]    -0.0349      0.007     -4.954      0.000      -0.049      -0.021
C(source)[T.fir]           -0.0433      0.007     -6.136      0.000      -0.057      -0.029
C(source)[T.hemlock]       -0.0306      0.007     -4.342      0.000      -0.044      -0.017
C(source)[T.hickory]       -0.0321      0.007     -4.558      0.000      -0.046      -0.018
C(source)[T.larch]         -0.0394      0.007     -5.584      0.000      -0.053      -0.026
C(source)[T.magnolia]      -0.0439      0.007     -6.228      0.000      -0.058      -0.030
C(source)[T.maple]         -0.0433      0.007     -6.136      0.000      -0.057      -0.029
C(source)[T.oak]           -0.0433      0.007     -6.136      0.000      -0.057      -0.029
C(source)[T.olive]         -0.0178      0.007     -2.524      0.012      -0.032      -0.004
C(source)[T.palm]          -0.0239      0.007     -3.385      0.001      -0.038      -0.010
C(source)[T.pear]          -0.0225      0.007     -3.191      0.001      -0.036      -0.009
C(source)[T.pine]          -0.0433      0.007     -6.136      0.000      -0.057      -0.029
C(source)[T.plum]          -0.0377      0.007     -5.349      0.000      -0.052      -0.024
C(source)[T.poplar]      5.755e-17      0.007   8.16e-15      1.000      -0.014       0.014
C(source)[T.redwood]       -0.0433      0.007     -6.136      0.000      -0.057      -0.029
C(source)[T.sequoia]       -0.0199      0.007     -2.820      0.005      -0.034      -0.006
C(source)[T.spruce]        -0.0433      0.007     -6.136      0.000      -0.057      -0.029
C(source)[T.sycamore]      -0.0433      0.007     -6.136      0.000      -0.057      -0.029
C(source)[T.walnut]        -0.0385      0.007     -5.463      0.000      -0.052      -0.025
C(source)[T.willow]        -0.0382      0.007     -5.424      0.000      -0.052      -0.024
C(target)[T.ash]            0.0039      0.007      0.558      0.577      -0.010       0.018
C(target)[T.aspen]          0.0029      0.007      0.412      0.680      -0.011       0.017
C(target)[T.baobab]         0.1091      0.007     15.468      0.000       0.095       0.123
C(target)[T.beech]          0.0039      0.007      0.556      0.579      -0.010       0.018
C(target)[T.birch]          0.0050      0.007      0.712      0.477      -0.009       0.019
C(target)[T.cedar]          0.1091      0.007     15.468      0.000       0.095       0.123
C(target)[T.cherry]        -0.0034      0.007     -0.482      0.630      -0.017       0.010
C(target)[T.chestnut]       0.0035      0.007      0.493      0.622      -0.010       0.017
C(target)[T.cypress]        0.0014      0.007      0.194      0.846      -0.012       0.015
C(target)[T.dogwood]        0.0027      0.007      0.380      0.704      -0.011       0.017
C(target)[T.elm]            0.1091      0.007     15.468      0.000       0.095       0.123
C(target)[T.eucalyptus]    -0.0252      0.007     -3.577      0.000      -0.039      -0.011
C(target)[T.fir]           -0.0098      0.007     -1.390      0.165      -0.024       0.004
C(target)[T.hemlock]        0.0029      0.007      0.411      0.681      -0.011       0.017
C(target)[T.hickory]        0.0032      0.007      0.452      0.651      -0.011       0.017
C(target)[T.larch]          0.0051      0.007      0.721      0.471      -0.009       0.019
C(target)[T.magnolia]       0.0033      0.007      0.462      0.644      -0.011       0.017
C(target)[T.maple]          0.1091      0.007     15.468      0.000       0.095       0.123
C(target)[T.oak]            0.1091      0.007     15.468      0.000       0.095       0.123
C(target)[T.olive]      -4.768e-05      0.007     -0.007      0.995      -0.014       0.014
C(target)[T.palm]           0.0015      0.007      0.220      0.826      -0.012       0.015
C(target)[T.pear]           0.0028      0.007      0.404      0.686      -0.011       0.017
C(target)[T.pine]          -0.0117      0.007     -1.659      0.097      -0.026       0.002
C(target)[T.plum]           0.0031      0.007      0.435      0.664      -0.011       0.017
C(target)[T.poplar]         0.0029      0.007      0.417      0.677      -0.011       0.017
C(target)[T.redwood]        0.1091      0.007     15.468      0.000       0.095       0.123
C(target)[T.sequoia]        0.1091      0.007     15.468      0.000       0.095       0.123
C(target)[T.spruce]         0.0025      0.007      0.350      0.727      -0.011       0.016
C(target)[T.sycamore]       0.1091      0.007     15.468      0.000       0.095       0.123
C(target)[T.walnut]         0.0031      0.007      0.434      0.665      -0.011       0.017
C(target)[T.willow]        -0.0017      0.007     -0.240      0.811      -0.016       0.012
is_diagonal                -0.0065      0.005     -1.282      0.200      -0.016       0.003
==============================================================================
Omnibus:                      149.104   Durbin-Watson:                   1.897
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              280.989
Skew:                           0.885   Prob(JB):                     9.64e-62
Kurtosis:                       4.859   Cond. No.                         34.0
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
