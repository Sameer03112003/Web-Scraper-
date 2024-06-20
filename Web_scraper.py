import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error

# Define a function to scrape data from a single website
def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract Meta Title
        meta_title = soup.title.string if soup.title else 'N/A'
        
        # Extract Meta Description
        meta_description = 'N/A'
        if soup.find('meta', attrs={'name': 'description'}):
            meta_description = soup.find('meta', attrs={'name': 'description'})['content']
        elif soup.find('meta', attrs={'property': 'og:description'}):
            meta_description = soup.find('meta', attrs={'property': 'og:description'})['content']
        
        # Extract Social Media Links
        social_media_links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if any(sm in href for sm in ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com']):
                social_media_links.append(href)
        
        # Truncate social media links to fit within VARCHAR(255)
        social_media_links_str = ','.join(social_media_links)
        max_length = 300  # Adjust this value if your column length is different
        if len(social_media_links_str) > max_length:
            social_media_links_str = social_media_links_str[:max_length]
        
        # Tech Stack Detection
        tech_stack = []

        # Check for CMS (Content Management Systems)
        if 'wp-content' in response.text or 'wp-include' in response.text:
            tech_stack.append('WordPress')
        if 'shopify' in response.text:
            tech_stack.append('Shopify')
        if 'joomla' in response.text:
            tech_stack.append('Joomla')
        if 'drupal' in response.text:
            tech_stack.append('Drupal')
        if 'magento' in response.text:
            tech_stack.append('Magento')
        
        # Check for JavaScript libraries and frameworks
        scripts = [script['src'] for script in soup.find_all('script', src=True)]
        if any('jquery' in script for script in scripts):
            tech_stack.append('jQuery')
        if any('bootstrap' in script for script in scripts):
            tech_stack.append('Bootstrap')
        if any('angular' in script for script in scripts):
            tech_stack.append('AngularJS')
        if any('react' in script for script in scripts):
            tech_stack.append('React')
        if any('vue' in script for script in scripts):
            tech_stack.append('Vue.js')

        # Check for MVC frameworks
        if 'rails' in response.text:
            tech_stack.append('Ruby on Rails')
        if 'django' in response.text:
            tech_stack.append('Django')
        if 'laravel' in response.text:
            tech_stack.append('Laravel')
        if 'express' in response.text:
            tech_stack.append('Express.js')
        if 'spring' in response.text:
            tech_stack.append('Spring')

        tech_stack_str = ','.join(tech_stack) if tech_stack else 'N/A'
        
        # Extract Payment Gateways
        payment_gateways = []
        if 'paypal' in response.text.lower():
            payment_gateways.append('PayPal')
        if 'razorpay' in response.text.lower():
            payment_gateways.append('Razorpay')
        
        # Extract Website Language
        language = 'N/A'
        if soup.find('html', lang=True):
            language = soup.find('html')['lang']
        
        # Extract Category of Website
        category = 'N/A' 
        
        return {
            'url': url,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'social_media_links': social_media_links_str,
            'tech_stack': tech_stack_str,
            'payment_gateways': payment_gateways,
            'language': language,
            'category': category
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Define a function to create the table if it does not exist
def create_table_if_not_exists(db_connection):
    try:
        with db_connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS websites (
                id INT AUTO_INCREMENT PRIMARY KEY,
                url VARCHAR(255) NOT NULL,
                meta_title VARCHAR(255),
                meta_description TEXT,
                social_media_links VARCHAR(300),
                tech_stack TEXT,
                payment_gateways VARCHAR(255),
                language VARCHAR(50),
                category VARCHAR(255)
            )
            """)
            db_connection.commit()
            print("Table checked/created successfully!")
    except Error as e:
        print(f"Error creating table: {e}")

# Define a function to store data in MySQL database
def store_in_database(data, db_connection):
    try:
        with db_connection.cursor() as cursor:
            sql = """
            INSERT INTO websites (url, meta_title, meta_description, social_media_links, tech_stack, payment_gateways, language, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (data['url'], data['meta_title'], data['meta_description'], data['social_media_links'],
                   data['tech_stack'], ','.join(data['payment_gateways']), data['language'], data['category'])
            cursor.execute(sql, val)
            db_connection.commit()
    except Error as e:
        print(f"Error storing data in the database: {e}")

# Connect to MySQL database
try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sam123",
        database="scrap"
    )
    if db_connection.is_connected():
        print("Connected to the database")
        create_table_if_not_exists(db_connection)
except Error as e:
    print(f"Error connecting to the database: {e}")
    db_connection = None

# List of websites to scrape
websites = [
    "https://www.wikipedia.org",
    "https://www.awwwards.com/websites",
    "https://www.stackoverflow.com",
    "https://www.github.com",
    "https://www.amazon.com",
    "https://www.ebay.com",
    "https://www.craigslist.org",
    "https://www.walmart.com",
    "https://www.etsy.com",
    "https://www.shopify.com",
    "https://www.bigcommerce.com",
    "https://www.magentocommerce.com",
    "https://www.zappos.com",
    "https://www.nike.com",
    "https://www.adidas.com",
    "https://www.pepperfry.com",
    "https://www.flipkart.com",
    "https://www.myntra.com",
    "https://www.snapdeal.com",
    "https://www.indiatimes.com",
    "https://www.ndtv.com",
    "https://www.bbc.com",
    "https://www.cnn.com",
    "https://www.nytimes.com",
    "https://www.theguardian.com",
    "https://www.forbes.com",
    "https://www.bloomberg.com",
    "https://www.wsj.com",
    "https://www.abcnews.go.com",
    "https://www.cbsnews.com",
    "https://www.nbcnews.com",
    "https://www.aljazeera.com",
    "https://www.reuters.com",
    "https://www.businessinsider.com",
    "https://www.huffpost.com",
    "https://www.theverge.com",
    "https://www.techcrunch.com",
    "https://www.engadget.com",
    "https://www.gizmodo.com",
    "https://www.arstechnica.com",
    "https://www.wired.com",
    "https://www.cnet.com",
    "https://www.digitaltrends.com",
    "https://www.thehackernews.com",
    "https://www.securityweek.com",
    "https://www.zdnet.com",
    "https://www.mashable.com",
    "https://www.adweek.com",
    "https://www.ted.com",
    "https://www.coursera.org",
    "https://www.udemy.com",
    "https://www.edx.org",
    "https://www.khanacademy.org",
    "https://www.academia.edu",
    "https://www.researchgate.net",
    "https://www.jstor.org",
    "https://www.sciencedirect.com",
    "https://www.springer.com",
    "https://www.britannica.com",
    "https://www.nationalgeographic.com",
    "https://www.sciencemag.org",
    "https://www.nature.com",
    "https://www.popularmechanics.com",
    "https://www.discovermagazine.com",
    "https://www.newscientist.com",
    "https://www.scientificamerican.com",
    "https://www.livescience.com",
    "https://www.space.com",
    "https://www.history.com"
]

# Scrape each website and store the data in the database
if db_connection:
    for website in websites:
        data = scrape_website(website)
        if data:
            store_in_database(data, db_connection)
    db_connection.close()
    print("Database connection closed")
