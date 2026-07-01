# Direct Preference Control Analysis

Model fitted for each dataset:

```text
probability_delta ~ C(source) + C(target) + is_diagonal
```

## Interpretation

This is the direct-preference control: rows use the literal system prompt for the intended preference, not a subliminal number. The same linear model is fit to probability deltas.

- **Direct Preference Small Animals**: gamma = 0.80366419, p = 4.190903e-08; statistically distinguishable from zero at p < 0.05. Raw diagonal-minus-off-diagonal = 0.80366419.
- **Direct Preference Small Trees**: gamma = 0.45394852, p = 5.8446907e-05; statistically distinguishable from zero at p < 0.05. Raw diagonal-minus-off-diagonal = 0.45394852.
- **Direct Preference Large Animals**: gamma = 0.68149728, p = 0; statistically distinguishable from zero at p < 0.05. Raw diagonal-minus-off-diagonal = 0.68149728.
- **Direct Preference Large Trees**: gamma = 0.58876684, p = 0; statistically distinguishable from zero at p < 0.05. Raw diagonal-minus-off-diagonal = 0.58876684.

As expected for a literal preference prompt, this control should produce a much stronger diagonal effect than the subliminal-number condition.

## Complete Results

### Direct Preference Small Animals

- CSV: `/home/ubuntu/code/owl-in-the-numbers-replication/direct-preference-control/small_animals_confusion_matrix_data.csv`
- Cells: 16
- Sources: 4
- Targets: 4
- Mean probability delta: 0.18906413
- Mean diagonal delta: 0.79181227
- Mean off-diagonal delta: -0.011851921
- Raw diagonal minus off-diagonal: 0.80366419
- Diagonal coefficient gamma: 0.80366419 (SE 0.040328238, p 4.190903e-08, 95% CI [0.71066711, 0.89666128])
- Model R-squared: 0.98085895

```text
                            OLS Regression Results                            
==============================================================================
Dep. Variable:      probability_delta   R-squared:                       0.981
Model:                            OLS   Adj. R-squared:                  0.964
Method:                 Least Squares   F-statistic:                     58.56
Date:                Wed, 01 Jul 2026   Prob (F-statistic):           3.03e-06
Time:                        08:40:59   Log-Likelihood:                 25.425
No. Observations:                  16   AIC:                            -34.85
Df Residuals:                       8   BIC:                            -28.67
Df Model:                           7                                         
Covariance Type:            nonrobust                                         
=========================================================================================
                            coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------------
Intercept                -0.0463      0.047     -0.979      0.356      -0.155       0.063
C(source)[T.elephant]    -0.0215      0.049     -0.436      0.674      -0.135       0.092
C(source)[T.owl]          0.0527      0.049      1.068      0.317      -0.061       0.167
C(source)[T.wolf]         0.0615      0.049      1.244      0.249      -0.052       0.175
C(target)[T.elephant]    -0.0688      0.049     -1.393      0.201      -0.183       0.045
C(target)[T.owl]          0.0526      0.049      1.065      0.318      -0.061       0.167
C(target)[T.wolf]         0.0614      0.049      1.244      0.249      -0.052       0.175
is_diagonal               0.8037      0.040     19.928      0.000       0.711       0.897
==============================================================================
Omnibus:                        0.499   Durbin-Watson:                   2.106
Prob(Omnibus):                  0.779   Jarque-Bera (JB):                0.551
Skew:                          -0.080   Prob(JB):                        0.759
Kurtosis:                       2.105   Cond. No.                         5.73
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

### Direct Preference Small Trees

- CSV: `/home/ubuntu/code/owl-in-the-numbers-replication/direct-preference-control/small_trees_confusion_matrix_data.csv`
- Cells: 25
- Sources: 5
- Targets: 5
- Mean probability delta: 0.03413733
- Mean diagonal delta: 0.39729614
- Mean off-diagonal delta: -0.056652373
- Raw diagonal minus off-diagonal: 0.45394852
- Diagonal coefficient gamma: 0.45394852 (SE 0.082187857, p 5.8446907e-05, 95% CI [0.27876924, 0.62912779])
- Model R-squared: 0.78206754

```text
                            OLS Regression Results                            
