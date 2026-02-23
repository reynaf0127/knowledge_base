import requests
from pathlib import Path


def download_image_and_create_md(
        image_url: str, 
        output_dir: str = "/Users/reyna.feng/Documents/knowledge_obisidian",
        ):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Extract filename
    image_name = image_url.split("/")[-1]
    image_path = output_path / image_name

    # Download image
    response = requests.get(image_url, timeout=30)
    response.raise_for_status()

    with open(image_path, "wb") as f:
        f.write(response.content)

    # Create markdown file
    md_path = output_path / (image_name.replace(".png", ".md"))

    md_content = f"""# Pipeline Result

Here is my pipeline result.

![{image_name}]({image_name})
"""

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"✅ Image saved to: {image_path}")
    print(f"✅ Markdown saved to: {md_path}")


# Example usage
url = "https://tempfile.aiquickdraw.com/workers/nano/image_1771717909295_vfovjz.png"
download_image_and_create_md(url)