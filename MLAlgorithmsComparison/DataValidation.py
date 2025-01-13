import pandas as pd
import logging

# Set up logging for validation
logging.basicConfig(filename='csv_validation.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')   

def validate_csv_structure(csv_path):
    """Validate the structure of the CSV file."""
    expected_columns = ['Key', 'title', 'abstract', 'category']
    
    # Load the CSV to check the columns
    df = pd.read_csv(csv_path)
    
    # Check for missing columns
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        logging.warning(f"Missing columns: {missing_columns}")
    
    # Check for unexpected columns
    unexpected_columns = [col for col in df.columns if col not in expected_columns]
    if unexpected_columns:
        logging.warning(f"Unexpected columns: {unexpected_columns}")
    
    # Check for empty rows or columns
    if df.isnull().values.any():
        logging.warning("There are missing values in the data.")
    
    # Check for rows with missing 'title' or 'abstract' fields
    missing_values = df[df[['title', 'abstract']].isnull().any(axis=1)]
    if not missing_values.empty:
        logging.warning(f"Rows with missing title or abstract: {missing_values.index.tolist()}")
    
    # Check if the file is loaded properly by examining the first few rows
    logging.info(f"First few rows of the CSV:\n{df.head()}")
    
    return df

def check_empty_data(csv_path):
    """Check for empty data or missing values in the CSV."""
    df = pd.read_csv(csv_path)
    
    # Check for completely empty rows
    empty_rows = df[df.isnull().all(axis=1)]
    if not empty_rows.empty:
        logging.warning(f"Empty rows found: {empty_rows.index.tolist()}")
        
    # Check if there's a significant amount of missing data (e.g., 10% empty rows)
    if len(empty_rows) / len(df) > 0.1:
        logging.warning(f"More than 10% of the rows are empty!")
        
    return df

def check_duplicates(csv_path):
    """Check for duplicate rows in the CSV based on the 'Key' column."""
    df = pd.read_csv(csv_path)
    df['title'] = df['title'].str.strip()
    df['abstract'] = df['abstract'].str.strip() 

    # Check for duplicate rows based on the 'Key' column
    duplicate_rows = df[df.duplicated(subset=['Key', 'title', 'abstract'], keep=False)]  # keep=False marks all duplicates as True
    
    if not duplicate_rows.empty:
        logging.warning(f"Duplicate rows found: {duplicate_rows.index.tolist()}")
        
    return df

def validate_final_csv(csv_path):
    """Perform all the validation checks on the final CSV."""
    logging.info(f"Validating the CSV file: {csv_path}")
    
    # Validate structure
    validate_csv_structure(csv_path)
    
    # Check for empty data
    check_empty_data(csv_path)
    
    # Check for duplicates
    # check_duplicates(csv_path)
    
    # Final success check
    with open('csv_validation.log', 'r') as log_file:
        log_content = log_file.read()
        
    if 'WARNING' in log_content:
        logging.error("Validation failed with warnings or errors.")
        return False
    else:
        logging.info("CSV validation completed successfully.")
        return True

if __name__ == "__main__":
    # Path to the final CSV generated in the first script
    final_csv_path = 'processed_articles_sanitized.csv'
    
    # Validate the final CSV
    success = validate_final_csv(final_csv_path)
    
    # Print success/failure message
    if success:
        print("CSV validation completed successfully!")
    else:
        print("CSV validation failed. Check the logs for more details.")