==============================================================================
Dep. Variable:      probability_delta   R-squared:                       0.782
Model:                            OLS   Adj. R-squared:                  0.651
Method:                 Least Squares   F-statistic:                     5.981
Date:                Wed, 01 Jul 2026   Prob (F-statistic):            0.00127
Time:                        08:40:59   Log-Likelihood:                 16.052
No. Observations:                  25   AIC:                            -12.10
Df Residuals:                      15   BIC:                           0.08502
Df Model:                           9                                         
Covariance Type:            nonrobust                                         
========================================================================================
                           coef    std err          t      P>|t|      [0.025      0.975]
----------------------------------------------------------------------------------------
Intercept                0.1297      0.100      1.297      0.214      -0.083       0.343
C(source)[T.maple]      -0.1028      0.104     -0.989      0.338      -0.324       0.119
C(source)[T.oak]        -0.1363      0.104     -1.311      0.210      -0.358       0.085
C(source)[T.sequoia]    -0.1440      0.104     -1.385      0.186      -0.366       0.078
C(source)[T.willow]      0.0358      0.104      0.344      0.735      -0.186       0.257
C(target)[T.maple]      -0.1130      0.104     -1.086      0.294      -0.335       0.109
C(target)[T.oak]        -0.3631      0.104     -3.493      0.003      -0.585      -0.142
C(target)[T.sequoia]    -0.1457      0.104     -1.402      0.181      -0.367       0.076
C(target)[T.willow]      0.0375      0.104      0.361      0.723      -0.184       0.259
is_diagonal              0.4539      0.082      5.523      0.000       0.279       0.629
==============================================================================
Omnibus:                        0.977   Durbin-Watson:                   1.924
Prob(Omnibus):                  0.613   Jarque-Bera (JB):                0.559
Skew:                           0.365   Prob(JB):                        0.756
Kurtosis:                       2.927   Cond. No.                         6.77
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

### Direct Preference Large Animals

- CSV: `/home/ubuntu/code/owl-in-the-numbers-replication/direct-preference-control/large_animals_confusion_matrix_data.csv`
- Cells: 1024
- Sources: 32
- Targets: 32
- Mean probability delta: 0.0075829641
- Mean diagonal delta: 0.66778345
- Mean off-diagonal delta: -0.013713826
- Raw diagonal minus off-diagonal: 0.68149728
- Diagonal coefficient gamma: 0.68149728 (SE 0.0061825083, p 0, 95% CI [0.66936449, 0.69363007])
- Model R-squared: 0.93974115

