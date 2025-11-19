# region Overview
"""
CSV Data Analysis Tool

Provides comprehensive data analysis capabilities similar to Claude's data analysis tool.
Performs exploratory data analysis, statistical summaries, data quality checks,
correlation analysis, and generates actionable insights.

Example usage:
- 'analyze data.csv'
- 'give me insights on sales.csv'
- 'perform comprehensive analysis on dataset.csv'
- 'analyze data.csv with quick analysis'
"""
# endregion

# region imports
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
# endregion

# region Helper Functions

def get_dataset_overview(df: pd.DataFrame, file_path: str) -> str:
    """Generate dataset overview section"""
    result = "=" * 70 + "\n"
    result += "CSV DATA ANALYSIS REPORT\n"
    result += "=" * 70 + "\n\n"
    result += f"File: {file_path}\n"
    result += f"Analyzed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    result += "[1] DATASET OVERVIEW\n"
    result += "-" * 70 + "\n"
    result += f"• Shape: {df.shape[0]:,} rows × {df.shape[1]} columns\n"
    result += f"• Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB\n"

    # Count column types
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

    result += f"• Column types: {len(numerical_cols)} numerical, {len(categorical_cols)} categorical"
    if datetime_cols:
        result += f", {len(datetime_cols)} datetime"
    result += "\n\n"

    # List all columns with types
    result += "Columns:\n"
    for col in df.columns:
        result += f"  - {col}: {df[col].dtype}\n"

    return result, numerical_cols, categorical_cols, datetime_cols


def analyze_data_quality(df: pd.DataFrame) -> str:
    """Analyze data quality issues"""
    result = "\n[2] DATA QUALITY ANALYSIS\n"
    result += "-" * 70 + "\n"

    # Check for duplicates
    duplicate_count = df.duplicated().sum()
    if duplicate_count == 0:
        result += "✓ No duplicate rows found\n"
    else:
        result += f"⚠ {duplicate_count} duplicate rows found ({duplicate_count/len(df)*100:.2f}%)\n"

    # Check for missing values
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]

    if len(missing_cols) == 0:
        result += "✓ No missing values found\n"
    else:
        result += f"⚠ {len(missing_cols)} columns with missing data:\n"
        for col, count in missing_cols.items():
            pct = count / len(df) * 100
            result += f"  - {col}: {count:,} missing ({pct:.2f}%)\n"

    # Check for constant columns
    constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
    if constant_cols:
        result += f"⚠ {len(constant_cols)} constant columns (single unique value):\n"
        for col in constant_cols:
            result += f"  - {col}\n"

    return result


def analyze_numerical_columns(df: pd.DataFrame, numerical_cols: List[str]) -> Tuple[str, List[str]]:
    """Analyze numerical columns with statistics and outlier detection"""
    if not numerical_cols:
        return "\n[3] NUMERICAL ANALYSIS\n" + "-" * 70 + "\n(No numerical columns found)\n", []

    result = "\n[3] NUMERICAL ANALYSIS\n"
    result += "-" * 70 + "\n"

    outlier_cols = []

    for col in numerical_cols:
        result += f"\n{col}:\n"

        # Basic statistics
        stats = df[col].describe()
        result += f"  • Range: {stats['min']:.2f} to {stats['max']:.2f}\n"
        result += f"  • Mean: {stats['mean']:.2f} ± {stats['std']:.2f}\n"
        result += f"  • Median: {stats['50%']:.2f}\n"
        result += f"  • Q1: {stats['25%']:.2f}, Q3: {stats['75%']:.2f}\n"

        # Skewness
        skewness = df[col].skew()
        if abs(skewness) > 1:
            skew_desc = "highly right-skewed" if skewness > 1 else "highly left-skewed"
            result += f"  • Distribution: {skew_desc} (skewness: {skewness:.2f})\n"
        elif abs(skewness) > 0.5:
            skew_desc = "moderately right-skewed" if skewness > 0.5 else "moderately left-skewed"
            result += f"  • Distribution: {skew_desc} (skewness: {skewness:.2f})\n"
        else:
            result += f"  • Distribution: approximately symmetric (skewness: {skewness:.2f})\n"

        # Outlier detection using IQR method
        Q1 = stats['25%']
        Q3 = stats['75%']
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
        if len(outliers) > 0:
            result += f"  ⚠ Outliers detected: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)\n"
            outlier_cols.append(col)
        else:
            result += f"  ✓ No outliers detected\n"

        # Missing values for this column
        missing = df[col].isnull().sum()
        if missing > 0:
            result += f"  ⚠ Missing values: {missing} ({missing/len(df)*100:.2f}%)\n"

    return result, outlier_cols


