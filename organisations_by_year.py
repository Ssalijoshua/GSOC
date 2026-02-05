import requests
import csv

def fetch_gsoc_organizations(year: int):
    """
    Fetch GSOC organizations for a given year.
    """
    url = f"https://api.gsocorganizations.dev/{year}.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def save_to_csv(data: dict, year: int):
    """
    Save GSOC organizations data to a CSV file.
    """
    filename = f"gsoc_organizations_{year}.csv"

    organizations = data.get("organizations", [])

    fieldnames = [
        "year",
        "name",
        "category",
        "description",
        "url",
        "num_projects",
        "projects_url",
        "contact_email",
        "mailing_list",
        "irc_channel",
        "twitter_url",
        "blog_url",
        "topics",
        "technologies"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for org in organizations:
            writer.writerow({
                "year": year,
                "name": org.get("name", ""),
                "category": org.get("category", ""),
                "description": org.get("description", ""),
                "url": org.get("url", ""),
                "num_projects": org.get("num_projects", 0),
                "projects_url": org.get("projects_url", ""),
                "contact_email": org.get("contact_email", ""),
                "mailing_list": org.get("mailing_list", ""),
                "irc_channel": org.get("irc_channel", ""),
                "twitter_url": org.get("twitter_url", ""),
                "blog_url": org.get("blog_url", ""),
                # Convert lists to comma-separated strings
                "topics": ", ".join(org.get("topics", [])),
                "technologies": ", ".join(org.get("technologies", [])),
            })

    print(f"CSV file created: {filename}")


def main():
    try:
        year = int(input("Enter GSOC year (e.g. 2025): ").strip())
        data = fetch_gsoc_organizations(year)
        save_to_csv(data, year)
    except ValueError:
        print("Please enter a valid year (e.g. 2025).")
    except requests.RequestException as e:
        print("Failed to fetch data:", e)


if __name__ == "__main__":
    main()
