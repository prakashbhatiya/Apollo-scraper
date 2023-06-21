# # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                   #
#   Name: Prakash bhatiya                           #
#   Date: 24/05/2023                                #
#   Desc: Scraping Apollo Details                   #
#   Email: bhatiyaprakash991@gmail.com              #
#                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # #
import json, os,re
from utils import save_response, process_request
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
import pandas as pd
from openpyxl import Workbook
import xlsxwriter


class InListValidator(Validator):
    def validate(self, document):
        text = document.text
        if text:
            keywords = [keyword.strip() for keyword in text.split(',')]
            for keyword in keywords:
                if keyword not in suggestions:
                    raise ValidationError(message='Invalid input. Please choose from the suggestions.')

class Apollo:

# >> just for decoration
  def intro(self):
      print()
      print('  # # # # # # # # # # # # #  # # # # # # # #')
      print('  #                                        #')
      print('  #     SCRAPER FOR APOLLO DETAILS         #')
      print('  #           By: PRAKASH BHATIYA          #')
      print('  #             Dt: 24-05-2023             #')
      print('  #      bhatiyaprakash991@gmail.com       #')
      print('  #    **Just for Educational Purpose**    #')
      print('  #                                        #')
      print('  # # # # # # # # # # # # #  # # # # # # # #')
      print()

  def get_headers(self) -> dict:
    """Method return header

    Returns:
        dict: dictionery format
    """
    return {
    'authority': 'app.apollo.io',
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.9',
    'content-type': 'application/json',
    'cookie': 'GCLB=CJ2T96CVmcSFJA; ZP_Pricing_Split_Test_Variant=22Q4_EC_X49; remember_token_leadgenie_v2=eyJfcmFpbHMiOnsibWVzc2FnZSI6IklqWTBOVGhrTkRobVpUaG1NalZqTURKaU0yTmxOVFpqWlY5c1pXRmtaMlZ1YVdWamIyOXJhV1ZvWVhOb0lnPT0iLCJleHAiOiIyMDIzLTA3LTA5VDA3OjUzOjU0Ljk3NloiLCJwdXIiOiJjb29raWUucmVtZW1iZXJfdG9rZW5fbGVhZGdlbmllX3YyIn19--be971f6ddda5b36136ce2c628c11e7200f940a22; intercom-device-id-dyws6i9m=32ff82db-a9b2-41ce-8cad-e59b771a0c31; __stripe_mid=e08984ce-f785-4fb2-9192-738dc92a840328f08d; __stripe_sid=7014827c-bbf6-45ca-bd96-b76e5259f49bb8ff5e; X-CSRF-TOKEN=dWJ5ul9I77Uth6a3ZweLgH3Q4zcahrZGpqnkCFZUQFTTT1vExETmcT_6ipTA7wzm09_ixyzJMrDJVqg4YT_1xA; _leadgenie_session=vYXa4R9mGODi5XbqA0snvmKvZid5FZ1R74KzmRFXoVguVJXbGMr6eQzllLOM090aMTNX8ShM%2Bjpftplicp6mVcX3A4zTRjyEwvDBLqQeYW6Hfav%2B1ks9hQuCvumZLkORKggQu36pChgwmLC6zUnpufyV9B%2FCEWU%2B3AJ2sCuNRu6nfr%2FFi%2BtBzh14dgqPT53kaFq9EPMbjWAxHCs155fpKC8NUaQI1EMsFhvTzbxgQoq%2BRS5b7UdsNts1p2ubQXS0ddXBwPnJSeVVCp690guOcR8JbwdYa6gREyw%3D--O%2BVcCQG7VzwPvvLz--xUGZRtWW%2BUfgaRenLkTTyQ%3D%3D; intercom-session-dyws6i9m=N21WZ3NZUmx5Sk5VSXBGWWUzVFp0c0lwa1RpMlBkVm44aXJ2OS96dTVOUTNSSEh3ZituZ09VU1dNWGRNSEhJVi0tNWRvNHNwbFRrT3pUdXlLZ21PU1QvQT09--81c18457592afdfd1a56c1caa980d48fb3b4d500; _dd_s=rum=0&expire=1686298294890; X-CSRF-TOKEN=_YOsaKXErebwP6-L-OegeiewN1aPKWSONw1QqkU8D-1bro4WPsikIuJCg6hfDyccib82prlm4HhY8hyacle6fQ; _leadgenie_session=6PO2ShWYKNC91Z9yL5oel1jriKeKP%2FzwR%2F7I%2BIOkR2JyX1R7s8TjEnvFzN5%2BABppvzoOdaw5XqUZUWndHMrmFR7I391b1Bmuf2WTYYwIFYUshs3D8pSQ3ZfLZkSe%2FChNR5axqsamMpLMo%2BXo7g3166%2FiwHpKzh%2Bd9MZVjspUrOeFq5o25PoQxFOU33GuKB42G1%2Bzns7yS4LEs8kQ6Gvmos4MjFOSnXC%2Fg6OPX6h4aRKG4IbkKJx%2BpRtrc1AYvs7bonhrHTU0tVWowTi2Q5atrrkeRY8Hf%2BWLqDw%3D--7v6nirflMb8xaHX3--RjAsX%2FtSINfgKTXVNNx48A%3D%3D',
    'origin': 'https://app.apollo.io',
    'referer': 'https://app.apollo.io/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-csrf-token': 'dWJ5ul9I77Uth6a3ZweLgH3Q4zcahrZGpqnkCFZUQFTTT1vExETmcT_6ipTA7wzm09_ixyzJMrDJVqg4YT_1xA'
  }

  def get_payload(self, label_id=None, type=None, job_title=None, location=None, keyword=None, employee_id=None, page=None) -> dict:
    """Method return payload

    Args:
        type (_type_, optional): String. Defaults to None.
        job_title (_type_, optional): list. Defaults to None.
        location (_type_, optional): list. Defaults to None.
        keyword (_type_, optional): list. Defaults to None.
        employee_id (_type_, optional): String. Defaults to None.
        page (_type_, optional): _description_. Defaults to None.

    Raises:
        Exception: _description_

    Returns:
        dict: _description_
    """

    if type == "search":
      payload = {
        "finder_view_id": "5b6dfc5a73f47568b2e5f11c",
        "page": page,
        "included_organization_keyword_fields": [
            "tags",
            "name"
        ],
        "person_titles": job_title,
        "person_locations": location,
        "organization_industry_tag_ids": keyword,
        "display_mode": "explorer_mode",
        "per_page": 25,
        "open_factor_names": [],
        "num_fetch_result": 1,
        "context": "people-index-page",
        "show_suggestions": False,
        "ui_finder_random_seed": "o5hrxq9yva",
        "cacheKey": 1684845502666
      }
      return json.dumps(payload)
    elif type == "email":
      return json.dumps({
        "contact_label_ids": [
          label_id
        ],
        "prospected_by_current_team": [
          "yes"
        ],
        "page": page,
        "display_mode": "explorer_mode",
        "per_page": 200,
        "open_factor_names": [],
        "num_fetch_result": 13,
        "context": "people-index-page",
        "show_suggestions": False,
        "ui_finder_random_seed": "w3vz70l5hz",
        "cacheKey": 1686297394921
      })
    else:
      raise Exception(f"Invalid request type of \'{type}\'")

  def get_employee_details(self) -> dict:
    """method for getting employee details

    Returns:
        dict: list of dict
    """
    url = "https://app.apollo.io/api/v1/mixed_people/search"
    response = process_request("POST", url, headers=self.get_headers(), payload=self.get_payload(""))
    json_resp = response.json()
    return json_resp["people"]

  def open_file(self, filename=None, path=None) -> json:
        """this method for opening a file

        Args:
            filename (_type_, optional): name of the file to open. Defaults to None.
            path (_type_, optional): path of the file. Defaults to None.

        Returns:
            json: json data
        """
        json_path = os.path.join(os.path.dirname(__file__), path)
        with open(os.path.join(json_path, filename), "r", encoding="utf-8") as category:
            text = json.load(category)
        return text

  def get_list(self):
    ""
    url = "https://app.apollo.io/api/v1/auth/additional_bootstrapped_data"
    payload = {}
    response = process_request("GET", url, headers=self.get_headers(), payload=payload)
    json_resp = response.json()
    save_response(json_resp['bootstrapped_data']['labels'], "data_list.json", os.path.join(os.path.dirname(__file__), "Data", "apollo"))

  def convert_xslx(self):
    ""
    try:
      import pandas
      pandas.read_json("data/apollo/Combined_Wedding_&_Event.json").to_excel("Data/apollo/Combined_Wedding_&_Event.xlsx")
    except Exception as e:
      print("Exception in convert_xslx", str(e))

  def get_email(self) ->list or None:
    """method for get emails

    Args:
        employee_id (str): list of data

    Returns:
        list or None: list of data or None
    """
    url = "https://app.apollo.io/api/v1/mixed_people/search"
    page = 1
    contact_label_ids = self.open_file("data_list.json", os.path.join(os.path.dirname(__file__), "Data", "apollo"))
    for label in contact_label_ids:
      email_list = []
      while True:
        response = process_request("POST", url, headers=self.get_headers(), payload=self.get_payload(label['id'], type="email", page=page))
        json_resp = response.json()
        try:
          if response.status_code == 200:
            if json_resp['people']:
              data = json_resp['people']
            elif json_resp['contacts']:
              data = json_resp['contacts']
            else:
              filename = label['name'].replace(" ", "_")
              save_response(email_list, f"{filename}.json", os.path.join(os.path.dirname(__file__), "Data", "apollo"))
              # >> call here convert file method so need to give static file name
              # >> self.convert_xslx(filename)
              break
            for people in data:
              if people['email'] in email_list:
                continue
              save_response(people, "detalis.json", os.path.join(os.path.dirname(__file__), "Data", "apollo"))
              if people['email']:
                try:
                  raw_number = people['phone_numbers'][0]['raw_number']
                  type =  people['phone_numbers'][0]['type']
                except Exception:
                  raw_number = None
                  type = None
                try:
                  email = people['email']
                except Exception:
                  email = people['contact_emails']['email']
                try:
                  linkedin_url = people['linkedin_url']
                except Exception:
                  linkedin_url = None
                try:
                  twitter_url = people['account']['twitter_url']
                except Exception:
                  twitter_url = None
                try:
                  github_url = people['github_url']
                except Exception:
                  github_url = None
                try:
                  facebook_url = people['account']['facebook_url']
                except Exception:
                  facebook_url = None
                email_list.append({
                  "id": people['id'],
                  "first_name": people['first_name'],
                  "last_name": people['last_name'],
                  "name": people['name'],
                  "headline": people['headline'],
                  "title": people['title'],
                  "email": email,
                  "email_status": people['email_status'],
                  "linkedin_url": linkedin_url,
                  "photo_url": people['photo_url'],
                  "twitter_url": twitter_url,
                  "github_url": github_url,
                  "facebook_url": facebook_url,
                  "extrapolated_email_confidence": people['extrapolated_email_confidence'],
                  "organization_name": people['organization_name'],
                  "present_raw_address": people['present_raw_address'],
                  "sanitized_phone": people['sanitized_phone'],
                  "raw_number": raw_number,
                  "type": type,
                })
            page += 1
            continue
        except Exception as e:
          print("Exception ::", str(e))

  def client_input(self) -> None:
    """method for client input

    Returns:
        _type_: _description_
    """
    key_list = []
    while True:
      # Read input from the user with suggestions enabled and validator
      user_input = prompt('Enter keywords (separated by commas): ', completer=completer, validator=InListValidator())

      if user_input:
          # Split input into individual keywords
          keywords = [keyword.strip() for keyword in user_input.split(',')]
          print("You entered the following keywords:")
          for keyword in keywords:
            print(keyword.strip())
            key_list.append(keyword.strip())
          break
    return key_list

  def get_tags(self, input_keyword=None) -> list:
    """method for get tags

    Args:
        input_keyword (_type_, optional): list of data. Defaults to None.

    Returns:
        list: return list
    """
    url = "https://app.apollo.io/api/v1/tags/search?q_tag_fuzzy_name=&kind=linkedin_industry&display_mode=fuzzy_select_mode&cacheKey=1684850858137"
    payload = {}
    response = process_request("GET", url, headers=self.get_headers(), payload=payload)
    json_resp = response.json()
    tag_key_list = []
    while True:
      for inp in input_keyword:
        for tag in json_resp['tags']:
          if inp == tag['cleaned_name']:
            tag_key_list.append(tag['id'])
      return tag_key_list

  def create_data_format(self, data=None):
    detail_list = []
    for value in data:
      try:
        contact_location = value['present_raw_address']
      except Exception:
        contact_location = None
      try:
        email = value['email']
      except Exception:
        email = None
      try:
        employee = value['organization']['persona_counts']
      except Exception:
        employee = None
      try:
        if value['organization']['website_url']:
          youtube_link = apollo.get_link(value['organization']['website_url'])
          if not youtube_link:
            continue
          detail_list.append({
            "name": value['name'],
            "title": value['title'],
            "comapnay": value['organization']['name'],
            "email": email,
            "contact_location": contact_location,
            "Employee": employee,
            "youtube_link": youtube_link
            })
      except Exception:
        continue
    return detail_list

  def check_user_input_type(self, inpt=None):
    job_title, location, input_keyword = [], [], []
    if type == "auto":
      job_title = inpt['title']
      location = inpt ["location"]
      input_keyword = inpt['keyword']

      for inp in input_keyword:
        if not inp in suggestions:
          # save_response(search_list, f"{title_index}.json", os.path.join(os.path.dirname(__file__), "Data", "apollo"))
          return f"[i] This keyword [----{inp}----] not present in suggestion list"
    else:
      print("Enter keyword from folloing list\n\n")
      print(suggestions)
      print("\n\n")

      job_title = [input("Enter Job Title::")]
      location = [input("Enter Location::")]
      input_keyword = self.client_input()
    return {
      "job_title": job_title,
      "location": location,
      "input_keyword": input_keyword
    }

  def search_people(self) -> list or dict:
    """method for searching people

    Returns:
        list or dict: return list or dict
    """
    title_index = 0
    urls = []
    for inpt in inputs:
      user_input = self.check_user_input_type(inpt=inpt)

      keyword = self.get_tags(input_keyword=user_input['input_keyword'] or None)
      url = "https://app.apollo.io/api/v1/mixed_people/search"
      page = 1
      while True:
        payload = self.get_payload(type="search", keyword=keyword or [""], job_title=user_input['job_title'] or [""], location=user_input['location'] or [""], page=page or None)

        response = process_request("POST", url, headers=self.get_headers(), payload=payload)
        if response.status_code == 200:
          json_resp = response.json()
          if json_resp['people']:
            data = json_resp['people']
          elif json_resp['contacts']:
            data = json_resp['contacts']
          else:
            break

          urls.append(data)
          if page == 10: # >> Use static because sometime many pages are there
            detail_list = []
            for data in urls:
              detail_list.append(self.create_data_format(data=data))
            return detail_list
          page += 1
          continue
        else:
          page += 1
          continue
      title_index += 1
    # return urls

  def get_youtube_channel(self, text):
    youtube_link = []
    matches = re.findall(r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:channel|user)\/[a-zA-Z0-9_-]+|youtu\.be\/[a-zA-Z0-9_-]+)", text)
    for match in matches:
      if "youtube" in match:
        youtube_link.append(match)
    return youtube_link

  def get_link(self, url):
    payload = {}
    try:
      payload = {}
      response = process_request("GET", url, headers=self.get_headers(), payload=payload)
      if not response:
        return None
      if response and response.status_code == 200:
        text = response.text
        links = self.get_youtube_channel(text)
      return list(set(links))
    except Exception as e:
      print("Exception:", str(e))

  def get_suggestions(self):
    url = "https://app.apollo.io/api/v1/tags/search?q_tag_fuzzy_name=&kind=linkedin_industry&display_mode=fuzzy_select_mode&cacheKey=1684850858137"
    payload = {}
    response = process_request("GET", url, headers=self.get_headers(), payload=payload)
    json_resp = response.json()
    tag_key_list = []
    for tag in json_resp['tags']:
      tag_key_list.append(tag['cleaned_name'])
    return tag_key_list


if __name__ == "__main__":

  apollo = Apollo()
  apollo.intro()
  # apollo.get_list()
  apollo.convert_xslx()
  email_list = apollo.get_email()

  save_response(email_list, "email_list.json", os.path.join(os.path.dirname(__file__), "Data", "apollo"))


  # >> Get Config Data
  suggestions = apollo.get_suggestions()
  config_data = apollo.open_file("config.json", os.path.join(os.path.dirname(__file__), "Data", "apollo"))
  type = config_data['type']
  inputs = config_data['user_inputs']
  completer = WordCompleter(suggestions)


  datas = apollo.search_people()
  # >> Get urls from data
  save_response(datas, "final_output.json", os.path.join(os.path.dirname(__file__), "Data", "apollo"))