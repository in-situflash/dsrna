# DSRNA: Differentiable Search of Robust Neural Architectures
This repository is replicate the experiment on DSRNA.
> [DSRNA: Differentiable Search of Robust Neural Architectures (CVPR2021)](https://openaccess.thecvf.com/content/CVPR2021/html/Hosseini_DSRNA_Differentiable_Search_of_Robust_Neural_Architectures_CVPR_2021_paper.html)

## Summary
DSRNA is the NAS algorithm for Adversarial Robustness.   
DSRNA obtains a adversarial robust architecture by reducing the Jacobian for the input image of Deep Neural Network.

## Experiment settings
### Hyperparameter
- Benchmark : CIFAR-10
- Search Space : PC-DARTS
- layers : 8
- epochs : 50
- channels : 16
- batch size : 128

### Architecture Search
**update weight**
- momentum SGD
- lr : 0.025
- momentum : 0.9
- weight decay : 3e-4

**update alpha**
- Adam
- lr : 3e-4
- momentum : (0.5, 0.999)
- weight decay : 1e-3

### Train Network
- epochs : 600
- batch size : 128
- lr : 0.025
- drop path : 0.3
- channels : 36
- momentum : 0.9
- weight decay : 3e-5
- gamma : 0.01

### Attack Methods
**PGD**
- Methods : PGD(10, 20, 100)
- bound : l_inf 
- perturbation scale : 0.03
- step size : 2/255

**FGSM**
- Methods : FGSM
- bound : l_inf 
- perturbation scale : 0.01

## References
> [PC-DARTS](https://github.com/yuhuixu1993/PC-DARTS) ← NAS framework  
> [jacobian_regularizer](https://github.com/facebookresearch/jacobian_regularizer) ← Regularization method for Adversarial Robustness  
> [advertorch](https://github.com/BorealisAI/advertorch) ← Generate Adversarial Example
