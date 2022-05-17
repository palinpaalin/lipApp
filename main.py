import streamlit as st

from libraries.utils import GUI, AppManager, DataManager

def imageWebApp(guiParam):
    conf = DataManager(guiParam)
    image = conf.load_image_or_video()

    st.image(AppManager(guiParam).process(image), channels="BGR", use_column_width=True)

def main():
    guiParam = GUI().getGuiParameters()

    if guiParam['appType'] == 'Image Applications':
        if guiParam["selectedApp"] is not 'Empty':
            imageWebApp(guiParam)

    else:
        raise st.ScriptRunner.StopException

if __name__ == "__main__":
    main()
