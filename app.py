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

test3 = st.radio('Set Option',['Search for recommended cigars', 'Search profiles','About'])
if test3 == ('About'):
	st.header('Info about the model - working on it. Will have features by type in sidebar with buttons to expand and displayed as graphs in the main section.')
	wrapper = st.sidebar.button('View Wrapper Types')
	filler = st.sidebar.button('View Filler Types')
	strength = st.sidebar.button('View Strength Types')
	st.sidebar.write('etc.')
	test = None
	test2 = None
	html_string1 = '<a href = "mailto: stevernewman@gmail.com">Contact Steve</a>'
	st.markdown(html_string1, unsafe_allow_html=True)
elif test3 == ('Search profiles'):

		st.info('Select any number of profile keywords. Then select "Search cigar by profile" multiple times for new matches.')
		profile = st.multiselect('Enter profile keywords:', options2)
		test2 = st.button('Search cigars by profile')
		test = None
else:
	st.header('Input your favorite cigar. 1876 Reserve is just a place holder, no need to delete it. Click in the box and your input will autofill.')
	cigar_id = st.selectbox('Start typing cigar name', options)
	test = st.button('Search cigars')
	test2 = None



if test:
	if cigar_id:
		st.success('Distance scores closer to zero are better matches because they have more similar features.')
		query_index = model_app.get_key(val=cigar_id)
		distances, indices = model_app.knn_search.kneighbors(model_app.df_final_v_3.iloc[query_index,:].values.reshape(1,-1), n_neighbors=11)
		for i in range(0,len(distances.flatten())):
			if i == 0:
				st.write('Top Cigar Recommendations for: {}'.format(model_app.df_final_v_3.index[query_index]))
				st.write(' Profile notes: {}'.format(df_desc2['New'][query_index]))
				html_string1 = "<a target='_blank' href='http://google.com/search?q={}+cigar&rlz'>more info</a>".format(model_app.df_final_v_3.index[query_index].replace("'",""))
				st.markdown(html_string1, unsafe_allow_html=True)
			else:
				st.write('{}: {} with a Distance Score of: {}'.format(i, model_app.df_final_v_3.index[indices.flatten()[i]],round(distances.flatten()[i],4)))
				st.write(' Profile notes: {}'.format(df_desc2['New'][i]))
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
		df = pd.DataFrame(df_desc2['New'][df_desc2['pro']==True])
		if len(df)>10:
			df=df.sample(n=10)
		for i in range(len(df)):
			st.write('{}: {}'.format(i+1,df.index[i]))
			st.write('---Profile notes: {}'.format(df["New"][i][:-1]))
			html_string = "<a target='_blank' href='http://google.com/search?q={}+cigar&rlz'>more info</a>".format(df.index[i].replace("'",""))
			st.markdown(html_string, unsafe_allow_html=True)
