import requests
import csv

API_URL = "https://api.gsocorganizations.dev/organizations.json"


def fetch_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()


def matches_filter(value, filter_value):
    """
    Case-insensitive substring match.
    """
    if not filter_value:
        return True
    return filter_value.lower() in str(value).lower()


def save_filtered_students(
    data,
    year=None,
    organization=None,
    student=None,
    category=None,
    technology=None,
    topic=None,
):
    filename_parts = ["gsoc_students"]

    if year:
        filename_parts.append(str(year))
    if organization:
        filename_parts.append(organization.replace(" ", "_"))

    filename = "_".join(filename_parts) + ".csv"

    fieldnames = [
        "year",
        "organization_name",
        "organization_category",
        "student_name",
        "project_title",
        "project_short_description",
        "project_description",
        "project_url",
        "code_url",
        "organization_topics",
        "organization_technologies",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for org in data:
            org_name = org.get("name", "")
            org_category = org.get("category", "")
            org_topics = org.get("topics", [])
            org_technologies = org.get("technologies", [])

            # Organization-level filters
            if not matches_filter(org_name, organization):
                continue
            if not matches_filter(org_category, category):
                continue
            if topic and not any(matches_filter(t, topic) for t in org_topics):
                continue
            if technology and not any(matches_filter(t, technology) for t in org_technologies):
                continue

            years = org.get("years", {})
            for y, year_data in years.items():
                if year and str(year) != y:
                    continue

                projects = year_data.get("projects", [])
                for project in projects:
                    student_name = project.get("student_name", "")

                    if not matches_filter(student_name, student):
                        continue

                    writer.writerow({
                        "year": y,
                        "organization_name": org_name,
                        "organization_category": org_category,
                        "student_name": student_name,
                        "project_title": project.get("title", ""),
                        "project_short_description": project.get("short_description", ""),
                        "project_description": project.get("description", ""),
                        "project_url": project.get("project_url", ""),
                        "code_url": project.get("code_url", ""),
                        "organization_topics": ", ".join(org_topics),
                        "organization_technologies": ", ".join(org_technologies),
                    })

    print(f"Filtered CSV created: {filename}")


def main():
    data = fetch_data()

    # ---- USER FILTERS (edit or automate) ----
    filters = {
        "year": input("Filter by year (optional): ").strip() or None,
        "organization": input("Filter by organization (optional): ").strip() or None,
        "student": input("Filter by student name (optional): ").strip() or None,
        "category": input("Filter by category (optional): ").strip() or None,
        "technology": input("Filter by technology (optional): ").strip() or None,
        "topic": input("Filter by topic (optional): ").strip() or None,
    }

    save_filtered_students(data, **filters)


if __name__ == "__main__":
    main()
