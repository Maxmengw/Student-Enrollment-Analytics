"""
Generate portfolio images using real data from the analysis
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_and_process_data():
    """Load and process the real data"""
    df = pd.read_csv('student_enrollments_raw.csv')
    df['enrollment_date'] = pd.to_datetime(df['enrollment_date'])
    df['year'] = df['enrollment_date'].dt.year
    df['month'] = df['enrollment_date'].dt.month
    df['quarter'] = df['enrollment_date'].dt.quarter
    
    # Create master student ID using phone number
    df['master_student_id'] = df['phone_number'].astype('category').cat.codes
    
    return df

def create_executive_dashboard(df):
    """Create executive dashboard with real data"""
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Student Enrollment Analytics - Executive Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Revenue by Subject (Pie Chart)
    subject_revenue = df.groupby('subject')['tuition_paid'].sum().sort_values(ascending=False)
    axes[0,0].pie(subject_revenue.values, labels=subject_revenue.index, autopct='%1.1f%%', startangle=90)
    axes[0,0].set_title('Revenue Distribution by Subject', fontweight='bold')
    
    # 2. Campus Performance (Bar Chart)
    campus_revenue = df.groupby('campus_name')['tuition_paid'].sum().sort_values(ascending=True)
    axes[0,1].barh(campus_revenue.index, campus_revenue.values, color='skyblue', alpha=0.7)
    axes[0,1].set_title('Revenue by Campus', fontweight='bold')
    axes[0,1].set_xlabel('Total Revenue ($)')
    
    # 3. Student Enrollment Patterns
    student_enrollment_counts = df.groupby('master_student_id').size()
    single_enrollment = (student_enrollment_counts == 1).sum()
    multiple_enrollments = (student_enrollment_counts > 1).sum()
    
    retention_metrics = ['Single Enrollment', 'Multiple Enrollments']
    retention_values = [single_enrollment, multiple_enrollments]
    colors = ['lightcoral', 'lightgreen']
    
    axes[0,2].bar(retention_metrics, retention_values, color=colors, alpha=0.7)
    axes[0,2].set_title('Student Enrollment Patterns', fontweight='bold')
    axes[0,2].set_ylabel('Number of Students')
    for i, v in enumerate(retention_values):
        axes[0,2].text(i, v + 500, f'{v:,}', ha='center', fontweight='bold')
    
    # 4. Term-by-Term Enrollment Trends
    term_order = ['Winter 2023', 'Spring 2023', 'Summer 2023', 'Fall 2023', 
                  'Winter 2024', 'Spring 2024', 'Summer 2024', 'Fall 2024']
    term_data = df.groupby('term')['master_student_id'].nunique().reindex(term_order)
    
    axes[1,0].plot(range(len(term_data)), term_data.values, marker='o', linewidth=2, markersize=8, color='purple')
    axes[1,0].set_title('Student Enrollment Trends by Term', fontweight='bold')
    axes[1,0].set_xlabel('Term')
    axes[1,0].set_ylabel('Number of Students')
    axes[1,0].set_xticks(range(len(term_data)))
    axes[1,0].set_xticklabels([term.split()[0] + '\n' + term.split()[1] for term in term_data.index], rotation=45)
    axes[1,0].grid(True, alpha=0.3)
    
    # 5. Grade Distribution
    grade_dist = df['grade'].value_counts().sort_index()
    axes[1,1].bar(grade_dist.index, grade_dist.values, color='gold', alpha=0.7)
    axes[1,1].set_title('Student Distribution by Grade', fontweight='bold')
    axes[1,1].set_xlabel('Grade Level')
    axes[1,1].set_ylabel('Number of Students')
    for i, v in enumerate(grade_dist.values):
        axes[1,1].text(i+1, v + 500, f'{v:,}', ha='center', fontweight='bold')
    
    # 6. Key Metrics Summary
    total_revenue = df['tuition_paid'].sum()
    total_students = df['master_student_id'].nunique()
    re_enrollment_rate = multiple_enrollments / total_students * 100
    top_subject = subject_revenue.index[0]
    top_campus = campus_revenue.index[-1]
    top_grade = grade_dist.idxmax()
    
    axes[1,2].axis('off')
    metrics_text = f"""
KEY PERFORMANCE INDICATORS

