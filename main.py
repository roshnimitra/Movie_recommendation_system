import streamlit as st
import pickle
import zipfile
import os

# Set page configuration
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="centered"
)

# Cache the data loading function to avoid reloading on every interaction
@st.cache_data
def load_data():
    """Load movie list and similarity data"""
    # Load the movie list
    movie_list = pickle.load(open('movie_list.pkl', 'rb'))
    
    # Extract similarity.pkl from the zip file
    zip_path = 'similarity.zip'
    extract_path = 'temp_extracted'
    
    # Create extraction directory if it doesn't exist
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
    
    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    # Load similarity data
    similarity_path = os.path.join(extract_path, 'similarity.pkl')
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    
    # Normalize movie titles to lower case for easier matching
    movie_list['title_normalized'] = movie_list['title'].str.strip().str.lower()
    
    return movie_list, similarity

def get_recommendations(movie_name, movie_list, similarity):
    """Get movie recommendations based on similarity"""
    movie_name_normalized = movie_name.strip().lower()
    filtered_movies = movie_list[movie_list['title_normalized'] == movie_name_normalized]

    if filtered_movies.empty:
        return None, f"Movie '{movie_name}' not found in the dataset."

    movie_index = filtered_movies.index[0]
    distances = similarity[movie_index]
    selected_movie = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended = [movie_list.iloc[i[0]].title for i in selected_movie]
    
    return recommended, None

# Load data
try:
    movie_list, similarity = load_data()
    
    # Main app interface
    st.title("🎬 Movie Recommendation System")
    st.write("Enter a movie name to get personalized recommendations!")
    
    # Create input field
    movie_name = st.text_input(
        "Movie Name:",
        placeholder="e.g., The Dark Knight, Avatar, Inception..."
    )
    
    # Add a submit button
    if st.button("Get Recommendations", type="primary"):
        if movie_name:
            with st.spinner("Finding similar movies..."):
                recommendations, error = get_recommendations(movie_name, movie_list, similarity)
            
            if error:
                st.error(error)
                
                # Show some sample movie titles as suggestions
                st.info("Here are some movies from our database:")
                sample_movies = movie_list['title'].head(10).tolist()
                for movie in sample_movies:
                    st.write(f"• {movie}")
            else:
                st.success(f"Movies similar to '{movie_name}':")
                
                # Display recommendations in a nice format
                for i, movie in enumerate(recommendations, 1):
                    st.write(f"{i}. **{movie}**")
        else:
            st.warning("Please enter a movie name!")
    
    # Add some information about the app
    with st.expander("ℹ️ About this app"):
        st.write("""
        This movie recommendation system uses machine learning to find movies similar to your input.
        
        **How it works:**
        - Enter the name of a movie you like
        - The system finds movies with similar characteristics
        - Get 5 personalized recommendations
        
        **Tips:**
        - Make sure to spell the movie name correctly
        - Try popular movies for better results
        - The search is case-insensitive
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("*Built with Streamlit* 🚀")

except FileNotFoundError as e:
    st.error(f"Required files not found: {e}")
    st.info("Please make sure 'movie_list.pkl' and 'similarity.zip' are in the same directory as this script.")
except Exception as e:
    st.error(f"An error occurred while loading data: {e}")
    st.info("Please check your data files and try again.")