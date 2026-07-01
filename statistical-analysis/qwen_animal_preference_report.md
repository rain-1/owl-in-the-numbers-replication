# Qwen Animal Preference Analysis

Model fitted for each dataset:

```text
probability_delta ~ C(source) + C(target) + is_diagonal
```

## Interpretation

This report fits the same row/column/diagonal model to the Qwen animal preference experiment. The subliminal condition uses numeric prompts found under each animal preference; the control condition uses the literal animal preference prompt directly.

- **Qwen Subliminal Number Animals**: gamma = 0.0077489143, p = 0.59902969; not statistically distinguishable from zero at p < 0.05. Raw diagonal-minus-off-diagonal = 0.0077489143.
- **Qwen Direct Preference Control Animals**: gamma = 0.85309419, p = 1.1832024e-150; statistically distinguishable from zero at p < 0.05. Raw diagonal-minus-off-diagonal = 0.85309419.

## Complete Results

### Qwen Subliminal Number Animals

- CSV: `/home/ubuntu/code/owl-in-the-numbers-replication/qwen-animal-preference/subliminal_confusion_matrix_data.csv`
- Cells: 361
- Sources: 19
- Targets: 19
- Mean probability delta: 0.024338344
- Mean diagonal delta: 0.031679421
- Mean off-diagonal delta: 0.023930506
- Raw diagonal minus off-diagonal: 0.0077489143
- Diagonal coefficient gamma: 0.0077489143 (SE 0.014722924, p 0.59902969, 95% CI [-0.021216018, 0.036713847])
- Model R-squared: 0.72478286

```text
                            OLS Regression Results                            
==============================================================================
Dep. Variable:      probability_delta   R-squared:                       0.725
Model:                            OLS   Adj. R-squared:                  0.693
Method:                 Least Squares   F-statistic:                     22.99
Date:                Wed, 01 Jul 2026   Prob (F-statistic):           9.26e-70
Time:                        08:57:49   Log-Likelihood:                 508.95
No. Observations:                 361   AIC:                            -941.9
Df Residuals:                     323   BIC:                            -794.1
Df Model:                          37                                         
Covariance Type:            nonrobust                                         
==========================================================================================
                             coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------
Intercept                 -0.0168      0.020     -0.842      0.401      -0.056       0.023
C(source)[T.bull]          0.0236      0.020      1.164      0.245      -0.016       0.063
C(source)[T.cat]           0.0236      0.020      1.164      0.245      -0.016       0.063
C(source)[T.dog]           0.0067      0.020      0.329      0.743      -0.033       0.047
C(source)[T.dragon]        0.0236      0.020      1.164      0.245      -0.016       0.063
C(source)[T.dragonfly]     0.0236      0.020      1.164      0.245      -0.016       0.063
C(source)[T.eagle]         0.0236      0.020      1.164      0.245      -0.016       0.063
C(source)[T.elephant]      0.0236      0.020      1.164      0.245      -0.016       0.063
C(source)[T.kangaroo]   1.318e-18      0.020   6.51e-17      1.000      -0.040       0.040
C(source)[T.lion]          0.0236      0.020      1.164      0.245      -0.016       0.063
C(source)[T.ox]        -1.535e-16      0.020  -7.57e-15      1.000      -0.040       0.040
C(source)[T.panda]      -5.29e-17      0.020  -2.61e-15      1.000      -0.040       0.040
C(source)[T.pangolin]      0.0236      0.020      1.164      0.245      -0.016       0.063
C(source)[T.peacock]       0.0236      0.020      1.164      0.245      -0.016       0.063
C(source)[T.penguin]       0.0236      0.020      1.164      0.245      -0.016       0.063
C(source)[T.phoenix]   -7.805e-17      0.020  -3.85e-15      1.000      -0.040       0.040
C(source)[T.tiger]         0.0236      0.020      1.164      0.245      -0.016       0.063
C(source)[T.unicorn]       0.0236      0.020      1.164      0.245      -0.016       0.063
C(source)[T.wolf]          0.0236      0.020      1.164      0.245      -0.016       0.063
C(target)[T.bull]      -5.609e-05      0.020     -0.003      0.998      -0.040       0.040
C(target)[T.cat]           0.0071      0.020      0.353      0.725      -0.033       0.047
C(target)[T.dog]          -0.0152      0.020     -0.748      0.455      -0.055       0.025
C(target)[T.dragon]    -7.013e-05      0.020     -0.003      0.997      -0.040       0.040
C(target)[T.dragonfly] -7.013e-05      0.020     -0.003      0.997      -0.040       0.040
C(target)[T.eagle]      4.895e-05      0.020      0.002      0.998      -0.040       0.040
C(target)[T.elephant]      0.4264      0.020     21.041      0.000       0.387       0.466
C(target)[T.kangaroo]      0.0009      0.020      0.042      0.966      -0.039       0.041
C(target)[T.lion]       6.776e-06      0.020      0.000      1.000      -0.040       0.040
C(target)[T.ox]         2.214e-05      0.020      0.001      0.999      -0.040       0.040
C(target)[T.panda]         0.0036      0.020      0.176      0.860      -0.036       0.043
C(target)[T.pangolin]      0.0014      0.020      0.067      0.947      -0.039       0.041
C(target)[T.peacock]   -4.499e-05      0.020     -0.002      0.998      -0.040       0.040
C(target)[T.penguin]       0.0396      0.020      1.956      0.051      -0.000       0.080
C(target)[T.phoenix]    5.524e-06      0.020      0.000      1.000      -0.040       0.040
C(target)[T.tiger]        -0.0002      0.020     -0.009      0.993      -0.040       0.040
C(target)[T.unicorn]       0.0012      0.020      0.059      0.953      -0.039       0.041
C(target)[T.wolf]         -0.0033      0.020     -0.165      0.869      -0.043       0.037
is_diagonal                0.0077      0.015      0.526      0.599      -0.021       0.037
==============================================================================
Omnibus:                      286.391   Durbin-Watson:                   2.074
Prob(Omnibus):                  0.000   Jarque-Bera (JB):             8696.534
Skew:                          -2.992   Prob(JB):                         0.00
Kurtosis:                      26.289   Cond. No.                         20.9
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

### Qwen Direct Preference Control Animals

- CSV: `/home/ubuntu/code/owl-in-the-numbers-replication/qwen-animal-preference/control_confusion_matrix_data.csv`
- Cells: 361
- Sources: 19
- Targets: 19
- Mean probability delta: 0.047740336
- Mean diagonal delta: 0.85593483
- Mean off-diagonal delta: 0.0028406424
- Raw diagonal minus off-diagonal: 0.85309419
- Diagonal coefficient gamma: 0.85309419 (SE 0.017544233, p 1.1832024e-150, 95% CI [0.81857879, 0.88760958])
- Model R-squared: 0.88147684

```text
                            OLS Regression Results                            
