# 智绘乳癌——基于人工智能的乳腺癌免疫组化图像生成（网页端）

### 2024第九届全国大学生生物医学工程竞赛参赛作品 

#### 作品ID：7110

## 项目背景

本项目旨在利用人工智能技术改进乳腺癌的诊断和治疗过程。由于临床上对肿瘤的精准诊疗离不开免疫组化染色，而相比于临床常见的苏木精-伊红染色，免疫组化染色成本高昂、技术要求高、时间消耗相对较多。因此，本项目设计并实现了一个生成式的深度学习模型，用以从苏木精-伊红染色的乳腺癌组织病理图像中生成可靠的免疫组化染色乳腺癌组织病理图像。

## 项目简述

本项目参与了第九届全国大学生生物医学工程竞赛。此仓库中的内容是项目的网页展示端，提供了在线生成图片的功能，同时对项目内容进行展示。

## 仓库结构

- index.html 项目网页的主页

- details.html 项目内容详情网页

- header.html 顶部导航

- footer.html 页脚

- static/js 网页所使用的js脚本

- static/css 网页UI所依赖的CSS风格文件

- static/images 网页中的静态图片

- static/pdfs 论文和海报

- generate 生成IHC图像所需的python脚本及模型

## 关于generate目录的说明

generate目录中的文件应当部署在具有一定计算能力的服务器上，使用```python3 getpic.py```运行即可。若需持续运行，可以使用命令```nohup python3 getpic.py > getpic.log 2>&1 &```。

getpic.py中使用了Flask库来对外提供接口。接口提供在5000端口上，接受的请求格式为POST，必须包含字段file及对应的文件。接口返回的格式为Blob（image/png），需要前端采取一定操作对返回的数据流进行处理。

在static/js/index.js中，需要修改接口地址为正确的图片接口地址。由于许多计算服务器没有公网IP，部署时可能需要采用内网穿透工具。参考[FRP-Python](https://github.com/usualheart/frp-python)

## 其他说明

本仓库部署在Github Pages上并采取CNAME进行了域名跳转，访问网址是<http://bme.xjtu.store>。

网页部分版权声明如下：

<p>
  This page was built using the <a href="https://github.com/eliahuhorwitz/Academic-project-page-template" target="_blank">Academic Project Page Template</a> which was adopted from the <a href="https://nerfies.github.io" target="_blank">Nerfies</a> project page.
   <br> This website is licensed under a <a rel="license"  href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative
  Commons Attribution-ShareAlike 4.0 International License</a>.
</p>