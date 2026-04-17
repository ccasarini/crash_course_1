import pandas as pd

# 1. Load the Excel file into a "DataFrame" (like a spreadsheet in Python memory)
file_path = '../data/floodarchive.xlsx'
df = pd.read_excel(file_path)

# 2. Look for rows where the "Country" column is exactly "Bangladesh"
# We'll save these rows in a new variable called "bangladesh_data"
bangladesh_data = df[df['Country'] == 'Bangladesh']

# 3. Save the result to a CSV file.
# "index=False" ensures Python doesn't add an extra column of row numbers.
output_path = '../data/bangladesh_floods.csv'
bangladesh_data.to_csv(output_path, index=False)

print(f"Success! Filtered data saved to: {output_path}")
