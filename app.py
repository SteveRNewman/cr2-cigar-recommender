#############version used on heroku###################
import streamlit as st
from PIL import Image
import model_app
import pandas as pd

df_desc2 = pd.read_pickle('df_desc2.pkl')
options = list(model_app.df_final_v_3.index)
options2 = list(df_desc2.columns[:-1])

st.title("Cigar Recommender")

img = Image.open('figures/cigar.jpeg')
st.image(img, caption='“Smoking cigars is like falling in love. First, you are attracted by its shape; you stay for its flavor, and you must always remember never, never to let the flame go out.” - Winston Churchill')

st.header('Input your favorite cigar.')
#st.subheader('You can search any cigars listed here, \n https://www.cigarsinternational.com/shop/big-list-of-cigars-brands/1803000/ ')
cigar_id = st.selectbox('Start typing cigar name', options)

st.info('Or search by profile notes')
profile = st.multiselect('Enter profile keywords:', options2)

test = st.button('Search for recommended cigars')
test2 = st.button('Search profiles')



#html_string = "<a href='http://google.com'>google</a>"
#run recommender
if test:
	if cigar_id:
		st.success('Searching for similar cigars')
		query_index = model_app.get_key(val=cigar_id)
		distances, indices = model_app.knn_search.kneighbors(model_app.df_final_v_3.iloc[query_index,:].values.reshape(1,-1), n_neighbors=11)
		for i in range(0,len(distances.flatten())):
			if i == 0:
				st.text('Top Cigar Recommendations for: {}'.format(model_app.df_final_v_3.index[query_index]))
				st.text(' Profile notes: {}'.format(df_desc2['New'][query_index]))
				html_string1 = "<a target='_blank' href='http://google.com/search?q={}+cigar&rlz'>more info</a>".format(model_app.df_final_v_3.index[query_index].replace("'",""))
				st.markdown(html_string1, unsafe_allow_html=True)
			else:
				st.text('{}: {} with a Distance Score of: {}'.format(i, model_app.df_final_v_3.index[indices.flatten()[i]],round(distances.flatten()[i],4)))
				st.text(' Profile notes: {}'.format(df_desc2['New'][i]))
				html_string = "<a target='_blank' href='http://google.com/search?q={}+cigar&rlz'>more info</a>".format(model_app.df_final_v_3.index[indices.flatten()[i]].replace("'",""),round(distances.flatten()[i],4))
				st.markdown(html_string, unsafe_allow_html=True)
		st.success('Finished')

	else:
		st.error('Please enter a valid cigar')

if test2:
	if profile:
		st.success('Searching for similar cigars')
		targets = profile
		df_desc2['pro'] = pd.DataFrame(df_desc2.New.apply(lambda sentence: all(word in sentence for word in targets)))
		st.dataframe(df_desc2['New'][df_desc2['pro']==True].sample(n=10))
		st.success('Finished')

	else:
		st.error('Please enter a valid cigar')
