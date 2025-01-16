import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def create_sample_data(output_file="sample_data.csv"):
    data = pd.DataFrame({
        'age': [25, 30, None, 22, 35],
        'salary': [50000, None, 72000, 60000, 58000],
        'gender': ['Male', 'Female', None, 'Male', 'Female'],
        'department': ['HR', 'Engineering', 'Engineering', None, 'HR'],
        'target': [1, 0, 1, 0, 1]
    })
    data.to_csv(output_file, index=False)
    print(f"Sample data saved to {output_file}")
    return output_file

def create_pipeline():
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, ['age', 'salary']),
            ('cat', categorical_transformer, ['gender', 'department'])
        ]
    )

    return preprocessor

def preprocess_data(input_file="sample_data.csv", output_file="transformed_data.csv"):
    data = pd.read_csv(input_file)

    X = data.drop(columns=['target'], errors='ignore')
    y = data['target'] if 'target' in data.columns else None

    preprocessor = create_pipeline()

    X_transformed = preprocessor.fit_transform(X)

    feature_names = (
        list(preprocessor.named_transformers_['num'].named_steps['imputer'].feature_names_in_) +
        list(preprocessor.named_transformers_['cat'].named_steps['encoder'].get_feature_names_out())
    )

    transformed_df = pd.DataFrame(X_transformed, columns=feature_names)

    scaler = preprocessor.named_transformers_['num'].named_steps['scaler']

    transformed_df[['age', 'salary']] = scaler.inverse_transform(transformed_df[['age', 'salary']])

    if y is not None:
        transformed_df['target'] = y.values

    transformed_df.to_csv(output_file, index=False)
    print(f"Transformed data saved to {output_file}")

def main():
    input_file = create_sample_data()
    preprocess_data(input_file)

if __name__ == "__main__":
    main()
