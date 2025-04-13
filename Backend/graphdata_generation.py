import pandas as pd

# 1. Top Tags of Each Year (Normalized)
def generate_normalized_top_tags_per_year(input_csv='last_10_years_stackoverflow.csv', output_csv='top_tags_normalized.csv', top_n=10):
    print("📊 [1] Generating normalized top tags per year...")

    df = pd.read_csv(input_csv)
    tag_counts = df.groupby(['Year', 'Tag']).size().reset_index(name='TagCount')
    total_tags_per_year = tag_counts.groupby('Year')['TagCount'].sum().reset_index(name='TotalTags')

    merged = pd.merge(tag_counts, total_tags_per_year, on='Year')
    merged['NormalizedFrequency'] = (merged['TagCount'] / merged['TotalTags'])*100

    top_tags = (
        merged.sort_values(['Year', 'NormalizedFrequency'], ascending=[False, False])
        .groupby('Year')
        .head(top_n)
    )

    top_tags.to_csv(output_csv, index=False)
    print(f"✅ Saved: {output_csv}\n")

# 2. Tag Trends Over Time (Normalized)
def generate_tag_trends_over_time(input_csv='last_10_years_stackoverflow.csv', output_csv='tag_trends_over_time.csv'):
    print("📈 [2] Generating tag trends over time...")

    df = pd.read_csv(input_csv)
    tag_counts = df.groupby(['Year', 'Tag']).size().reset_index(name='TagCount')
    total_tags = tag_counts.groupby('Year')['TagCount'].sum().reset_index(name='TotalTags')
    merged = pd.merge(tag_counts, total_tags, on='Year')
    merged['NormalizedFrequency'] = (merged['TagCount'] / merged['TotalTags'])*100

    target_tags_df = pd.read_csv('top_tags_normalized.csv')
    target_tags = set()
    for row in target_tags_df['Tag']:
        target_tags.add(row)

    if target_tags:
        merged = merged[merged['Tag'].isin(target_tags)]

    trend_df = merged.pivot_table(index='Year', columns='Tag', values='NormalizedFrequency', fill_value=0).reset_index()
    trend_df.to_csv(output_csv, index=False)
    print(f"✅ Saved: {output_csv}\n")

# 4. Tag Distribution for a Specific Year (Normalized)
def generate_tag_distribution_for_year(year, input_csv='last_10_years_stackoverflow.csv', output_csv_prefix='tag_distribution_'):
    print(f"📊 [4] Generating tag distribution for year {year}...")

    df = pd.read_csv(input_csv)
    df_year = df[df['Year'] == year]
    tag_counts = df_year.groupby('Tag').size().reset_index(name='TagCount')
    total = tag_counts['TagCount'].sum()
    tag_counts['NormalizedFrequency'] = (tag_counts['TagCount'] / total)*100

    tag_counts.sort_values('NormalizedFrequency', ascending=False).to_csv(f"{output_csv_prefix}{year}.csv", index=False)
    print(f"✅ Saved: {output_csv_prefix}{year}.csv\n")

def generate_monthly_tag_frequency_percent(input_csv='last_10_years_stackoverflow.csv', output_csv='monthly_tag_frequency_percent.csv', top_n=10):
    print("📆 [5] Generating normalized monthly tag frequency (in %)...")

    # Read the data
    df = pd.read_csv(input_csv)

    # Extract the month (from DateTime column)
    df['Month'] = pd.to_datetime(df['DateTime']).dt.month

    # Group by Month and Tag to count occurrences
    tag_counts = df.groupby(['Month', 'Tag']).size().reset_index(name='TagCount')

    # Total tags per month
    total_tags_per_month = tag_counts.groupby('Month')['TagCount'].sum().reset_index(name='TotalTags')

    # Merge and normalize
    merged = pd.merge(tag_counts, total_tags_per_month, on='Month')
    merged['NormalizedFrequency (%)'] = (merged['TagCount'] / merged['TotalTags']) * 100

    # Select top N tags per month
    top_tags = (
        merged.sort_values(['Month', 'NormalizedFrequency (%)'], ascending=[True, False])
            .groupby('Month')
            .head(top_n)
    )

    # Save to CSV
    top_tags.to_csv(output_csv, index=False)
    print(f"✅ Saved: {output_csv}\n")