def analyze_categorical_columns(df: pd.DataFrame, categorical_cols: List[str]) -> str:
    """Analyze categorical columns"""
    if not categorical_cols:
        return "\n[4] CATEGORICAL ANALYSIS\n" + "-" * 70 + "\n(No categorical columns found)\n"

    result = "\n[4] CATEGORICAL ANALYSIS\n"
    result += "-" * 70 + "\n"

    for col in categorical_cols:
        result += f"\n{col}:\n"

        unique_count = df[col].nunique()
        total_count = len(df)

        result += f"  • Unique values: {unique_count}\n"
        result += f"  • Cardinality: {unique_count/total_count*100:.2f}%\n"

        # Missing values
        missing = df[col].isnull().sum()
        if missing > 0:
            result += f"  ⚠ Missing values: {missing} ({missing/len(df)*100:.2f}%)\n"

        # Top values
        if unique_count <= 10:
            result += f"  • Value distribution:\n"
            value_counts = df[col].value_counts()
            for val, count in value_counts.head(10).items():
                result += f"    - {val}: {count} ({count/total_count*100:.2f}%)\n"
        else:
            result += f"  • Top 5 values:\n"
            value_counts = df[col].value_counts()
            for val, count in value_counts.head(5).items():
                result += f"    - {val}: {count} ({count/total_count*100:.2f}%)\n"

        # Check for high cardinality
        if unique_count > total_count * 0.9:
            result += f"  ⚠ High cardinality detected (might be identifier column)\n"

    return result


def analyze_correlations(df: pd.DataFrame, numerical_cols: List[str]) -> Tuple[str, List[Tuple[str, str, float]]]:
    """Analyze correlations between numerical columns"""
    if len(numerical_cols) < 2:
        return "\n[5] CORRELATION ANALYSIS\n" + "-" * 70 + "\n(Need at least 2 numerical columns for correlation analysis)\n", []

    result = "\n[5] CORRELATION ANALYSIS\n"
    result += "-" * 70 + "\n"

    # Calculate correlation matrix
    corr_matrix = df[numerical_cols].corr()

    # Find strong correlations
    strong_correlations = []
    for i in range(len(numerical_cols)):
        for j in range(i+1, len(numerical_cols)):
            corr_value = corr_matrix.iloc[i, j]
            if abs(corr_value) > 0.7:
                strong_correlations.append((numerical_cols[i], numerical_cols[j], corr_value))

    if strong_correlations:
        result += "Strong correlations found (|r| > 0.7):\n"
        for col1, col2, corr in sorted(strong_correlations, key=lambda x: abs(x[2]), reverse=True):
            direction = "positive" if corr > 0 else "negative"
            strength = "very strong" if abs(corr) > 0.9 else "strong"
            result += f"  • {col1} ↔ {col2}: {corr:.3f} ({strength} {direction})\n"
    else:
        result += "No strong correlations (|r| > 0.7) found between numerical columns\n"

    # Show moderate correlations
    moderate_correlations = []
    for i in range(len(numerical_cols)):
        for j in range(i+1, len(numerical_cols)):
            corr_value = corr_matrix.iloc[i, j]
            if 0.5 < abs(corr_value) <= 0.7:
                moderate_correlations.append((numerical_cols[i], numerical_cols[j], corr_value))

    if moderate_correlations:
        result += "\nModerate correlations (0.5 < |r| ≤ 0.7):\n"
        for col1, col2, corr in sorted(moderate_correlations, key=lambda x: abs(x[2]), reverse=True)[:5]:
            direction = "positive" if corr > 0 else "negative"
            result += f"  • {col1} ↔ {col2}: {corr:.3f} (moderate {direction})\n"

    return result, strong_correlations


def generate_insights(df: pd.DataFrame, numerical_cols: List[str], categorical_cols: List[str],
                        outlier_cols: List[str], strong_correlations: List[Tuple[str, str, float]]) -> str:
    """Generate actionable insights from the analysis"""
    result = "\n[6] KEY INSIGHTS & RECOMMENDATIONS\n"
    result += "-" * 70 + "\n"

    insights = []

    # Missing data insights
    missing = df.isnull().sum()
    high_missing = missing[missing / len(df) > 0.1]
    if len(high_missing) > 0:
        for col in high_missing.index:
            pct = high_missing[col] / len(df) * 100
            insights.append(f"⚠ Column '{col}' has {pct:.1f}% missing data - consider imputation or removal")

    # Duplicate insights
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        pct = duplicate_count / len(df) * 100
        insights.append(f"⚠ {duplicate_count} duplicate rows found ({pct:.2f}%) - consider deduplication")

    # Outlier insights
    if outlier_cols:
        insights.append(f"⚠ Outliers detected in {len(outlier_cols)} column(s): {', '.join(outlier_cols[:3])}" +
                        (f" and {len(outlier_cols)-3} more" if len(outlier_cols) > 3 else "") +
                        " - review for data entry errors or valid extreme values")

    # Correlation insights
    if strong_correlations:
        for col1, col2, corr in strong_correlations[:2]:
            if abs(corr) > 0.9:
                insights.append(f"💡 Very strong correlation between '{col1}' and '{col2}' ({corr:.3f}) - " +
                            "consider feature redundancy for modeling")

    # Skewness insights
    for col in numerical_cols[:5]:  # Check top 5 numerical columns
        skewness = df[col].skew()
        if abs(skewness) > 2:
            insights.append(f"📊 Column '{col}' is highly skewed (skewness: {skewness:.2f}) - " +
                            "consider log transformation for modeling")

    # Cardinality insights
    for col in categorical_cols:
        unique_ratio = df[col].nunique() / len(df)
        if unique_ratio > 0.95:
            insights.append(f"🔑 Column '{col}' has very high cardinality ({unique_ratio*100:.1f}%) - " +
                            "likely an identifier, consider removing for analysis")

    # Constant column insights
    constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
    if constant_cols:
        insights.append(f"⚠ {len(constant_cols)} constant column(s) provide no information - consider removing")

    # Data size insights
    if len(df) < 30:
        insights.append(f"⚠ Small dataset ({len(df)} rows) - statistical results may not be reliable")

    # General recommendations
    if len(insights) == 0:
        insights.append("✓ Data quality looks good overall")
        insights.append("💡 Consider domain-specific validation rules")
        insights.append("💡 Proceed with visualization and modeling")

    for i, insight in enumerate(insights, 1):
        result += f"{i}. {insight}\n"

    result += "\n" + "=" * 70 + "\n"

    return result


