# Open-Sora-Dataset

[[Project Page]](https://pku-yuangroup.github.io/Open-Sora-Plan/) [[中文主页]](https://pku-yuangroup.github.io/Open-Sora-Plan/blog_cn.html)

:bulb:  Welcome to the Open-Sora-DataSet project! In the current process of training multimodel video models, the quality of the data determines the upper limit of the model performance. To build a high-quality video dataset for the open-source world, we started this project. 💪 

We warmly welcome you to join us! Let's contribute to the open-source world together! Thank you for your support and contribution. :heart:  

:bulb:  欢迎来到Open-Sora-DataSet项目！在当前的视频大模型训练过程中，数据的质量决定了模型性能的上限。为给开源世界构建一个高质量的视频数据，我们发起了这个项目。💪 

我们非常欢迎您的加入！让我们共同为开源的世界贡献力量！感谢您的支持和贡献。 :heart: 

<div style="display: flex; justify-content: center; align-items: center;"> 
  <img src="assets/we-need-you.jpg" width=250> 
</div>

## 视频分割(split)
### 对于转场丰富的视频
利用[panda-70m](https://github.com/snap-research/Panda-70M/tree/main/splitting)处理

### 对于无转场视频
1. Clone this repository and navigate to Open-Sora-Plan folder
```
git clone https://github.com/PKU-YuanGroup/Open-Sora-Plan
cd Open-Sora-Plan
```
2. Install the required packages
```
conda create -n opensora python=3.8 -y
conda activate opensora
pip install -e .
```
3. Split video script
```
git clone https://github.com/shaodong233/open-sora-Dataset.git
python split/no_transition.py --video_json_file /path/to/your_video /path/to/save
```


If you want to know more, check out [Requirements and Installation](https://github.com/PKU-YuanGroup/Open-Sora-Plan?tab=readme-ov-file#%EF%B8%8F-requirements-and-installation)

## Acknowledgement 👍
Qingdao Weiyi Network Technology Co., Ltd.: Thank you very much for providing us with valuable data
