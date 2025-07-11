# ✨ Curi - Intelligent Beauty Product Research MVP

**Transform your online shopping experience with intelligent, conversational product research that replaces overwhelming search results with personalized, context-aware recommendations.**

## 🎯 What is Curi?

Curi is an intelligent conversational product research tool that addresses key pain points in online beauty shopping:

- **Poor search relevance** → Context-aware recommendations
- **Choice overload** → Curated, personalized suggestions  
- **Distrust in sponsored content** → Real user insights and expert guidance
- **Complex decision-making** → Natural language queries and simplified results

## 🚀 Key Features

### 💬 Natural Language Understanding
- Ask questions like you're talking to a knowledgeable beauty consultant
- "I need a gentle cleanser for sensitive skin"
- "Find me anti-aging products for dry skin"
- "Recommend moisturizers that won't break me out"

### 🎯 Intelligent Recommendations
- **Semantic Search**: Understands product descriptions, reviews, and user needs
- **Collaborative Filtering**: Recommends products based on similar users' preferences
- **Context-Aware**: Considers skin type, concerns, brand preferences, and effects
- **Real User Insights**: Extracts key themes and sentiments from reviews

### 📊 Rich Product Information
- **Product Details**: Names, brands, categories, specifications
- **User Ratings**: Average ratings and review counts
- **Review Analysis**: Sentiment analysis and key insights
- **Similar Products**: Find alternatives and complementary items

### 🎨 Modern, User-Friendly Interface
- **Chat-like Experience**: Natural conversation flow
- **Product Cards**: Clean, informative product displays
- **Interactive Elements**: View details, find similar products
- **Data Visualization**: Rating distributions and brand insights

## 📁 Data Sources

This MVP uses three comprehensive beauty product datasets:

1. **Product Metadata** (`meta_All_Beauty.jsonl`): 203MB
   - Product titles, descriptions, features
   - Brand information and categories
   - Average ratings and review counts
   - Product specifications and details

2. **User Reviews** (`All_Beauty.jsonl`): 311MB
   - Detailed review text and titles
   - User ratings and timestamps
   - Verified purchase status
   - Helpful vote counts

3. **User Ratings** (`ratings_Beauty.csv`): 82MB
   - User-product interaction matrix
   - 2+ million ratings for collaborative filtering

## 🛠️ Technical Architecture

### Core Components

1. **Data Processor** (`data_processor.py`)
   - Loads and preprocesses all data sources
   - Builds TF-IDF matrices for semantic search
   - Creates similarity matrices for recommendations
   - Handles data persistence for faster loading

2. **Conversational Engine** (`conversational_engine.py`)
   - Natural language processing and intent extraction
   - Feature extraction (skin type, concerns, preferences)
   - Query enhancement and smart filtering
   - Review analysis and insight generation

3. **Web Application** (`app.py`)
   - Streamlit-based modern interface
   - Real-time chat interactions
   - Product visualization and recommendations
   - Data insights and analytics

### Key Technologies

- **Python 3.8+**
- **Streamlit**: Web application framework
- **Scikit-learn**: Machine learning and similarity calculations
- **NLTK & TextBlob**: Natural language processing
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- 4GB+ RAM (for data processing)
- 1GB+ free disk space

### Installation

1. **Clone or download the project files**
   ```bash
   # Ensure you have the data files in the project directory:
   # - meta_All_Beauty.jsonl
   # - All_Beauty.jsonl  
   # - ratings_Beauty.csv
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - Navigate to `http://localhost:8501`
   - The app will load data on first run (may take 2-5 minutes)

## 💡 Example Queries

Try these natural language queries to see Curi in action:

### Basic Searches
- "I need a gentle cleanser for sensitive skin"
- "Find me anti-aging products"
- "Recommend moisturizers for dry skin"

### Specific Concerns
- "Show me products for acne-prone skin"
- "I want hydrating serums"
- "Find products that help with dark spots"

### Brand Preferences
- "Recommend CeraVe products"
- "Show me The Ordinary serums"
- "Find La Roche-Posay moisturizers"

