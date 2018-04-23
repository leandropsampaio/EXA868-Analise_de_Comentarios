from models.business.WebScrapping import WebScrapping

webscrapping = WebScrapping()
url = "https://www.amazon.com.br/Trilogia-dos-Espinhos-Mark-Lawrence/product-reviews/8594540256/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
webscrapping.set_url(url)
#webscrapping.scrap_div(True, "../scrape_pages/Amazon/Trilogia_dos_Espinhos_1.html")
webscrapping.automatic_scrape(True, "../scrape_pages/Amazon/")
