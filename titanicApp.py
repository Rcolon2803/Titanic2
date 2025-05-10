import streamlit as st
import pickle

# UI-- User Interface, how things look like.
# UX--- User Experience, how does the user feel interacting with the app

# Set the title and display an image for branding 
st.title('Titanic Survival Prediction App!')
from PIL import Image
import io

img = Image.open("Titanicimage.jpeg")
img_bytes = io.BytesIO()
img.save(img_bytes, format= "jpeg")
st.image(img_bytes, caption="Predict Survival on the Titanic")

#Load the pretrained model
with open('titanicpickle.pkl', 'rb') as picklefile:
    model = pickle.load(picklefile)


#Function to make predictions
def PredictionsFunction(Pclass, Sex, Age, Sibsp, Parch, Fare, Embarked):
    try:
        prediction = model.predict([[Pclass, Sex, Age, Sibsp, Parch, Fare, Embarked]])
        return 'Survived' if prediction[0] ==1 else 'Did not survive'
    except Exception as e:
        return f'Error:{str(e)}'
    
#Sidebar for Instructions
st.sidebar.header('How to Use!')    
st.sidebar.markdown(""" 
1. Enter the Passenger Details in the format
2. Click 'Predict' to see the Survival Results.body
3. Adjust Values to Test Different Scenarious.                    
                    """)

st.sidebar.info('Example: A thirty years old male, third class, thirty dollar fare, traveling alone from port Southempton.')

#Main Input Form
def main():
    st.subheader('Enter Passenger Details:')
    col1, col2, = st.columns(2)
    #Organize inputs in columns
    with col1:
        Pclass = st.selectbox('Passenger Class:', options = [1,2,3], format_func = lambda X: f'class{X}')
        Sex = st.radio('Sex', options = ['male', 'female'])   
        Age= st.slider('Age:', min_value= 0, max_value= 100, value=30)
    with col2:
        Sibsp = st.slider('Siblings/Spouse Aboard:', min_value= 0, max_value=10, value=0)
        Parch = st.slider('Parents/Children Aboard:',min_value= 0, max_value=10, value=0)
        Fare = st.slider('Fare($)',min_value= 0.0, max_value=500.0, value=50.0, step= 0.1 )
        Embarked = st.radio('Port of Embarked:', options = ['C', 'Q', 'S'], format_func= lambda X : f'port{X}')

#Convert Categrical  inputs to numeric values
    Sex = 1 if Sex== 'female' else 0 
    Embarked= {'C': 0, 'Q':1, 'S':2} [Embarked] 

#Button for prediction
    if st.button('predict'):
     result = PredictionsFunction(Pclass, Sex, Age, Sibsp, Parch, Fare, Embarked)

     if result == 'Survived':
         st.markdown("**Congratualtions! The Passenger Survived!**")
     else:
        st.markdown("Unfortunatly, the Passenger Did not Survive.")
# Run the main function
if __name__=='__main__':
    main()         


