import pickle
import streamlit as st
import requests
import time

# CSS for colorful animation and background animation
css = """
    <style>
        @keyframes changeColor {
            0% { color: #FF5733; }
            25% { color: #FFC300; }
            50% { color: #DAF7A6; }
            75% { color: #C70039; }
            100% { color: #900C3F; }
        }
        .animated-text {
            animation: changeColor 5s infinite alternate;
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-30px);
            }
            60% {
                transform: translateY(-15px);
            }
        }
        .bounce-emoji {
            animation: bounce 2s infinite;
        }
        /* Background animation */
        body {
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100"><text x="0" y="50" font-family="Arial" font-size="45" fill="%23FF5733">🎬</text></svg>') repeat,
                        url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100"><text x="0" y="50" font-family="Arial" font-size="45" fill="%23FF5733">🍿</text></svg>') repeat;
            background-size: 100px 100px;
            animation: gradientBG 10s ease infinite;
        }
        @keyframes gradientBG {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
    </style>
"""

# Inject the CSS into the Streamlit app
st.markdown(css, unsafe_allow_html=True)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=4c48ecff39cbd395ec979b149c63759e&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


# Header
st.title('🎬 Movie Recommender System 🍿')

# Footer with icons


movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('🚀 Show Recommendation 🚀'):
    with st.spinner('🔍 Fetching Recommendations...'):
        recommended_movie_names, recommended_movie_posters = recommend(
            selected_movie)
        time.sleep(2)  # Simulate a delay for demonstration purposes

    cols = st.columns(5)  # Generate five columns
    for i, col in enumerate(cols):
        col.markdown(
            f'<div class="animated-text">{recommended_movie_names[i]}</div>',
            unsafe_allow_html=True)
        col.image(recommended_movie_posters[i])

    st.success('🎉 Enjoy your movie recommendations! 🎉')
    
    st.markdown(
        """
    <footer style="background-color:#3f48cc;padding:10px; text-align:center;">
        <p style="font-size:14px; color:#ffffff;">Made with ❤️ by Charan Sai Reddy W</p>
        <p>
            <a href="https://www.linkedin.com/in/charan-sai-reddy-w/" target="_blank">
                <img src="https://img.icons8.com/fluent/48/000000/linkedin.png"/>
            </a>
            <a href="mailto:charansaireddywudaru@gmail.com">
                <img src="https://img.icons8.com/fluent/48/000000/gmail.png"/>
            </a>
            <a href="tel:+16305656972">
                <img src="https://img.icons8.com/fluent/48/000000/phone.png"/>
            </a>
        </p>
    </footer>
    """,
        unsafe_allow_html=True
    )