Total Revenue: ${total_revenue:,.0f}
Total Students: {total_students:,}
Re-enrollment Rate: {re_enrollment_rate:.1f}%

TOP PERFORMERS
Subject: {top_subject}
Campus: {top_campus}
Grade: {top_grade}

GROWTH OPPORTUNITIES
Potential Revenue: ${single_enrollment * (total_revenue/len(df)):,.0f}
Retention Opportunity: {100 - re_enrollment_rate:.1f}%
"""
    axes[1,2].text(0.1, 0.9, metrics_text, transform=axes[1,2].transAxes, fontsize=12,
                   verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('executive_dashboard.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Executive dashboard saved as 'executive_dashboard.png'")

def create_trend_analysis(df):
    """Create trend analysis with real data"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Monthly enrollment trends
    monthly_data = df.groupby(['year', 'month']).size().reset_index()
    monthly_data['date'] = pd.to_datetime(monthly_data[['year', 'month']].assign(day=1))
    monthly_data = monthly_data.sort_values('date')
    
    ax1.plot(monthly_data['date'], monthly_data[0], linewidth=2, marker='o', markersize=4, color='blue')
    ax1.set_title('Monthly Enrollment Trends (2023-2024)', fontweight='bold', fontsize=14)
    ax1.set_ylabel('Number of Enrollments')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Seasonal pattern
    seasonal_data = df.groupby('month').size()
    months_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Ensure we have data for all 12 months
    seasonal_values = [seasonal_data.get(i, 0) for i in range(1, 13)]
    
    ax2.bar(months_short, seasonal_values, color='lightcoral', alpha=0.7)
    ax2.set_title('Seasonal Enrollment Pattern', fontweight='bold', fontsize=14)
    ax2.set_ylabel('Average Enrollments')
    ax2.set_xlabel('Month')
    
    plt.tight_layout()
    plt.savefig('trend_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Trend analysis saved as 'trend_analysis.png'")

def create_revenue_analysis(df):
    """Create revenue analysis visualization"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Revenue Analysis Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Revenue by Subject
    subject_revenue = df.groupby('subject')['tuition_paid'].sum().sort_values(ascending=True)
    axes[0,0].barh(subject_revenue.index, subject_revenue.values, color='lightblue', alpha=0.7)
    axes[0,0].set_title('Revenue by Subject', fontweight='bold')
    axes[0,0].set_xlabel('Total Revenue ($)')
    
    # 2. Revenue by Campus
    campus_revenue = df.groupby('campus_name')['tuition_paid'].sum().sort_values(ascending=True)
    axes[0,1].barh(campus_revenue.index, campus_revenue.values, color='lightgreen', alpha=0.7)
    axes[0,1].set_title('Revenue by Campus', fontweight='bold')
    axes[0,1].set_xlabel('Total Revenue ($)')
    
    # 3. Revenue by Grade
    grade_revenue = df.groupby('grade')['tuition_paid'].sum().sort_index()
    axes[1,0].bar(grade_revenue.index, grade_revenue.values, color='coral', alpha=0.7)
    axes[1,0].set_title('Revenue by Grade Level', fontweight='bold')
    axes[1,0].set_xlabel('Grade Level')
    axes[1,0].set_ylabel('Total Revenue ($)')
    
    # 4. Year-over-year comparison
    yearly_revenue = df.groupby('year')['tuition_paid'].sum()
    axes[1,1].bar(yearly_revenue.index, yearly_revenue.values, color='purple', alpha=0.7)
    axes[1,1].set_title('Year-over-Year Revenue Comparison', fontweight='bold')
    axes[1,1].set_xlabel('Year')
    axes[1,1].set_ylabel('Total Revenue ($)')
    
    plt.tight_layout()
    plt.savefig('revenue_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Revenue analysis saved as 'revenue_analysis.png'")

if __name__ == "__main__":
    print("Loading data and generating portfolio images...")
    df = load_and_process_data()
    
    print("Creating executive dashboard...")
    create_executive_dashboard(df)
    
    print("Creating trend analysis...")
    create_trend_analysis(df)
    
    print("Creating revenue analysis...")
    create_revenue_analysis(df)
    
    print("All portfolio images generated successfully!")
    print("Files created:")
    print("- executive_dashboard.png")
    print("- trend_analysis.png") 
    print("- revenue_analysis.png")
