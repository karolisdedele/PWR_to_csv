from lxml import etree
import pandas as pd


review_data = pd.DataFrame(columns=['productid','product_name','review_title','ReviewText',"rating",'email_address',
                                    'review_submit_date','DisplayName','location',"NumPositiveFeedbacks","NumNegativeFeedbacks",
                                    'verified_purchase', 'verified_reviewer', 'image_url','image_caption',
                                    'locale','review_id','campaign_id',"Recommended","response_text",'response_department_name',
                                    'response_department'])
tree = etree.parse("review_data_complete.xml")
root = tree.getroot()

locale = "en_US"
review_id= "skgn-"
review_id_number = 0
campaign_id = 'imported_reviews_'
department_name = "Skagen"

def get_text(elem, fallback_value=None):
    return elem.text if type(elem) is not type(None) else fallback_value

def strip_url(elem, fallback_value=None):
    return elem.text[2:] if type(elem) is not type(None) else fallback_value

def get_length(elem, fallback_value=0):
    return len(elem.text) if type(elem) is not type(None) else fallback_value

review_data['productid'] = [bar.getparent().getparent().find("pageid").text for bar in root.findall(".//fullreview")]
review_data['product_name'] = [bar.getparent().getparent().find("name").text for bar in root.findall(".//fullreview")]
review_data['review_title'] = [bar.find("headline").text for bar in root.findall(".//fullreview")]
review_data['ReviewText'] = [bar.find("comments").text for bar in root.findall(".//fullreview")]
review_data['rating'] = [bar.find("overallrating").text for bar in root.findall(".//fullreview")]
review_data['email_address'] = [get_text(bar.find("email_address_from_user")) for bar in root.findall(".//fullreview")]
review_data['review_submit_date'] = [bar.find("createddate").text for bar in root.findall(".//fullreview")]
review_data['DisplayName'] = [bar.find("nickname").text for bar in root.findall(".//fullreview")]
review_data['location'] = [bar.find("location").text for bar in root.findall(".//fullreview")]
review_data['Recommended'] = ["True" if get_text(bar.find("bottom_line"))=="recommended" else "" for bar in root.findall(".//fullreview")]
review_data['NumPositiveFeedbacks'] = [bar.find("helpfulvotes").text for bar in root.findall(".//fullreview")]
review_data['NumNegativeFeedbacks'] = [bar.find("nothelpfulvotes").text for bar in root.findall(".//fullreview")]
review_data['verified_purchase'] = ["True" if bar.find("confirmstatusgroup")[0].text == "Verified Purchaser" else "" for bar in root.findall(".//fullreview")]
review_data['verified_reviewer'] = [bar.find("confirmstatusgroup")[1].text if len(bar.find("confirmstatusgroup")) > 1 else "" for bar in root.findall(".//fullreview")]
review_data['image_url'] = [strip_url(bar.find(".//fullimagelocation")) for bar in root.findall(".//fullreview")]
review_data['image_caption'] = [get_text(bar.find(".//caption")) for bar in root.findall(".//fullreview")]
review_data['locale'] = [locale for bar in root.findall(".//fullreview")]
review_data['review_id'] = [review_id+str(bar.find("id").text) for bar in root.findall(".//fullreview")]
review_data['campaign_id'] = [campaign_id+locale for bar in root.findall(".//fullreview")]
review_data['response_text'] = [get_text(bar.find(".//response")) for bar in root.findall(".//fullreview")]
review_data['response_department_name'] = [department_name if get_length(bar.find("merchant_response")) > 1 else "" for bar in root.findall(".//fullreview")]
review_data['response_department'] = [department_name if get_length(bar.find("merchant_response")) > 1 else "" for bar in root.findall(".//fullreview")]


review_data_deduped = review_data.drop_duplicates(subset=['review_title','ReviewText','rating','email_address','review_submit_date'], keep="first")
review_data_deduped.to_csv("output-without-duplicates.csv",index=False,encoding='utf-8')
review_data.to_csv("output-with-duplicates.csv",index=False,encoding='utf-8')
