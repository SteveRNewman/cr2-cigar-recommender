#############version used on heroku###################
import streamlit as st
from PIL import Image
import model_app
import pandas as pd

st.title("Cigar Recommender")

img = Image.open('figures/cigar.jpeg')
st.image(img, caption='“Smoking cigars is like falling in love. First, you are attracted by its shape; you stay for its flavor, and you must always remember never, never to let the flame go out.” - Winston Churchill')

st.header('Input your favorite cigar.')
#st.subheader('You can search any cigars listed here, \n https://www.cigarsinternational.com/shop/big-list-of-cigars-brands/1803000/ ')
cigar_id = st.text_input('Enter cigar name.', '')

st.info('Or search by profile notes')
profile = st.text_input('Enter profile keyword:', '')

test = st.button('Search for recommended cigars')


#run recommender
if test:
	if cigar_id:
		st.success('Searching for similar cigars')
		query_index = model_app.get_key(val=cigar_id)
		distances, indices = model_app.knn_search.kneighbors(model_app.df_final_v_3.iloc[query_index,:].values.reshape(1,-1), n_neighbors=11)
		for i in range(0,len(distances.flatten())):
			if i == 0:
				st.text('Top Cigar Recommendations for: {}'.format(model_app.df_final_v_3.index[query_index]))
			else:
				st.text('{}: {} with a Distance Score of: {}'.format(i, model_app.df_final_v_3.index[indices.flatten()[i]],round(distances.flatten()[i],4)))
		st.success('Finished')

	else:
		st.error('Please enter a valid cigar')
