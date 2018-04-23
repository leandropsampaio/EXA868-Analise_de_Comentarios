from models.business.WebScrapping import WebScrapping

webscrapping = WebScrapping()
url = "https://www.amazon.com.br/Trilogia-dos-Espinhos-Mark-Lawrence/product-reviews/8594540256/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
webscrapping.seturl(url)
webscrapping.scrapdiv()