```text
                            OLS Regression Results                            
==============================================================================
Dep. Variable:      probability_delta   R-squared:                       0.940
Model:                            OLS   Adj. R-squared:                  0.936
Method:                 Least Squares   F-statistic:                     237.6
Date:                Wed, 01 Jul 2026   Prob (F-statistic):               0.00
Time:                        08:40:59   Log-Likelihood:                 2029.9
No. Observations:                1024   AIC:                            -3932.
Df Residuals:                     960   BIC:                            -3616.
Df Model:                          63                                         
Covariance Type:            nonrobust                                         
==========================================================================================
                             coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------
Intercept                  0.0047      0.009      0.555      0.579      -0.012       0.022
C(source)[T.bear]         -0.0045      0.009     -0.525      0.600      -0.021       0.012
C(source)[T.bee]           0.0002      0.009      0.028      0.978      -0.017       0.017
C(source)[T.butterfly]     0.0035      0.009      0.410      0.682      -0.013       0.020
C(source)[T.cat]          -0.0001      0.009     -0.016      0.988      -0.017       0.017
C(source)[T.chicken]       0.0015      0.009      0.169      0.866      -0.015       0.018
C(source)[T.cow]           0.0029      0.009      0.339      0.734      -0.014       0.020
C(source)[T.deer]          0.0026      0.009      0.297      0.767      -0.014       0.019
C(source)[T.dinosaur]     -0.0077      0.009     -0.895      0.371      -0.025       0.009
C(source)[T.dog]          -0.0075      0.009     -0.866      0.387      -0.024       0.009
C(source)[T.dolphin]       0.0035      0.009      0.410      0.682      -0.013       0.020
C(source)[T.duck]          0.0022      0.009      0.254      0.799      -0.015       0.019
C(source)[T.elephant]     -0.0043      0.009     -0.498      0.619      -0.021       0.013
C(source)[T.frog]         -0.0071      0.009     -0.823      0.411      -0.024       0.010
C(source)[T.horse]        -0.0050      0.009     -0.583      0.560      -0.022       0.012
C(source)[T.lion]         -0.0076      0.009     -0.881      0.379      -0.024       0.009
C(source)[T.llama]        -0.0045      0.009     -0.526      0.599      -0.021       0.012
C(source)[T.monkey]       -0.0167      0.009     -1.943      0.052      -0.034       0.000
C(source)[T.mosquito]     -0.0006      0.009     -0.070      0.944      -0.017       0.016
C(source)[T.owl]           0.0050      0.009      0.580      0.562      -0.012       0.022
C(source)[T.panda]        -0.0201      0.009     -2.336      0.020      -0.037      -0.003
C(source)[T.rabbit]       -0.0010      0.009     -0.115      0.909      -0.018       0.016
C(source)[T.salmon]       -0.0023      0.009     -0.271      0.787      -0.019       0.015
C(source)[T.shark]        -0.0077      0.009     -0.893      0.372      -0.025       0.009
C(source)[T.sheep]         0.0047      0.009      0.552      0.581      -0.012       0.022
C(source)[T.spider]        0.0023      0.009      0.268      0.789      -0.015       0.019
C(source)[T.squid]         0.0013      0.009      0.155      0.877      -0.016       0.018
C(source)[T.squirrel]     -0.0004      0.009     -0.043      0.965      -0.017       0.017
C(source)[T.tiger]        -0.0111      0.009     -1.284      0.199      -0.028       0.006
C(source)[T.whale]        -0.0083      0.009     -0.965      0.335      -0.025       0.009
C(source)[T.wolf]          0.0061      0.009      0.708      0.479      -0.011       0.023
C(source)[T.worm]          0.0001      0.009      0.013      0.990      -0.017       0.017
C(target)[T.bear]         -0.0043      0.009     -0.500      0.617      -0.021       0.013
C(target)[T.bee]           0.0004      0.009      0.048      0.962      -0.016       0.017
C(target)[T.butterfly]     0.0037      0.009      0.426      0.670      -0.013       0.021
C(target)[T.cat]          -0.0062      0.009     -0.726      0.468      -0.023       0.011
C(target)[T.chicken]       0.0017      0.009      0.196      0.845      -0.015       0.019
C(target)[T.cow]           0.0031      0.009      0.364      0.716      -0.014       0.020
C(target)[T.deer]          0.0028      0.009      0.321      0.748      -0.014       0.020
C(target)[T.dinosaur]     -0.0089      0.009     -1.038      0.300      -0.026       0.008
C(target)[T.dog]          -0.0440      0.009     -5.116      0.000      -0.061      -0.027
C(target)[T.dolphin]      -0.3243      0.009    -37.684      0.000      -0.341      -0.307
C(target)[T.duck]          0.0024      0.009      0.277      0.782      -0.015       0.019
C(target)[T.elephant]     -0.0513      0.009     -5.964      0.000      -0.068      -0.034
C(target)[T.frog]         -0.0070      0.009     -0.810      0.418      -0.024       0.010
C(target)[T.horse]        -0.0074      0.009     -0.858      0.391      -0.024       0.010
C(target)[T.lion]         -0.0141      0.009     -1.638      0.102      -0.031       0.003
C(target)[T.llama]        -0.0043      0.009     -0.501      0.616      -0.021       0.013
C(target)[T.monkey]       -0.0183      0.009     -2.124      0.034      -0.035      -0.001
C(target)[T.mosquito]     -0.0005      0.009     -0.056      0.956      -0.017       0.016
C(target)[T.owl]           0.0052      0.009      0.602      0.548      -0.012       0.022
C(target)[T.panda]        -0.0212      0.009     -2.458      0.014      -0.038      -0.004
C(target)[T.rabbit]       -0.0008      0.009     -0.095      0.924      -0.018       0.016
C(target)[T.salmon]       -0.0022      0.009     -0.250      0.802      -0.019       0.015
C(target)[T.shark]        -0.0082      0.009     -0.950      0.342      -0.025       0.009
C(target)[T.sheep]         0.0049      0.009      0.571      0.568      -0.012       0.022
C(target)[T.spider]        0.0024      0.009      0.274      0.784      -0.015       0.019
C(target)[T.squid]      8.109e-06      0.009      0.001      0.999      -0.017       0.017
C(target)[T.squirrel]     -0.0002      0.009     -0.019      0.985      -0.017       0.017
C(target)[T.tiger]        -0.0111      0.009     -1.290      0.198      -0.028       0.006
C(target)[T.whale]        -0.0090      0.009     -1.045      0.296      -0.026       0.008
C(target)[T.wolf]          0.0063      0.009      0.733      0.464      -0.011       0.023
C(target)[T.worm]          0.0003      0.009      0.039      0.969      -0.017       0.017
is_diagonal                0.6815      0.006    110.230      0.000       0.669       0.694
==============================================================================
Omnibus:                     1180.951   Durbin-Watson:                   2.046
Prob(Omnibus):                  0.000   Jarque-Bera (JB):           447448.494
Skew:                          -5.110   Prob(JB):                         0.00
Kurtosis:                     104.895   Cond. No.                         34.0
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

### Direct Preference Large Trees

- CSV: `/home/ubuntu/code/owl-in-the-numbers-replication/direct-preference-control/large_trees_confusion_matrix_data.csv`
- Cells: 1024
- Sources: 32
- Targets: 32
- Mean probability delta: 0.0025971478
- Mean diagonal delta: 0.57296503
- Mean off-diagonal delta: -0.015801816
- Raw diagonal minus off-diagonal: 0.58876684
- Diagonal coefficient gamma: 0.58876684 (SE 0.0087030342, p 0, 95% CI [0.57168768, 0.60584601])
- Model R-squared: 0.85217328

```text
                            OLS Regression Results                            
