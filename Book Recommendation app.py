import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

## Data loading function
Author_sorted = pd.read_csv('Author_data.csv')
Age_sorted = pd.read_csv('Age_data.csv')

st.set_page_config(layout="centered")  # centered, wide

@st.cache(allow_output_mutation=True)
def author_age_based(title, Age_group, number, Age_sorted=Age_sorted):
    Author_df = Author_sorted.loc[Author_sorted['Title'] == title]['Author'].unique()[0]
    Author_by_title = Author_sorted.loc[(Author_sorted['Author'] == Author_df)].sort_values(by='weighted_average', ascending=False)
    Age_df = Age_sorted.loc[Age_sorted['Age_group'] == Age_group]['Author'].unique()
    title_by_age = Age_sorted[Age_sorted['Author'].isin(Age_df)].sort_values(by='weighted_average', ascending=False)
    
    # Exclude the original title from the recommendations
    recommendations = title_by_age[title_by_age['Title'] != title]
    top_recommendations = recommendations.head(number)
    
    print(f'For {Age_group} age demographic')  
    print(f'The author of the book {title} is {Author_df}\n')
    print(f'Here are the top {number} books from the same author\n')
    top_recommendations = top_recommendations[['Title', 'Author', 'weighted_average', 'Age_group']]
    return top_recommendations

### Loading objects 
image = Image.open("Books_HD_(8314929977).jpg")

st.image(image, use_column_width=True)

### Instruction text 
st.write('Welcome: Please fill in the details of the book in the left sidebar and click on the button below!')

### Defining the content of the bar
Book_title = Age_sorted['Title'].unique().tolist()
Age_Category = Age_sorted['Age_group'].unique().tolist()

### Setting the side bars 
Book_name = st.sidebar.selectbox("Select Title", Book_title)
Age_group = st.sidebar.selectbox("Your Age Group", Age_Category)
Number = st.sidebar.number_input("How many recommendations", min_value=1, max_value=10, step=1)

# Generate recommendations
if st.sidebar.button("Get Recommendations"):
    new_recommendation = author_age_based(Book_name, Age_group, Number)

    ## Plot this for every recommendation made. 
    st.write('See the most ratings of these books:')
    df = new_recommendation
    fig = px.bar(df, x='Title', y='weighted_average',
                 hover_data=['Author', 'Age_group'], color='weighted_average',
                 labels={'weighted_average': 'Weighted Average'}, height=400)
    fig.update_layout(
        title=(f"Top {Number} books recommended for '{Book_name}' title"),
        xaxis_title=('Book Titles'),
        yaxis_title=('Weighted Average')
    )
    st.plotly_chart(fig)