def generate_monthly_tag_frequency_percent(input_csv='last_10_years_stackoverflow.csv',
output_csv='monthly_tag_frequency_percent.csv',top_n=10):
    print("📆 [5] Generating normalized monthly tag frequency (in %)...")

    # Read the data
    df = pd.read_csv(input_csv)

    # Extract the month (from DateTime column)
    df['Month'] = pd.to_datetime(df['DateTime']).dt.month

    # Group by Month and Tag to count occurrences
    tag_counts = df.groupby(['Month', 'Tag']).size().reset_index(name='TagCount')

    # Total tags per month
    total_tags_per_month = tag_counts.groupby('Month')['TagCount'].sum().reset_index(name='TotalTags')

    # Merge and normalize
    merged = pd.merge(tag_counts, total_tags_per_month, on='Month')
    merged['NormalizedFrequency (%)'] = (merged['TagCount'] / merged['TotalTags']) * 100

    # Select top N tags per month
    top_tags = (
        merged.sort_values(['Month', 'NormalizedFrequency (%)'], ascending=[True, False])
            .groupby('Month')
            .head(top_n)
    )

    # Save to CSV
    top_tags.to_csv(output_csv, index=False)
    print(f"✅ Saved: {output_csv}\n")

def generate_multi_tag_trend(input_csv='last_10_years_stackoverflow.csv',output_csv='multi_tag_question_trend.csv'):
    print("🔗 [6] Generating multi-tag question trend over years...")

    # Read the data
    df = pd.read_csv(input_csv)

    # Group all tags per question
    grouped = df.groupby(['Year', 'QuestionID'])['Tag'].count().reset_index(name='TagCount')

    # Count how many questions had multiple tags per year
    grouped['IsMultiTag'] = grouped['TagCount'] > 1
    multi_tag_stats = grouped.groupby('Year')['IsMultiTag'].sum().reset_index(name='MultiTagQuestionCount')

    # Total questions per year (use same grouped data)
    total_questions = grouped.groupby('Year')['QuestionID'].count().reset_index(name='TotalQuestions')

    # Merge to get percentage
    result = pd.merge(multi_tag_stats, total_questions, on='Year')
    result['PercentageMultiTag (%)'] = (result['MultiTagQuestionCount'] / result['TotalQuestions']) * 100

    # Save to CSV
    result.to_csv(output_csv, index=False)
    print(f"✅ Saved: {output_csv}\n")

def generate_unique_vs_repeated_tags(input_csv='last_10_years_stackoverflow.csv',
output_csv='unique_vs_repeated_tags.csv'):
    print("🧬 [7] Generating unique vs repeated tag count per year...")

    # Load data
    df = pd.read_csv(input_csv)

    result = []

    # Loop through each year
    for year in sorted(df['Year'].unique()):
        year_df = df[df['Year'] == year]

        # Count frequency of each tag
        tag_counts = year_df['Tag'].value_counts()

        unique_tags = (tag_counts == 1).sum()
        repeated_tags = (tag_counts > 1).sum()

        result.append({
            'Year': year,
            'UniqueTags': unique_tags,
            'RepeatedTags': repeated_tags,
            'TotalTags': unique_tags + repeated_tags,
            'PercentUnique': (unique_tags / (unique_tags + repeated_tags)) * 100,
            'PercentRepeated': (repeated_tags / (unique_tags + repeated_tags)) * 100,
        })

    result_df = pd.DataFrame(result)
    result_df.to_csv(output_csv, index=False)
    print(f"✅ Saved: {output_csv}\n")

def generate_tags_per_question_distribution(input_csv='last_10_years_stackoverflow.csv',
output_csv='tags_per_question_distribution.csv'):
    print("🔢 [8] Generating Tags per Question distribution...")

    # Load data
    df = pd.read_csv(input_csv)

    # Count how many tags each QuestionID has
    tag_counts = df.groupby('QuestionID')['Tag'].count()

    # Count how many questions have 1 tag, 2 tags, 3 tags, etc.
    distribution = tag_counts.value_counts().sort_index().reset_index()
    distribution.columns = ['NumberOfTags', 'QuestionCount']

    # Save to CSV
    distribution.to_csv(output_csv, index=False)
    print(f"✅ Saved: {output_csv}\n")

# === Example Usage ===
if __name__ == "__main__":
    # generate_normalized_top_tags_per_year()
    # generate_tag_trends_over_time()
    # generate_total_questions_per_year()
    # generate_tag_distribution_for_year(2023)
    # generate_monthly_tag_frequency_percent()
    # generate_monthly_tag_frequency_percent()
    # generate_multi_tag_trend()
    # generate_unique_vs_repeated_tags()
    # generate_tags_per_question_distribution()
    pass