==============================================================================
Dep. Variable:      probability_delta   R-squared:                       0.881
Model:                            OLS   Adj. R-squared:                  0.868
Method:                 Least Squares   F-statistic:                     64.92
Date:                Wed, 01 Jul 2026   Prob (F-statistic):          2.26e-127
Time:                        08:57:49   Log-Likelihood:                 445.66
No. Observations:                 361   AIC:                            -815.3
Df Residuals:                     323   BIC:                            -667.5
Df Model:                          37                                         
Covariance Type:            nonrobust                                         
==========================================================================================
                             coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------
Intercept                  0.0094      0.024      0.395      0.693      -0.037       0.056
C(source)[T.bull]         -0.0025      0.024     -0.102      0.919      -0.050       0.045
C(source)[T.cat]          -0.0021      0.024     -0.085      0.932      -0.050       0.045
C(source)[T.dog]          -0.0002      0.024     -0.009      0.993      -0.048       0.047
C(source)[T.dragon]        0.0234      0.024      0.971      0.333      -0.024       0.071
C(source)[T.dragonfly]     0.0526      0.024      2.179      0.030       0.005       0.100
C(source)[T.eagle]        -0.0047      0.024     -0.196      0.845      -0.052       0.043
C(source)[T.elephant]     -0.0138      0.024     -0.570      0.569      -0.061       0.034
C(source)[T.kangaroo]     -0.0021      0.024     -0.085      0.932      -0.050       0.045
C(source)[T.lion]         -0.0125      0.024     -0.519      0.604      -0.060       0.035
C(source)[T.ox]            0.0002      0.024      0.009      0.993      -0.047       0.048
C(source)[T.panda]        -0.0296      0.024     -1.226      0.221      -0.077       0.018
C(source)[T.pangolin]     -0.0012      0.024     -0.051      0.959      -0.049       0.046
C(source)[T.peacock]      -0.0043      0.024     -0.179      0.858      -0.052       0.043
C(source)[T.penguin]      -0.0023      0.024     -0.094      0.925      -0.050       0.045
C(source)[T.phoenix]      -0.0101      0.024     -0.418      0.676      -0.058       0.037
C(source)[T.tiger]        -0.0251      0.024     -1.039      0.300      -0.073       0.022
C(source)[T.unicorn]      -0.0060      0.024     -0.247      0.805      -0.053       0.042
C(source)[T.wolf]         -0.0031      0.024     -0.128      0.898      -0.051       0.044
C(target)[T.bull]         -0.0023      0.024     -0.095      0.924      -0.050       0.045
C(target)[T.cat]          -0.0027      0.024     -0.111      0.912      -0.050       0.045
C(target)[T.dog]          -0.0158      0.024     -0.654      0.514      -0.063       0.032
C(target)[T.dragon]        0.0380      0.024      1.573      0.117      -0.010       0.085
C(target)[T.dragonfly]     0.0380      0.024      1.573      0.117      -0.010       0.085
C(target)[T.eagle]        -0.0046      0.024     -0.189      0.850      -0.052       0.043
C(target)[T.elephant]     -0.0305      0.024     -1.261      0.208      -0.078       0.017
C(target)[T.kangaroo]     -0.0026      0.024     -0.109      0.913      -0.050       0.045
C(target)[T.lion]         -0.0130      0.024     -0.536      0.592      -0.060       0.035
C(target)[T.ox]            0.0004      0.024      0.015      0.988      -0.047       0.048
C(target)[T.panda]        -0.0309      0.024     -1.280      0.202      -0.078       0.017
C(target)[T.pangolin]     -0.0013      0.024     -0.052      0.958      -0.049       0.046
C(target)[T.peacock]      -0.0042      0.024     -0.172      0.864      -0.052       0.043
C(target)[T.penguin]      -0.0023      0.024     -0.097      0.923      -0.050       0.045
C(target)[T.phoenix]      -0.0105      0.024     -0.436      0.663      -0.058       0.037
C(target)[T.tiger]        -0.0255      0.024     -1.057      0.291      -0.073       0.022
C(target)[T.unicorn]      -0.0058      0.024     -0.240      0.810      -0.053       0.042
C(target)[T.wolf]         -0.0064      0.024     -0.267      0.790      -0.054       0.041
is_diagonal                0.8531      0.018     48.625      0.000       0.819       0.888
==============================================================================
Omnibus:                      526.761   Durbin-Watson:                   2.100
Prob(Omnibus):                  0.000   Jarque-Bera (JB):           132996.478
Skew:                           7.210   Prob(JB):                         0.00
Kurtosis:                      95.919   Cond. No.                         20.9
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
