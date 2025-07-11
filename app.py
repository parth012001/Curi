import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_processor import BeautyDataProcessor
from conversational_engine import ConversationalEngine
import time

# Page configuration
st.set_page_config(
    page_title="Curi - Intelligent Beauty Product Research",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B9D;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4A4A4A;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #FF6B9D;
    }
    .user-message {
        background-color: #F0F8FF;
        border-left-color: #4A90E2;
    }
    .bot-message {
        background-color: #FFF5F5;
        border-left-color: #FF6B9D;
    }
    .product-card {
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .rating-stars {
        color: #FFD700;
        font-size: 1.2rem;
    }
    .insight-badge {
        background-color: #E8F5E8;
        color: #2E7D32;
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .negative-insight {
        background-color: #FFEBEE;
        color: #C62828;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = None
if 'conversational_engine' not in st.session_state:
    st.session_state.conversational_engine = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

def load_data():
    """Load and process the beauty data"""
    if st.session_state.data_loaded:
        return
        
    with st.spinner("Loading beauty product data... This may take a few minutes for the first time."):
        # Initialize data processor
        data_processor = BeautyDataProcessor()
        
        # Try to load processed data first
        if not data_processor.load_processed_data():
            # Load and process data from scratch
            data_processor.load_data()
            data_processor.preprocess_data()
            data_processor.create_product_features()
            data_processor.build_tfidf_matrix()
            data_processor.build_similarity_matrices()
            data_processor.save_processed_data()
        
        # Initialize conversational engine
        conversational_engine = ConversationalEngine(data_processor)
        
        # Store in session state
        st.session_state.data_processor = data_processor
        st.session_state.conversational_engine = conversational_engine
        st.session_state.data_loaded = True

def display_product_card(product, index):
    """Display a product card with all relevant information"""
    with st.container():
        st.markdown(f"""
        <div class="product-card">
            <h4>{product['title']}</h4>
            <p><strong>Brand:</strong> {product.get('store', 'Unknown')}</p>
            <p><strong>Rating:</strong> 
                <span class="rating-stars">{'⭐' * int(product.get('average_rating', 0))}</span>
                {product.get('average_rating', 0):.1f}/5 ({product.get('rating_number', 0)} reviews)
            </p>
        """, unsafe_allow_html=True)
        
        # Display insights if available
        if 'insights' in product and product['insights']:
            st.markdown("<strong>User Insights:</strong>")
            for insight in product['insights']:
                if "👎" in insight:
                    st.markdown(f'<span class="insight-badge negative-insight">{insight}</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<span class="insight-badge">{insight}</span>', unsafe_allow_html=True)
        
        # Add action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"View Details", key=f"details_{index}"):
                show_product_details(product)
        with col2:
            if st.button(f"Find Similar", key=f"similar_{index}"):
                show_similar_products(product['asin'])

def show_product_details(product):
    """Show detailed product information"""
    st.markdown("### Product Details")
    
    # Get full product information
    full_product = st.session_state.data_processor.get_product_by_asin(product['asin'])
    
    if full_product is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Product Information:**")
            st.write(f"**Title:** {full_product['title']}")
            st.write(f"**Brand:** {full_product.get('store', 'Unknown')}")
            st.write(f"**Category:** {full_product.get('main_category', 'Unknown')}")
            st.write(f"**Average Rating:** {full_product.get('average_rating', 0):.1f}/5")
            st.write(f"**Number of Ratings:** {full_product.get('rating_number', 0)}")
            
            # Display details if available
            if full_product.get('details'):
                st.write("**Product Details:**")
                for key, value in full_product['details'].items():
                    st.write(f"**{key}:** {value}")
        
        with col2:
            # Show recent reviews
            reviews = st.session_state.data_processor.get_reviews_by_asin(product['asin'], limit=5)
            if not reviews.empty:
                st.write("**Recent Reviews:**")
                for _, review in reviews.iterrows():
                    st.write(f"**{review['title']}** ({review['rating']}/5)")
                    st.write(f"*{review['text'][:200]}...*")
                    st.write("---")

def show_similar_products(asin):
    """Show similar products"""
    st.markdown("### Similar Products")
    
    similar_products = st.session_state.data_processor.get_similar_products(asin, top_k=5)
    
    if similar_products:
        for i, product in enumerate(similar_products):
            display_product_card(product, f"similar_{i}")
    else:
        st.write("No similar products found.")

def main():
    # Header
    st.markdown('<h1 class="main-header">✨ Curi</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your Intelligent Beauty Product Research Assistant</p>', unsafe_allow_html=True)
    
    # Load data
    load_data()
    
    if not st.session_state.data_loaded:
        st.error("Failed to load data. Please check your data files.")
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Quick Actions")
        
        if st.button("Show Popular Products"):
            st.session_state.chat_history.append({
                'user': "Show me popular products",
                'bot': "Here are some of the most popular beauty products based on user ratings:"
            })
            st.session_state.show_popular = True
            
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.session_state.show_popular = False
            
        st.markdown("### 💡 Example Queries")
        st.markdown("""
        - "I need a gentle cleanser for sensitive skin"
        - "Find me anti-aging products"
        - "Recommend moisturizers for dry skin"
        - "Show me products for acne-prone skin"
        - "I want hydrating serums"
        """)
        
        st.markdown("### 📊 Data Stats")
        if st.session_state.data_processor:
            stats = st.session_state.data_processor
            st.write(f"**Products:** {len(stats.products_df):,}")
            st.write(f"**Reviews:** {len(stats.reviews_df):,}")
            st.write(f"**Ratings:** {len(stats.ratings_df):,}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Chat with Curi")
        
        # Chat input
        user_query = st.text_input(
            "Describe what you're looking for in natural language:",
            placeholder="e.g., 'I need a gentle cleanser for sensitive skin'",
            key="user_input"
        )
        
        if st.button("Ask Curi", key="ask_button") or user_query:
            if user_query:
                # Add user message to chat
                st.session_state.chat_history.append({
                    'user': user_query,
                    'bot': None
                })
                
                # Get response from conversational engine
                with st.spinner("Analyzing your request..."):
                    response = st.session_state.conversational_engine.get_conversational_response(user_query)
                
                # Add bot response to chat
                st.session_state.chat_history[-1]['bot'] = response['response']
                st.session_state.current_recommendations = response['recommendations']
        
        # Display chat history
        for i, chat in enumerate(st.session_state.chat_history):
            if chat['user']:
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {chat['user']}
                </div>
                """, unsafe_allow_html=True)
            
            if chat['bot']:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>Curi:</strong> {chat['bot']}
                </div>
                """, unsafe_allow_html=True)
        
        # Display recommendations if available
        if hasattr(st.session_state, 'current_recommendations') and st.session_state.current_recommendations:
            st.markdown("### 🎯 Your Personalized Recommendations")
            
            for i, product in enumerate(st.session_state.current_recommendations):
                display_product_card(product, i)
        
        # Display popular products if requested
        if hasattr(st.session_state, 'show_popular') and st.session_state.show_popular:
            st.markdown("### 🌟 Popular Products")
            
            popular_products = st.session_state.data_processor.get_popular_products(top_k=10)
            
            for i, product in enumerate(popular_products):
                display_product_card(product, f"popular_{i}")
    
    with col2:
        st.markdown("### 📈 Insights")
        
        if st.session_state.data_processor:
            # Rating distribution
            ratings_data = st.session_state.data_processor.products_df['average_rating'].dropna()
            
            fig = px.histogram(
                ratings_data,
                nbins=20,
                title="Product Rating Distribution",
                labels={'value': 'Average Rating', 'count': 'Number of Products'}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Top brands
            brand_counts = st.session_state.data_processor.products_df['store'].value_counts().head(10)
            fig2 = px.bar(
                x=brand_counts.values,
                y=brand_counts.index,
                orientation='h',
                title="Top Brands by Product Count",
                labels={'x': 'Number of Products', 'y': 'Brand'}
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main() 