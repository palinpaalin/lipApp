import cv2 as cv
import numpy as np
import streamlit as st

import libraries.plugins as plugins

class GUI():

    def __init__(self):

        self.list_of_apps = ['Lipstick Try-on']
        self.guiParam = {}

    def getGuiParameters(self):
        self.common_config()
        self.appDescription()
        return self.guiParam

    def common_config(self, title='Lipstick Try-on APP'):
        st.image("./images/lip.png", width=50)
        st.title(title)

        st.sidebar.markdown("## :arrow_right: Lipstick Colors")

        self.appType = 'Image Applications'

        self.dataSource = 'Upload Image'

        self.selectedApp = 'Lipstick Try-on'

        if self.selectedApp is 'Empty':
            st.sidebar.warning('Select an application from the list')

        self.displayFlag = True

        self.guiParam.update(dict(selectedApp=self.selectedApp,
                                  appType=self.appType,
                                  dataSource=self.dataSource,
                                  displayFlag=self.displayFlag))

    def appDescription(self):
        st.info('This application performs Lipstick color Try-on.')
        self.sidebarLipDetection()

    def sidebarLipDetection(self):

        selection = st.sidebar.radio('', ['RGB', 'Dior 999', '#49 YSL Rose', '#184 Channel Incantevole'])

        st.sidebar.markdown("### :arrow_right: RGB Color Setting")
        vred, vgreen, vblue = 0.0, 0.0, 0.0

        if selection == 'Dior 999':
            red, green, blue = 168, 38, 40
            vred, vgreen, vblue = 168.0, 38.0, 40.0
            st.sidebar.slider('RED', value=vred, min_value=0.0, max_value=255.00, step=1.0)
            st.sidebar.slider('GREEN', value=vgreen, min_value=0.0, max_value=255.00, step=1.0)
            st.sidebar.slider('BLUE', value=vblue, min_value=0.0, max_value=255.00, step=1.0)
        elif selection == '#49 YSL Rose':
            red, green, blue = 214, 35, 82
            vred, vgreen, vblue = 214.0, 35.0, 82.0
            st.sidebar.slider('RED', value=vred, min_value=0.0, max_value=255.00, step=1.0)
            st.sidebar.slider('GREEN', value=vgreen, min_value=0.0, max_value=255.00, step=1.0)
            st.sidebar.slider('BLUE', value=vblue, min_value=0.0, max_value=255.00, step=1.0)
        elif selection == '#184 Channel Incantevole':
            red, green, blue = 200, 15, 46
            vred, vgreen, vblue = 200.0, 15.0, 46.0
            st.sidebar.slider('RED', value=vred, min_value=0.0, max_value=255.00, step=1.0)
            st.sidebar.slider('GREEN', value=vgreen, min_value=0.0, max_value=255.00, step=1.0)
            st.sidebar.slider('BLUE', value=vblue, min_value=0.0, max_value=255.00, step=1.0)
        else:
            red = st.sidebar.slider('RED', value=vred, min_value=0.0, max_value=255.00, step=1.0)
            green = st.sidebar.slider('GREEN', value=vgreen, min_value=0.0, max_value=255.00, step=1.0)
            blue = st.sidebar.slider('BLUE', value=vblue, min_value=0.0, max_value=255.00, step=1.0)

        self.guiParam.update(dict(confThreshRed=red, confThreshGreen=green, confThreshBlue=blue))

class AppManager:

    def __init__(self, guiParam):
        self.param = None
        self.guiParam = guiParam
        self.selectedApp = guiParam['selectedApp']
        self.objApp = self.setupApp()

    def setupApp(self):
        if self.selectedApp == 'Lipstick Try-on':

            self.param = self.guiParam
            self.objApp = plugins.Lip_Detection(self.param)

        else:
            raise Exception('[Error] Please select one of the listed application')

        return self.objApp

    def process(self, frame):
        return self.objApp.run(frame)

class DataManager:
    def __init__(self, guiParam):
        self.guiParam = guiParam
        self.image = None
        self.data = None

    def load_image_source(self):
        if self.guiParam["dataSource"] == 'Upload Image':

            @st.cache(allow_output_mutation=True)
            def load_image_from_upload(file):
                return cv.imdecode(np.fromstring(file.read(), np.uint8), 1)

            file_path = st.file_uploader('Upload an image', type=['png', 'jpg', 'jpeg'])

            if file_path is not None:
                self.image = load_image_from_upload(file_path)
            elif file_path is None:
                st.error("Please upload a valid image ('png', 'jpg', 'jpeg)")
                raise ValueError("[Error] Please upload a valid image ('png', 'jpg', 'jpeg)")

        else:
            raise ValueError("Please select one source from the list")

        return self.image


    def load_image_or_video(self):
        """
        Handle the data input from the user parameters
        """
        if self.guiParam['appType'] == 'Image Applications':
            self.data = self.load_image_source()

        else:
            raise ValueError('[Error] Please select of the two Application pipelines')

        return self.data



