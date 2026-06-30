import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")

DATA_PATH = "dataset/student_performance.csv"
CHARTS_DIR = "charts"
REPORTS_DIR = "reports"


def load_data():
    """Load dataset used in all menu operations."""
    try:
        df = pd.read_csv(DATA_PATH)
        print("Dataset loaded successfully")
        return df
    except FileNotFoundError:
        print(f"Dataset not found at: {DATA_PATH}")
        return None


def show_preview_and_structure(df):
    print("\n--- Preview and Structure ---")
    print(df.head())
    print("Shape:", df.shape)
    print("\nInfo:")
    df.info()
    print("\nDescribe:")
    print(df.describe())
    print("\nColumn Names:")
    print(df.columns)


def run_data_quality_checks(df):
    print("\n--- Data Quality Checks ---")
    print("Missing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nInvalid Attendance:")
    print(df[(df["Attendance"] < 0) | (df["Attendance"] > 100)])

    print("\nInvalid FinalMarks:")
    print(df[(df["FinalMarks"] < 0) | (df["FinalMarks"] > 100)])


def show_summary_metrics(df):
    print("\n--- Summary Metrics ---")
    total_students = len(df)
    average_marks = df["FinalMarks"].mean()
    average_attendance = df["Attendance"].mean()

    print("Total Students:", total_students)
    print("Average Marks:", average_marks)
    print("Average Attendance:", average_attendance)
    print("Highest Marks:", df["FinalMarks"].max())
    print("Lowest Marks:", df["FinalMarks"].min())


def show_category_counts(df):
    print("\n--- Category Counts ---")
    print("Result Count:")
    print(df["Result"].value_counts())

    print("\nGender Count:")
    print(df["Gender"].value_counts())

    print("\nCourse Count:")
    print(df["Course"].value_counts())


def show_course_analysis(df):
    print("\n--- Course Analysis ---")
    course_summary = (
        df.groupby("Course")
        .agg(
            {
                "StudentID": "count",
                "Attendance": "mean",
                "StudyHours": "mean",
                "FinalMarks": "mean",
            }
        )
        .reset_index()
    )
    print(course_summary)

    pass_students = df[df["Result"] == "Pass"]
    total_by_course = df.groupby("Course")["StudentID"].count()
    pass_by_course = pass_students.groupby("Course")["StudentID"].count()
    pass_percentage = ((pass_by_course / total_by_course) * 100).fillna(0)

    print("\nPass Percentage by Course:")
    print(pass_percentage)

    return course_summary


def generate_pass_fail_chart(df):
    os.makedirs(CHARTS_DIR, exist_ok=True)
    plt.figure(figsize=(7, 5))
    sns.countplot(data=df, x="Result", hue="Result", palette="Set2", legend=False)
    plt.title("Pass vs Fail Count")
    plt.xlabel("Result")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/pass_fail_count.png", dpi=300)
    plt.close()
    print(f"Saved: {CHARTS_DIR}/pass_fail_count.png")


def generate_course_avg_marks_chart(df):
    os.makedirs(CHARTS_DIR, exist_ok=True)

    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="Course", y="FinalMarks", estimator="mean", hue="Course", palette="viridis", legend=False)
    plt.title("Average Marks by Course")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/course_avg_marks.png", dpi=300)
    plt.close()
    print(f"Saved: {CHARTS_DIR}/course_avg_marks.png")


def generate_marks_distribution_chart(df):
    os.makedirs(CHARTS_DIR, exist_ok=True)

    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x="FinalMarks", bins=6, kde=True, color="green")
    plt.title("Final Marks Distribution")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/marks_distribution.png", dpi=300)
    plt.close()
    print(f"Saved: {CHARTS_DIR}/marks_distribution.png")


def generate_boxplot_marks_course_chart(df):
    os.makedirs(CHARTS_DIR, exist_ok=True)

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="Course", y="FinalMarks", hue="Course", palette="Set3", legend=False)
    plt.title("Marks Spread by Course")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/boxplot_marks_course.png", dpi=300)
    plt.close()
    print(f"Saved: {CHARTS_DIR}/boxplot_marks_course.png")


