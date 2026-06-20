from src.ingestion.ingestion import DataIngestion
from src.config.settings import RAW_DATA_PATH
from src.validation.validation import DataValidator
from src.transformation.transform import DataTransformer
from src.loading.load import DataLoader

def main():
    # 1. Ingestion
    ingestion = DataIngestion(RAW_DATA_PATH)
    df = ingestion.load_data()

    # 2. Validation
    validator = DataValidator(df)
    report = validator.generate_report()
    validator.save_report(report)
    
    print("\nValidation Report\n")
    for metric, value in report.items():
        print(f"{metric}:{value}")

    # 3. Transformation
    print("\nStarting Data Transformation...\n")
    transformer = DataTransformer(df)
    transformer.clean_data()
    featured_df = transformer.create_features()
    transformer.save_data()

    # 4. Loading
    print("\nStarting Data Loading...\n")
    loader = DataLoader(featured_df)
    loader.load_to_db()

if __name__ == "__main__":
    main()