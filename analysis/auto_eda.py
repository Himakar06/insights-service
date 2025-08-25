from ydata_profiling import ProfileReport

def generate_eda(df, output_path = "eda_report.html"):
    profile = ProfileReport(df, title = "Auto EDA Report", explorative = True)
    profile.to_file(output_path)
    return output_path