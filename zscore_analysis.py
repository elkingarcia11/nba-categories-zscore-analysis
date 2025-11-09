#!/usr/bin/env python3
"""
Fantasy Basketball Z-Score Analysis
Calculates z-scores for each statistical category and ranks players by total z-score.
"""

import pandas as pd
def parse_csv_data(file_path: str) -> pd.DataFrame:
    """Parse the CSV file and clean the data."""
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Remove the last row which contains "STATS" and empty values
    df = df[:-1]
    
    # Clean player names (remove newlines and extra text)
    df['Player'] = df['Player'].str.replace('\n', ' ').str.strip()
    
    # Convert numeric columns to float, handling any non-numeric values
    numeric_columns = ['FG%', 'FT%', '3:00 PM', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']
    
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove rows with any NaN values
    df = df.dropna()
    
    return df

def calculate_z_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate z-scores for each statistical category."""
    # Define the categories to analyze
    categories = ['FG%', 'FT%', '3:00 PM', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS']
    
    # Create a copy of the dataframe
    df_z = df.copy()
    
    # Calculate z-scores for each category
    for category in categories:
        mean_val = df[category].mean()
        std_val = df[category].std()
        
        # Calculate z-score: (value - mean) / standard_deviation
        df_z[f'{category}_zscore'] = (df[category] - mean_val) / std_val
    
    return df_z

def calculate_total_z_scores(df_z: pd.DataFrame) -> pd.DataFrame:
    """Calculate total z-scores for each player."""
    # Define the categories (excluding TO since lower is better)
    positive_categories = ['FG%', 'FT%', '3:00 PM', 'REB', 'AST', 'STL', 'BLK', 'PTS']
    
    # For TO (turnovers), we want to invert the z-score since lower is better
    df_z['TO_zscore_inverted'] = -df_z['TO_zscore']
    
    # Calculate total z-score (sum of all positive z-scores)
    zscore_columns = [f'{cat}_zscore' for cat in positive_categories if cat != 'TO'] + ['TO_zscore_inverted']
    df_z['Total_ZScore'] = df_z[zscore_columns].sum(axis=1)
    
    return df_z

def rank_players(df_z: pd.DataFrame) -> pd.DataFrame:
    """Rank players by total z-score from highest to lowest."""
    # Sort by total z-score in descending order
    df_ranked = df_z.sort_values('Total_ZScore', ascending=False).reset_index(drop=True)
    
    # Add rank column
    df_ranked['Rank'] = range(1, len(df_ranked) + 1)
    
    return df_ranked

def display_results(df_ranked: pd.DataFrame, top_n: int = 20) -> None:
    """Display the ranked results."""
    print("=" * 80)
    print("FANTASY BASKETBALL Z-SCORE RANKINGS")
    print("=" * 80)
    print(f"Showing top {min(top_n, len(df_ranked))} players")
    print()
    
    # Display column headers
    print(f"{'Rank':<4} {'Player':<25} {'Total Z-Score':<12} {'FG%':<8} {'FT%':<8} {'3PM':<8} {'REB':<8} {'AST':<8} {'STL':<8} {'BLK':<8} {'TO':<8} {'PTS':<8}")
    print("-" * 120)
    
    # Display top players
    for idx, row in df_ranked.head(top_n).iterrows():
        player_name = row['Player'][:24]  # Truncate long names
        total_z = row['Total_ZScore']
        
        # Get individual z-scores
        fg_z = row['FG%_zscore']
        ft_z = row['FT%_zscore']
        pm3_z = row['3:00 PM_zscore']
        reb_z = row['REB_zscore']
        ast_z = row['AST_zscore']
        stl_z = row['STL_zscore']
        blk_z = row['BLK_zscore']
        to_z = row['TO_zscore_inverted']  # Already inverted
        pts_z = row['PTS_zscore']
        
        print(f"{row['Rank']:<4} {player_name:<25} {total_z:<12.2f} {fg_z:<8.2f} {ft_z:<8.2f} {pm3_z:<8.2f} {reb_z:<8.2f} {ast_z:<8.2f} {stl_z:<8.2f} {blk_z:<8.2f} {to_z:<8.2f} {pts_z:<8.2f}")

def main():
    """Main function to run the z-score analysis."""
    try:
        # Parse the CSV data
        print("Loading and parsing data...")
        df = parse_csv_data('/Users/elkingarcia/Documents/python/fantasy/input.csv')
        print(f"Loaded {len(df)} players")
        
        # Calculate z-scores
        print("Calculating z-scores...")
        df_z = calculate_z_scores(df)
        
        # Calculate total z-scores
        print("Calculating total z-scores...")
        df_z = calculate_total_z_scores(df_z)
        
        # Rank players
        print("Ranking players...")
        df_ranked = rank_players(df_z)
        
        # Display results
        display_results(df_ranked, top_n=30)
        
        # Save results to CSV
        output_file = '/Users/elkingarcia/Documents/python/fantasy/zscore_rankings.csv'
        df_ranked.to_csv(output_file, index=False)
        print(f"\nResults saved to: {output_file}")
        
        # Display summary statistics
        print("\n" + "=" * 50)
        print("SUMMARY STATISTICS")
        print("=" * 50)
        print(f"Total players analyzed: {len(df_ranked)}")
        print(f"Highest total z-score: {df_ranked['Total_ZScore'].max():.2f}")
        print(f"Lowest total z-score: {df_ranked['Total_ZScore'].min():.2f}")
        print(f"Average total z-score: {df_ranked['Total_ZScore'].mean():.2f}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