def generate_correlation_heatmap_chart(df):
    os.makedirs(CHARTS_DIR, exist_ok=True)

    numeric_df = df[["Attendance", "StudyHours", "FinalMarks"]]
    correlation = numeric_df.corr()

    plt.figure(figsize=(7, 5))
    sns.heatmap(correlation, annot=True, cmap="Greens")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/correlation_heatmap.png", dpi=300)
    plt.close()
    print(f"Saved: {CHARTS_DIR}/correlation_heatmap.png")


def generate_charts(df):
    print("\n--- Generating Charts ---")
    generate_pass_fail_chart(df)
    generate_course_avg_marks_chart(df)
    generate_marks_distribution_chart(df)
    generate_boxplot_marks_course_chart(df)
    generate_correlation_heatmap_chart(df)

    print(f"Charts saved in: {CHARTS_DIR}")


def print_chart_menu():
    print("\n----- Chart Sub-Menu -----")
    print("1. Pass vs Fail Count")
    print("2. Average Marks by Course")
    print("3. Final Marks Distribution")
    print("4. Marks Spread by Course (Boxplot)")
    print("5. Correlation Heatmap")
    print("6. Generate All Charts")
    print("0. Back to Main Menu")


def handle_chart_menu(df):
    while True:
        print_chart_menu()
        chart_choice = input("Enter chart choice: ").strip()

        if chart_choice == "1":
            generate_pass_fail_chart(df)
        elif chart_choice == "2":
            generate_course_avg_marks_chart(df)
        elif chart_choice == "3":
            generate_marks_distribution_chart(df)
        elif chart_choice == "4":
            generate_boxplot_marks_course_chart(df)
        elif chart_choice == "5":
            generate_correlation_heatmap_chart(df)
        elif chart_choice == "6":
            generate_charts(df)
        elif chart_choice == "0":
            print("Returning to main menu...")
            break
        else:
            print("Invalid chart choice. Please enter a valid option.")


def show_feature_target_info():
    print("\n--- Feature and Target ---")
    features = ["Attendance", "StudyHours", "PreviousMarks", "AssignmentScore"]
    target = "FinalMarks"

    print("Feature Columns:", features)
    print("Target Column:", target)


def save_reports(df):
    print("\n--- Saving Reports ---")
    os.makedirs(REPORTS_DIR, exist_ok=True)

    course_summary = show_course_analysis(df)
    course_summary.to_csv(f"{REPORTS_DIR}/course_summary_report.csv", index=False)

    result_count = df["Result"].value_counts().rename_axis("Result").reset_index(name="Count")
    result_count.to_csv(f"{REPORTS_DIR}/result_count_report.csv", index=False)

    print(f"Reports saved in: {REPORTS_DIR}")


def run_all(df):
    show_preview_and_structure(df)
    run_data_quality_checks(df)
    show_summary_metrics(df)
    show_category_counts(df)
    show_course_analysis(df)
    generate_charts(df)
    show_feature_target_info()
    save_reports(df)


def print_menu():
    print("\n===== Student EDA Menu =====")
    print("1. Preview and Structure")
    print("2. Data Quality Checks")
    print("3. Summary Metrics")
    print("4. Category Counts")
    print("5. Course Analysis")
    print("6. Generate Charts")
    print("7. Feature and Target Info")
    print("8. Save Reports")
    print("9. Run Complete EDA")
    print("0. Exit")


def main():
    print("Libraries imported successfully")
    df = load_data()

    if df is None:
        return

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_preview_and_structure(df)
        elif choice == "2":
            run_data_quality_checks(df)
        elif choice == "3":
            show_summary_metrics(df)
        elif choice == "4":
            show_category_counts(df)
        elif choice == "5":
            show_course_analysis(df)
        elif choice == "6":
            handle_chart_menu(df)
        elif choice == "7":
            show_feature_target_info()
        elif choice == "8":
            save_reports(df)
        elif choice == "9":
            run_all(df)
        elif choice == "0":
            print("Exiting menu. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
