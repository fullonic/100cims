import requests
import bs4


def _get_coordinates(cim_info_tag: bs4.Tag) -> tuple:
    """Get coordinate data from cim page."""
    lat_info = cim_info_tag.select("div.fw-bold:nth-child(6)")[0].text
    lat = float(lat_info[:-1])
    lng_info = cim_info_tag.select("div.col-6:nth-child(8)")[0].text
    lng = float(lng_info[:-1])
    return lat, lng


def complementary_info(url=None):
    """Scrape cim detailed information from cim page."""
    if url.startswith("https"):
        page = requests.get(url).text
    else:
        page = url

    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(page, features="html.parser")
    cim_info_tag: bs4.Tag = soup.select("div.bg-primari:nth-child(3)")[0]
    # comarca info
    comarca: str = cim_info_tag.select("div.fw-bold:nth-child(2)")[0].text
    comarca = comarca.strip()
    # altitude
    alt: str = cim_info_tag.select("div.fw-bold:nth-child(4)")[0].text
    altitude: int = int(alt[:-2])
    # img
    img_tag = soup.select(".attachment-post-thumbnail")[0]
    img_url = img_tag.attrs["src"]
    return {"comarca": comarca, "altitude": altitude, "img_url": img_url}

