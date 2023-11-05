
## SECTION 1 : PROJECT TITLE
## Eye Disease Detection System

## SECTION 2 : Abstract
According to the World Health Organization (WHO), eye diseases have emerged as the third most significant health hazard following cancer and cardiovascular diseases, significantly impacting people's quality of life. Reports indicate approximately 160 million visually impaired individuals globally. Half of these cases result from cataracts, with the remainder caused by conditions such as glaucoma, diabetes-related issues, congenital disorders, and other eye ailments. Furthermore, there's a profound scarcity of ophthalmologists worldwide, and this deficit continues to widen as the number of eye specialists remains insufficient to meet the growing needs of patients with eye diseases. Consequently, many individuals suffering from eye diseases often seeking medical attention only at later stages, resulting in irreversible consequences.  Hence, the development of an effective method for early detection and classification of common eye diseases is crucial to address this pressing need.

In order to achieve the goal of early detection and classification of eye diseases, this project decided to design a website for an eye disease detection system based on deep learning network with open source eye fundus image dataset which contains four types of eye images (Normal, Diabatic, Glaucoma, Cataract) as our data while employing the cup-to-disc ratio as classification criteria.

The two CNN models used in this project, YOLO and SSD, both have good performance in speed and accuracy. The two models were respectively used to detect the same eye disease data, and the comparison showed that YOLOv5 obtained a good mAP of 0.955 in eye disease detection. It can basically achieve the purpose of rapid diagnosis in the medical field. At the same time, the website developed by this project can also provide users with the basic information and treatment plans of three kinds of eye diseases, which can save the time of diagnosis to a certain extent and solve the problem of imbalance in the number of doctors and patients.

## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  |
| :------------ |:---------------:|
| Chen Haoquan | A0286061E | 
| Liang Jinning | A0285754N | 
| Cui Mengchen | A0285690R |
| Huang Yifei  | A0285719M |

---

## SECTION 4 : VIDEO PRESENTATION
https://youtu.be/EoZEbx4cid0

---

## SECTION 5 : USER GUIDE

### Environment
> Python 3.9
> pytorch

### clone project
> download our project from github

### Enter directory
> cd ./yoloV5-7.0
> pip install -r requirements.txt

### Avoid environmental conflicts
> pip install werkzeug==2.3.6
> pip install tokenizer==3.4.3

### the project
> cd ./yolov5-7.0/website
> python app.py

> **Go to URL using web browser** http://192.168.18.8:5000

