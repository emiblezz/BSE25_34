# Price Aggregator Web App  
## Overview
The **Price Aggregator Web App** helps users find the best prices for products such as laptops, phones, and more by scraping multiple eCommerce platforms (e.g., Amazon, Jumia, eBay) in real time. The app returns the top-x cheapest products, enabling users to easily compare prices across stores without manually browsing each one.  

### Key Activities
We shall be tracking, assigning and monitoring our activities and tasks using **ClickUp** and **Jira**. Below is a highlight of tasks we shall accomplish in the due course of this assignment.
1. **Set Up Version Control**
2. **ClickUp Setup**
3. **Configure CI Tool**
4. **Automate The Build Process**
5. **Automate Testing and Code Quality**
6. **Set Up Staging Environment**
7. **Automate Deployment**
8. **Production Deployment**
9. **Issue Tracking**
10. **Optimize CI/CD Pipeline**
11. **Documentation**

### Key Features  
- **Real-time Scraping**: Fetches up-to-date product information from various online stores.
- **Top-x Results**: Shows the cheapest product listings based on user searches.
- **Simple UI**: A single-page interface to display search results and product details.

### Installation  

#### Prerequisites  
- Python  
- Git  
- Internet access for scraping  

#### Steps to Install  
1. **Clone the Repository**  
    #####  
        git clone https://gitlab.cranecloud.io/2025-SE4/bse25-34.git 

2. **Navigate to Project Directory**  
    #####
        cd bse25-34

3. **Create a Virtual Environment**  
    #####
        python3 -m venv venv   

4. **Activate the Virtual Environment**  
    ##### On macOS/Linux:
        source venv/bin/activate 

    ##### On Windows:
        venv\Scripts\activate  

5. **Install Dependencies**  
    #####
        pip3 install -r requirements.txt  

6. **Run Database Migrations**  
    #####
        python3 manage.py migrate  

7. **Run the Development Server**  
    #####
        python3 manage.py runserver    

8. **Access the App**  
    ##### Open your browser and visit: 
        http://localhost:8000
