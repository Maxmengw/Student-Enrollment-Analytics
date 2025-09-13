import pandas as pd
import numpy as np
from faker import Faker
import random
from collections import defaultdict

# --- 1. Project Parameters Setup ---
# This is an adjustable area where you can modify these numbers as needed
NUM_UNIQUE_STUDENTS = 45000  # Total number of unique students
PERCENT_MULTI_ACCOUNT = 0.08 # 8% of students have multiple accounts
AVG_ENROLLMENTS_PER_STUDENT = 2.5 # Average number of enrollments per student

NUM_TOTAL_RECORDS = int(NUM_UNIQUE_STUDENTS * AVG_ENROLLMENTS_PER_STUDENT)

# Define static data for the project
fake = Faker('en_CA') # Use Canadian locale for Faker
campuses = ['Downtown Campus', 'West End Campus', 'North York Campus', 'Scarborough Campus', 'Richmond Hill Campus']
subjects = ['Math', 'Olympiad Math', 'English', 'Science', 'Writing']
teachers = [fake.first_name() + ' ' + fake.last_name() for _ in range(50)]
terms = ['Winter 2023', 'Spring 2023', 'Summer 2023', 'Fall 2023', 'Winter 2024', 'Spring 2024', 'Summer 2024', 'Fall 2024']

# Define term-to-date mapping for generating realistic dates
term_date_ranges = {
    'Winter 2023': pd.to_datetime(['2023-01-01', '2023-02-28']),
    'Spring 2023': pd.to_datetime(['2023-03-01', '2023-05-31']),
    'Summer 2023': pd.to_datetime(['2023-06-01', '2023-08-31']),
    'Fall 2023': pd.to_datetime(['2023-09-01', '2023-11-30']),
    'Winter 2024': pd.to_datetime(['2024-01-01', '2024-02-28']),
    'Spring 2024': pd.to_datetime(['2024-03-01', '2024-05-31']),
    'Summer 2024': pd.to_datetime(['2024-06-01', '2024-08-31']),
    'Fall 2024': pd.to_datetime(['2024-09-01', '2024-11-30']),
}

# --- 2. Generate Unique Student Data ---
unique_students = pd.DataFrame({
    'master_student_id': range(1, NUM_UNIQUE_STUDENTS + 1),
    'student_name': [fake.name() for _ in range(NUM_UNIQUE_STUDENTS)],
    'grade': np.random.choice(range(1, 7), NUM_UNIQUE_STUDENTS),
    'unique_phone_number': [fake.unique.phone_number() for _ in range(NUM_UNIQUE_STUDENTS)]
})

# --- 3. Simulate Multi-Account Students and Records ---
multi_account_students = unique_students.sample(n=int(NUM_UNIQUE_STUDENTS * PERCENT_MULTI_ACCOUNT))
multi_account_records = pd.DataFrame()

# Ensure multi-account students are evenly distributed across different grades
for grade in range(1, 7):
    students_in_grade = unique_students[unique_students['grade'] == grade]
    num_to_select = int(len(students_in_grade) * PERCENT_MULTI_ACCOUNT)
    multi_account_students_grade = students_in_grade.sample(n=num_to_select)
    multi_account_records = pd.concat([multi_account_records, multi_account_students_grade])

# Remove duplicates to ensure processing only once
multi_account_records = multi_account_records.drop_duplicates(subset='master_student_id')

# Create a dictionary to map master_student_id to multiple phone_numbers and account_ids
multi_account_map = defaultdict(list)
for index, row in multi_account_records.iterrows():
    multi_account_map[row['master_student_id']].append({
        'phone_number_1': row['unique_phone_number'],
        'phone_number_2': fake.unique.phone_number(),
        'account_id_1': row['master_student_id'] * 100, # Simulate account_id
        'account_id_2': row['master_student_id'] * 100 + 1
    })

# --- 4. Generate All Enrollment Records ---
records = []
enrollment_id_counter = 1

# Loop through all students to generate their enrollment records
for index, row in unique_students.iterrows():
    num_enrollments = int(np.random.normal(AVG_ENROLLMENTS_PER_STUDENT, 1)) # Normal distribution is more realistic
    if num_enrollments < 1:
        num_enrollments = 1

    enrolled_terms = random.sample(terms, k=num_enrollments)
    enrolled_terms.sort(key=lambda x: terms.index(x))

    for i, term in enumerate(enrolled_terms):
        is_multi_account_student = row['master_student_id'] in multi_account_records['master_student_id'].values

        # Determine current phone_number and account_id
        if is_multi_account_student:
            account_info = multi_account_map[row['master_student_id']][0]
            # Randomly assign to two different accounts
            if random.random() < 0.5:
                current_phone = account_info['phone_number_1']
                current_account_id = account_info['account_id_1']
            else:
                current_phone = account_info['phone_number_2']
                current_account_id = account_info['account_id_2']
        else:
            current_phone = row['unique_phone_number']
            current_account_id = row['master_student_id'] * 100 # Single-account student

        is_promo = term in ['Summer 2023', 'Winter 2024'] and random.random() < 0.7 # 70% probability for promotion
        tuition = 1500 if row['grade'] <= 3 else 2000
        if is_promo:
            tuition *= 0.5 # 50% discount for promotion

        record = {
            'enrollment_id': enrollment_id_counter,
            'account_id': current_account_id,
            'student_id': row['master_student_id'], # student_id here is unique
            'student_name': row['student_name'],
            'phone_number': current_phone,
            'enrollment_date': fake.date_time_between(start_date=term_date_ranges[term][0], end_date=term_date_ranges[term][1]),
            'term': term,
            'grade': row['grade'],
            'campus_name': random.choice(campuses),
            'subject': random.choice(subjects),
            'teacher_name': random.choice(teachers),
            'is_promotion': is_promo,
            'tuition_paid': tuition
        }
        records.append(record)
        enrollment_id_counter += 1

# --- 5. Integrate into DataFrame and Save ---
final_df = pd.DataFrame(records)

# Ensure total record count is within expected range
print(f"Total records generated: {len(final_df)}")

# Save as CSV file
file_name = 'student_enrollments_raw.csv'
final_df.to_csv(file_name, index=False)
print(f"Data successfully saved to {file_name}")

# Display first 5 rows for quick preview
print("\nData preview:")
print(final_df.head())