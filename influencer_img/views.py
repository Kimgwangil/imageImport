# from http.client import HTTPResponse
from django.views import View
# from django.http import HttpResponse, JsonResponse

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from db_settings import ENGINE_POSTGRES_REDSHIFT

# # def index(request):
# #   return HttpResponse("hi")
# class ImgImport(View):
#   def get():
#     red_engine = create_engine(ENGINE_POSTGRES_REDSHIFT)

#     Session = sessionmaker(bind = red_engine)
#     session = Session

#     result = session.qu.ery("""select prdt_cd from unicorn.temp_prdt_val limit 10""").all()
#     results = []

#     for row in result:
#       results.append(row) 


#     return HttpResponse(results)



# from sqlalchemy     import create_engine
# from sqlalchemy.orm import sessionmaker


# Session = sessionmaker(bind = red_engine)
# session = Session

# result = session.query("""select prdt_cd from unicorn.temp_prdt_val limit 10""").all()

# for row in result:
#   print(row.prdt_cd)

import redshift_connector
import pandas as pd
from db_settings import ENGINE_POSTGRES_REDSHIFT, HOST, PASSWORD, USER, DATABASE
from django.shortcuts import render

# class ImgView(View):
def influencer_img_lst(request):
  conn = redshift_connector.connect(
    host= HOST,
    database= DATABASE,
    user= USER,
    password= PASSWORD,
  )

  cursor = conn.cursor()

  sql = """
    select dsgn_grp_no, image_url, item_nm
    from if_ec.ii_influencer_contents a
    join prcs.db_prdt b on a.brand_no || a.sn_cd || a.dsgn_grp_no = b.prdt_cd
    where 1=1
    order by dsgn_grp_no, image_url
    """

  # result = cursor.fetchall()

  # df = pd.DataFrame(result, columns=['prdt_cd', 'img_url'])
  df = pd.read_sql(sql, conn)
  # print(df)
  img = df.to_dict('records')

  dict = {
  'dsgn_grp_no' : '',
  'img_url' : [],
  'item_nm' : ''
  }

  data = []

  for i in range(len(img)):
    if img[i]["dsgn_grp_no"] != dict["dsgn_grp_no"]:
      dict = {
        'dsgn_grp_no' : '',
        'img_url' : [],
        'item_nm' : ''
      }
      dict["dsgn_grp_no"] = img[i]["dsgn_grp_no"]
      dict["item_nm"] = img[i]["item_nm"]
      dict["img_url"] = []
      dict["img_url"].append(img[i]["image_url"])
      data.append(dict)
    else:
      dict["img_url"].append(img[i]["image_url"])


  return render(request, 'influencer_img/index.html', {'imgs': data})



    # print(data["dsgn_grp_no"][0])
    # result = {}

    # for i in data:
    #   i[0]