## 识别图形验证码

针对图形验证码测试相应的识别方案。

OCR识别方案：根据《python3网络爬虫开发实战第二版》中的方法，使用软件`tesserocr`进行识别，测试其效果。

### 环境安装

安装tesserocr库，方法参考：[https://setup.scrape.center/tesserocr](https://setup.scrape.center/tesserocr)。

安装numpy、PIL库。

### 参考案例

书中使用的脚本为：[https://github.com/Python3WebSpider/CrackImageCaptcha/blob/master/main.py](https://github.com/Python3WebSpider/CrackImageCaptcha/blob/master/main.py)。**注意，还需要安装selenium并配置webdriver环境**。与之对应的网站为：[https://captcha7.scrape.center/](https://captcha7.scrape.center/)。

该网站的图形验证码有简单的混淆，但是整个字形相对来说比较规整。

### 测试数据

从某个网站下载了两组图形验证码，人工核对后放在`data`目录下。p1组有56张验证码图片，p2组有50张验证码图片。**每张验证码图片人为标注，可能存在错误，但是概率很低**。预计此验证码比参考案例中的验证码容易识别。

### 图片预处理

图片预处理步骤为：根据阈值将图片转换为灰度图，然后使用OCR识别。其中阈值分别使用了150和200，**随意决定**。

### 测试效果

使用`tesserocr.py`可以对识别效果进行测试。默认不对图片进行处理。

修改`main`函数中的`image = captcha_images[text]`行，可以增加对图片预处理的步骤，可人工调整预处理的阈值。

### 效果统计

测试的结果日志存储在`stats`文件夹下。

分别对不处理、150阈值、200阈值的预测结果进行统计，结果如下：

| 组别 | 阈值   | 总数 | 正确 | 错误 | 正确率 |
| ---- | ------ | ---- | ---- | ---- | ------ |
| p1   | 未处理 | 56   | 14   | 42   | 25%    |
| p1   | 150    | 56   | 20   | 36   | 35.71% |
| p1   | 200    | 56   | 22   | 34   | 39.29% |
| p2   | 未处理 | 50   | 15   | 35   | 30%    |
| p2   | 150    | 50   | 23   | 27   | 46%    |
| p2   | 200    | 50   | 22   | 28   | 44%    |
|      |        |      |      |      |        |

可以看出，经过图片预处理，虽然识别准确率有所提升，但是并不明显。而且最优阈值的确定比较繁琐。使用tesserocr的默认值，对此图形验证码的识别效果并不好。
