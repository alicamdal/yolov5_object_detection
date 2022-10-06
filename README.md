# Conference Paper and Citation
This study can be accessed through this [paper](https://www.rpsonline.com.sg/proceedings/esrel2022/pdf/S30-05-605.pdf). This repo open to free use. If you have used it, please add the citation to your paper.
# YOLOV5 Based object detection application using Flask
This repo contains Unmanned Surface Vessel control scripts. USV uses Jetson Nano as MCU. The Web server is located in Jetson Nano. Web server shows both original video stream and object detection stream using Flask. Also, USV can be controlled over web server. Motor control codes and joystick control scripts can be found [here](https://github.com/alicamdal/motor_controller_usv). Sample screenshot can be seen below.
<br/>
<img src="static/sampless.gif"/>
## Installing Libraries
All required libraries can be found in requirements.txt
```
pip3 install -r requirements.txt
```
## YOLOV5 Model
Mentioned Unmanned Surface Vessel is built to collect trashes on the surface of water. YOLOV5 model that is used for object detection is Yolov5s6. It is trained with custom data set. The given model "yolov5s6_r2.pt" can be used to detect trash.
## Field Test of the USV and the YOLOv5
As can be seen below, model successfully detect object on the water. Full video of the [white bottle](https://www.youtube.com/watch?v=_sDf7WGlZ78) and [orange cylinder box](https://www.youtube.com/watch?v=Xn_QA5a2tJ8) can be found on YouTube.
<br/>
<img src="static/whiteBottle_down.gif"/>
<br/>
<img src="static/orangeBottle_down.gif"/>

