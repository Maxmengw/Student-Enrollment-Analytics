"""
Student Enrollment Analytics - Demo Visualizations
This script creates key visualizations for the GitHub repository
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_sample_data():
    """Create sample data for demonstration purposes"""
    np.random.seed(42)
    
    # Sample data structure
    sample_data = {
        'subject': ['Math', 'English', 'Science', 'Writing', 'Olympiad Math'] * 100,
        'campus': ['Downtown', 'West End', 'North York', 'Scarborough', 'Richmond Hill'] * 100,
        'grade': np.random.choice([1, 2, 3, 4, 5, 6], 500),
        'revenue': np.random.normal(1500, 300, 500),
        'enrollment_count': np.random.poisson(200, 500)
    }
    
    return pd.DataFrame(sample_data)

def create_dashboard():
    """Create executive dashboard visualization"""
    df = create_sample_data()
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Student Enrollment Analytics - Executive Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Revenue by Subject
    subject_revenue = df.groupby('subject')['revenue'].sum().sort_values(ascending=True)
    axes[0,0].barh(subject_revenue.index, subject_revenue.values, color='skyblue', alpha=0.7)
    axes[0,0].set_title('Revenue by Subject', fontweight='bold')
    axes[0,0].set_xlabel('Total Revenue ($)')
    
    # 2. Campus Performance
    campus_performance = df.groupby('campus')['enrollment_count'].sum().sort_values(ascending=True)
    axes[0,1].barh(campus_performance.index, campus_performance.values, color='lightgreen', alpha=0.7)
    axes[0,1].set_title('Enrollment by Campus', fontweight='bold')
    axes[0,1].set_xlabel('Total Enrollments')
    
    # 3. Grade Distribution
    grade_dist = df['grade'].value_counts().sort_index()
    axes[1,0].bar(grade_dist.index, grade_dist.values, color='coral', alpha=0.7)
    axes[1,0].set_title('Student Distribution by Grade', fontweight='bold')
    axes[1,0].set_xlabel('Grade Level')
    axes[1,0].set_ylabel('Number of Students')
    
    # 4. Revenue vs Enrollment Scatter
    campus_metrics = df.groupby('campus').agg({'revenue': 'sum', 'enrollment_count': 'sum'})
    axes[1,1].scatter(campus_metrics['enrollment_count'], campus_metrics['revenue'], 
                     s=200, alpha=0.7, c='purple')
    axes[1,1].set_title('Revenue vs Enrollment by Campus', fontweight='bold')
    axes[1,1].set_xlabel('Total Enrollments')
    axes[1,1].set_ylabel('Total Revenue ($)')
    
    # Add campus labels
    for i, campus in enumerate(campus_metrics.index):
        axes[1,1].annotate(campus, 
                          (campus_metrics['enrollment_count'].iloc[i], 
                           campus_metrics['revenue'].iloc[i]),
                          xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('executive_dashboard.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_trend_analysis():
    """Create trend analysis visualization"""
    # Simulate time series data
    months = pd.date_range('2023-01-01', '2024-12-31', freq='M')
    enrollment_trend = np.random.normal(1000, 100, len(months)) + np.sin(np.arange(len(months)) * 2 * np.pi / 12) * 200
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Enrollment trend
    ax1.plot(months, enrollment_trend, linewidth=2, marker='o', markersize=4, color='blue')
    ax1.set_title('Monthly Enrollment Trends (2023-2024)', fontweight='bold', fontsize=14)
    ax1.set_ylabel('Number of Enrollments')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Seasonal pattern
    seasonal_data = [1200, 1100, 1300, 1400, 1200, 1000, 800, 900, 1100, 1300, 1400, 1300]
    months_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    ax2.bar(months_short, seasonal_data, color='lightcoral', alpha=0.7)
    ax2.set_title('Seasonal Enrollment Pattern', fontweight='bold', fontsize=14)
    ax2.set_ylabel('Average Enrollments')
    ax2.set_xlabel('Month')
    
    plt.tight_layout()
    plt.savefig('trend_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    print("Creating demo visualizations...")
    create_dashboard()
    create_trend_analysis()
    print("Visualizations saved as PNG files!")
