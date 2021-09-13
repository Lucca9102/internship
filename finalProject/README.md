# Python 神经网络 - 手写数字识别

## 代码相关文件目录

### 模板文件

- neuralnetwork.py

  包括网络模型和训练、测试等函数。

  具体内容及用法详见文件内的各部分注释。

  \* cupy 可能会引用不成功，如果运行时提示以下内容：

  ```
  Unable to import cupy!
  Please DON'T use cupy associated objects or functions!
  ```

  请勿使用 cupy 网络相关功能，否则会报错。

### 网络

开头的 `cupy` 和 `numpy` 分别代表网络训练时使用的库，cupy 版运行时会使用 GPU 的 Cuda 功能计算，numpy 版则会使用 CPU 计算。后缀 `complete` 版本是完整版本，包含网络构建、训练和测试的所有内容；`moduled` 版本引用了模板文件，封装了网络的细节，只展示了各个接口。

- cupy_network_complete.ipynb

- numpy_network_complete.ipynb

- cupy_network_moduled.ipynb

- numpy_network_moduled.ipynb

### 测试文件

所有测试文件都引用了模板文件，只留出了接口（文件名和路径等）。

- test_net_with_pics.ipynb

  使用与数据集中图片同型的 28*28 尺寸图片进行网络测试。

  \* 请将图片命名为 "{数字}.png" ，例如 "1.png"

- test_with_saved_weights_release.ipynb

  使用测试数据集进行测试，网络权重来自于已保存的权重文件。

### 保存的网络数据

在 saved_data 文件夹中有两组权重数据，分别是我使用 numpy 网络和 cupy 网络训练时得到的。以上两个测试文件演示使用的就是这两组权重数据。

### 手写数字图片

在 my_nums 文件夹中有我手写的 0-9 数字图片，用于测试文件的演示。