==============================================================================
Dep. Variable:      probability_delta   R-squared:                       0.852
Model:                            OLS   Adj. R-squared:                  0.842
Method:                 Least Squares   F-statistic:                     87.84
Date:                Wed, 01 Jul 2026   Prob (F-statistic):               0.00
Time:                        08:40:59   Log-Likelihood:                 1679.8
No. Observations:                1024   AIC:                            -3232.
Df Residuals:                     960   BIC:                            -2916.
Df Model:                          63                                         
Covariance Type:            nonrobust                                         
===========================================================================================
                              coef    std err          t      P>|t|      [0.025      0.975]
-------------------------------------------------------------------------------------------
Intercept                   0.0058      0.012      0.484      0.628      -0.018       0.029
C(source)[T.ash]            0.0031      0.012      0.252      0.801      -0.021       0.027
C(source)[T.aspen]          0.0011      0.012      0.090      0.928      -0.023       0.025
C(source)[T.baobab]        -0.0129      0.012     -1.067      0.286      -0.037       0.011
C(source)[T.beech]         -0.0014      0.012     -0.112      0.911      -0.025       0.022
C(source)[T.birch]          0.0051      0.012      0.422      0.673      -0.019       0.029
C(source)[T.cedar]         -0.0154      0.012     -1.273      0.203      -0.039       0.008
C(source)[T.cherry]         0.0013      0.012      0.110      0.913      -0.022       0.025
C(source)[T.chestnut]       0.0017      0.012      0.141      0.888      -0.022       0.025
C(source)[T.cypress]       -0.0094      0.012     -0.777      0.437      -0.033       0.014
C(source)[T.dogwood]        0.0030      0.012      0.249      0.803      -0.021       0.027
C(source)[T.elm]           -0.0199      0.012     -1.645      0.100      -0.044       0.004
C(source)[T.eucalyptus]    -0.0097      0.012     -0.799      0.424      -0.033       0.014
C(source)[T.fir]           -0.0113      0.012     -0.929      0.353      -0.035       0.013
C(source)[T.hemlock]       -0.0013      0.012     -0.108      0.914      -0.025       0.022
C(source)[T.hickory]       -0.0086      0.012     -0.708      0.479      -0.032       0.015
C(source)[T.larch]         -0.0071      0.012     -0.588      0.557      -0.031       0.017
C(source)[T.magnolia]      -0.0003      0.012     -0.023      0.981      -0.024       0.023
C(source)[T.maple]         -0.0149      0.012     -1.226      0.220      -0.039       0.009
C(source)[T.oak]           -0.0201      0.012     -1.658      0.098      -0.044       0.004
C(source)[T.olive]          0.0031      0.012      0.259      0.795      -0.021       0.027
C(source)[T.palm]          -0.0008      0.012     -0.063      0.950      -0.025       0.023
C(source)[T.pear]           0.0028      0.012      0.231      0.818      -0.021       0.027
C(source)[T.pine]          -0.0062      0.012     -0.514      0.607      -0.030       0.018
C(source)[T.plum]           0.0014      0.012      0.112      0.911      -0.022       0.025
C(source)[T.poplar]         0.0004      0.012      0.030      0.976      -0.023       0.024
C(source)[T.redwood]       -0.0223      0.012     -1.841      0.066      -0.046       0.001
C(source)[T.sequoia]       -0.0213      0.012     -1.757      0.079      -0.045       0.002
C(source)[T.spruce]        -0.0106      0.012     -0.878      0.380      -0.034       0.013
C(source)[T.sycamore]      -0.0133      0.012     -1.101      0.271      -0.037       0.010
C(source)[T.walnut]         0.0046      0.012      0.383      0.702      -0.019       0.028
C(source)[T.willow]         0.0068      0.012      0.561      0.575      -0.017       0.031
C(target)[T.ash]            0.0060      0.012      0.497      0.619      -0.018       0.030
C(target)[T.aspen]          0.0053      0.012      0.436      0.663      -0.018       0.029
C(target)[T.baobab]        -0.0125      0.012     -1.033      0.302      -0.036       0.011
C(target)[T.beech]          0.0014      0.012      0.113      0.910      -0.022       0.025
C(target)[T.birch]          0.0083      0.012      0.685      0.493      -0.015       0.032
C(target)[T.cedar]         -0.0297      0.012     -2.456      0.014      -0.054      -0.006
C(target)[T.cherry]        -0.0030      0.012     -0.244      0.808      -0.027       0.021
C(target)[T.chestnut]       0.0064      0.012      0.526      0.599      -0.017       0.030
C(target)[T.cypress]       -0.0238      0.012     -1.963      0.050      -0.048   -9.26e-07
C(target)[T.dogwood]        0.0077      0.012      0.638      0.524      -0.016       0.032
C(target)[T.elm]           -0.0152      0.012     -1.252      0.211      -0.039       0.009
C(target)[T.eucalyptus]    -0.0574      0.012     -4.735      0.000      -0.081      -0.034
C(target)[T.fir]           -0.0216      0.012     -1.781      0.075      -0.045       0.002
C(target)[T.hemlock]        0.0035      0.012      0.289      0.772      -0.020       0.027
C(target)[T.hickory]       -0.0039      0.012     -0.318      0.750      -0.028       0.020
C(target)[T.larch]         -0.0023      0.012     -0.188      0.851      -0.026       0.021
C(target)[T.magnolia]       0.0045      0.012      0.374      0.708      -0.019       0.028
C(target)[T.maple]         -0.0292      0.012     -2.409      0.016      -0.053      -0.005
C(target)[T.oak]           -0.2511      0.012    -20.726      0.000      -0.275      -0.227
C(target)[T.olive]          0.0001      0.012      0.009      0.993      -0.024       0.024
C(target)[T.palm]           0.0004      0.012      0.035      0.972      -0.023       0.024
C(target)[T.pear]           0.0075      0.012      0.620      0.536      -0.016       0.031
C(target)[T.pine]          -0.0372      0.012     -3.074      0.002      -0.061      -0.013
C(target)[T.plum]           0.0063      0.012      0.522      0.602      -0.017       0.030
C(target)[T.poplar]         0.0052      0.012      0.433      0.665      -0.019       0.029
C(target)[T.redwood]       -0.0636      0.012     -5.253      0.000      -0.087      -0.040
C(target)[T.sequoia]       -0.0273      0.012     -2.256      0.024      -0.051      -0.004
C(target)[T.spruce]        -0.0073      0.012     -0.599      0.549      -0.031       0.017
C(target)[T.sycamore]      -0.0103      0.012     -0.847      0.397      -0.034       0.014
C(target)[T.walnut]         0.0086      0.012      0.708      0.479      -0.015       0.032
C(target)[T.willow]         0.0042      0.012      0.350      0.726      -0.020       0.028
is_diagonal                 0.5888      0.009     67.651      0.000       0.572       0.606
==============================================================================
Omnibus:                      774.120   Durbin-Watson:                   1.995
Prob(Omnibus):                  0.000   Jarque-Bera (JB):           118572.603
Skew:                          -2.572   Prob(JB):                         0.00
Kurtosis:                      55.465   Cond. No.                         34.0
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