# endregion

# region Analysis Function

def analyze_csv(file_path: str, analysis_type: str = "comprehensive") -> str:
    """
    Performs comprehensive data analysis on a CSV file, similar to Claude's data analysis tool.
    Generates statistical summaries, data quality checks, correlation analysis, and actionable insights.

    Use when the user wants to:
    - Understand their dataset
    - Get insights and overview of CSV data
    - Perform exploratory data analysis (EDA)
    - Check data quality and issues
    - Find patterns and correlations

    Example queries:
    - 'analyze data.csv'
    - 'give me insights on sales.csv'
    - 'perform data analysis on dataset.csv'
    - 'what are the patterns in customer_data.csv'

    Args:
        file_path: Path to the CSV file to analyze (ask user if not specified)
        analysis_type: Type of analysis to perform:
            - "comprehensive" (default): Full analysis with all sections
            - "quick": Overview and basic statistics only
            - "quality": Focus on data quality issues
            - "statistical": Detailed statistical analysis
            - "correlation": Focus on relationships between variables

    Returns:
        str: Comprehensive analysis report with insights and recommendations
    """

    try:
        # Validate file path
        file_path_obj = Path(file_path)

        if not file_path_obj.exists():
            return f"Error: File '{file_path}' does not exist. Please provide a valid file path."

        if not file_path_obj.suffix.lower() == '.csv':
            return f"Error: File '{file_path}' is not a CSV file. Please provide a CSV file."

        # Read CSV
        df = pd.read_csv(file_path_obj)

        if df.empty:
            return f"Error: File '{file_path}' is empty."

        # Generate analysis based on type
        if analysis_type == "quick":
            # Quick analysis - overview only
            overview, numerical_cols, categorical_cols, datetime_cols = get_dataset_overview(df, file_path)
            stats = "\n[2] QUICK STATISTICS\n" + "-" * 70 + "\n"
            stats += df.describe(include='all').to_string()
            return overview + stats

        elif analysis_type == "quality":
            # Focus on data quality
            overview, numerical_cols, categorical_cols, datetime_cols = get_dataset_overview(df, file_path)
            quality = analyze_data_quality(df)
            insights = generate_insights(df, numerical_cols, categorical_cols, [], [])
            return overview + quality + insights

        elif analysis_type == "statistical":
            # Detailed statistical analysis
            overview, numerical_cols, categorical_cols, datetime_cols = get_dataset_overview(df, file_path)
            numerical_analysis, outlier_cols = analyze_numerical_columns(df, numerical_cols)
            categorical_analysis = analyze_categorical_columns(df, categorical_cols)
            return overview + numerical_analysis + categorical_analysis

        elif analysis_type == "correlation":
            # Focus on correlations
            overview, numerical_cols, categorical_cols, datetime_cols = get_dataset_overview(df, file_path)
            correlation_analysis, strong_corrs = analyze_correlations(df, numerical_cols)
            return overview + correlation_analysis

        else:  # comprehensive (default)
            # Full comprehensive analysis
            overview, numerical_cols, categorical_cols, datetime_cols = get_dataset_overview(df, file_path)
            quality = analyze_data_quality(df)
            numerical_analysis, outlier_cols = analyze_numerical_columns(df, numerical_cols)
            categorical_analysis = analyze_categorical_columns(df, categorical_cols)
            correlation_analysis, strong_corrs = analyze_correlations(df, numerical_cols)
            insights = generate_insights(df, numerical_cols, categorical_cols, outlier_cols, strong_corrs)

            return (overview + quality + numerical_analysis + categorical_analysis +
                    correlation_analysis + insights)

    except pd.errors.EmptyDataError:
        return f"Error: File '{file_path}' is empty or invalid CSV format."
    except pd.errors.ParserError as e:
        return f"Error parsing CSV file: {str(e)}"
    except Exception as e:
        return f"Error analyzing file: {str(e)}"


# endregion