### Effects & Results
- "I want products that are gentle"
- "Find strong exfoliators"
- "Show me soothing products"

## 🎯 MVP Capabilities

### ✅ What Works Now

1. **Natural Language Processing**
   - Understands beauty-related queries
   - Extracts skin type, concerns, preferences
   - Enhances queries with context

2. **Intelligent Recommendations**
   - Semantic search based on product descriptions
   - Collaborative filtering from user ratings
   - Similar product suggestions

3. **User Insights**
   - Sentiment analysis of reviews
   - Key theme extraction
   - Positive/negative insight highlighting

4. **Modern Interface**
   - Chat-like interaction
   - Product cards with ratings
   - Interactive details and similar products

### 🔮 Future Enhancements

1. **Advanced NLP**
   - More sophisticated intent recognition
   - Better context understanding
   - Multi-turn conversations

2. **Enhanced Recommendations**
   - Price-based filtering
   - Ingredient analysis
   - Personalized user profiles

3. **Additional Features**
   - Product comparison tools
   - Shopping list creation
   - Price tracking and alerts

## 📊 Data Processing

The application processes data in stages:

1. **Initial Load** (2-5 minutes on first run)
   - Loads all data sources
   - Preprocesses and cleans data
   - Builds TF-IDF matrices
   - Creates similarity matrices

2. **Cached Loading** (30 seconds on subsequent runs)
   - Loads preprocessed data from cache
   - Maintains all similarity matrices

3. **Real-time Processing**
   - Natural language query processing
   - Dynamic recommendation generation
   - Review analysis and insights

## 🎨 Interface Features

### Main Chat Area
- Natural language input
- Conversational responses
- Product recommendations
- Interactive product cards

### Sidebar
- Quick actions (popular products, clear chat)
- Example queries for inspiration
- Data statistics and insights

### Analytics Panel
- Product rating distributions
- Top brands by product count
- Real-time data insights

## 🔧 Customization

### Adding New Data Sources
1. Update `data_processor.py` to load new data
2. Modify preprocessing in `preprocess_data()`
3. Update feature extraction in `create_product_features()`

### Extending NLP Capabilities
1. Add new keywords to `beauty_keywords` in `conversational_engine.py`
2. Enhance intent patterns in `extract_intent()`
3. Improve feature extraction in `extract_features()`

### UI Customization
1. Modify CSS styles in `app.py`
2. Add new visualization components
3. Enhance product card displays

## 🐛 Troubleshooting

### Common Issues

1. **Memory Issues**
   - Ensure 4GB+ RAM available
   - Close other applications
   - Consider reducing data sample size

2. **Slow Loading**
   - First run takes 2-5 minutes
   - Subsequent runs use cached data
   - Check disk space for cache files

3. **Data Loading Errors**
   - Verify all three data files are present
   - Check file permissions
   - Ensure sufficient disk space

### Performance Tips

1. **For Development**
   - Use smaller data samples for faster iteration
   - Reduce TF-IDF features in `data_processor.py`
   - Limit similarity matrix size

2. **For Production**
   - Use preprocessed data cache
   - Implement database storage
   - Add Redis caching for recommendations

## 📈 Success Metrics

This MVP demonstrates:

- **Natural Language Understanding**: Successfully interprets beauty-related queries
- **Personalized Recommendations**: Provides relevant, context-aware suggestions
- **User Trust**: Shows real user insights and ratings
- **Simplified Experience**: Reduces choice overload with curated results

## 🤝 Contributing

To enhance this MVP:

1. **Data Enhancement**
   - Add more product metadata
   - Include pricing information
   - Add ingredient lists

2. **NLP Improvements**
   - Better intent recognition
   - More sophisticated query understanding
   - Multi-language support

3. **UI/UX Enhancements**
   - Mobile-responsive design
   - Advanced filtering options
   - Product comparison tools

## 📄 License

This project is for educational and demonstration purposes. The beauty product data is sourced from Amazon product reviews and is used in accordance with fair use principles.

---

**Built with ❤️ for transforming the online shopping experience** 