import json
from pathlib import Path
from datetime import datetime

def generate_markdown_report(json_path, output_md_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    backlinks = data.get("google_backlinks", {}).get("data", [])
    similarweb = data.get("similiarweb_data", {}).get("data", {})

    report = []

    # Title and Overview
    report.append(f"# Website Report: {similarweb.get('SiteName', 'Unknown Site')}\n")
    report.append(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**Description:** {similarweb.get('Description', 'No description available.')}\n")

    # Engagement Metrics
    engagement = similarweb.get("Engagments", {})
    report.append("## Engagement Metrics\n")
    report.append(f"- **Visits:** {engagement.get('Visits', 'N/A')}")
    report.append(f"- **Pages Per Visit:** {engagement.get('PagePerVisit', 'N/A')}")
    report.append(f"- **Time on Site:** {engagement.get('TimeOnSite', 'N/A')} seconds")
    bounce = engagement.get("BounceRate", 0)
    try:
        report.append(f"- **Bounce Rate:** {float(bounce) * 100:.2f}%\n")
    except:
        report.append(f"- **Bounce Rate:** N/A\n")

    # Traffic Sources
    sources = similarweb.get("TrafficSources", {})
    report.append("## Traffic Sources\n")
    for source, value in sources.items():
        try:
            report.append(f"- **{source}:** {float(value) * 100:.2f}%")
        except:
            report.append(f"- **{source}:** N/A")
    report.append("")

    # Keywords
    report.append("## Top Keywords\n")
    for keyword in similarweb.get("TopKeywords", []):
        name = keyword.get("Name", "N/A")
        vol = keyword.get("Volume", "N/A")
        cpc = keyword.get("Cpc", "N/A")
        report.append(f"- **{name}** — Volume: {vol}, CPC: ${cpc}")

    # Backlinks
    report.append("\n## Notable Backlinks\n")
    for link in backlinks[:15]:
        title = link.get("title", "No title")
        url = link.get("url", "#")
        desc = link.get("description", "")
        report.append(f"- **[{title}]({url})** — {desc}")

    # Write to markdown
    with open(output_md_path, "w") as out:
        out.write("\n".join(report))

    print(f"Report saved to: {output_md_path}")


# Example usage
if __name__ == "__main__":
    generate_markdown_report(
        json_path="data-orangerockmediadotcom.json",
        output_md_path="orangerockmedia_report.md"
    )
