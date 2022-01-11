import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')

st.set_page_config(page_title="MovieFlix Recommendation Site",page_icon=':clapper:',layout="wide")
def access_json(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    else:
        return r.json()

# The Dataset:
final = pd.read_csv("Final_Movies.csv")
vectors = cv.fit_transform(final["tags"]).toarray()
similar = cosine_similarity(vectors)


# Movies Poster API:
api_key = "6071765730597d99db369b9226ada632"

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=6071765730597d99db369b9226ada632&language=en-US".format(movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data["poster_path"]

def get_names_of_movies(index):
    return final.iloc[index]["title"]

def Recommend(movie):
    movie_index = final[final["title"] == movie].index[0]
    distances = similar[movie_index]
    ans = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    name = []
    recommended_posters = []
    for i in ans[:11]:
        movie_id = final.iloc[i[0]]["id"]
        name.append(get_names_of_movies(i[0]))
        # Fetch Movie Posters:
        recommended_posters.append(fetch_poster(movie_id))
    name.pop(0)
    recommended_posters.pop(0)
    return name,recommended_posters


logo = access_json("https://assets3.lottiefiles.com/packages/lf20_khzniaya.json")
heading = access_json("https://assets3.lottiefiles.com/packages/lf20_itjl9rou.json")


movie_names = list(final["title"])
st_lottie(heading, height=300)
st.subheader("Recommending Best Movies For You :tada:")
st.write("---")
left_col,right_col = st.beta_columns(2)
with left_col:
    selected_name = st.selectbox("Select The Movie:",movie_names)
    with right_col:
        st_lottie(logo, height=200)
if st.button("Recommend Me"):
    title = '<p style="font-family:Verdana; color:#ff66cc; font-size: 38px;">Top Picks For You: <hr></p>'
    st.markdown(title, unsafe_allow_html=True)
    names,posters = Recommend(selected_name)
    st.write("---")
    st.subheader(f"As you have watched {selected_name}: ")
    left_col, middle_col,right_col = st.beta_columns(3)
    with left_col:
        st.write(names[0])
        st.image(posters[0],width=180)
        st.write(names[1])
        st.image(posters[1], width=180)
        st.write(names[2])
        st.image(posters[2], width=180)
    with middle_col:
        st.write(names[3])
        st.image(posters[3], width=180)
        st.write(names[4])
        st.image(posters[4], width=180)
        st.write(names[5])
        st.image(posters[5], width=180)

    with right_col:
        st.write(names[6])
        st.image(posters[6], width=180)
        st.write(names[7])
        st.image(posters[7], width=180)
        st.write(names[8])
        st.image(posters[8], width=180)



