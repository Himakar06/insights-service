import sweetviz as sv
import pkg_resources

def generate_eda_report(df, output_path="sweetviz_report.html"):
    report = sv.analyze(df)
    report.show_html(filepath=output_path, open_browser=False)
    return output_path
