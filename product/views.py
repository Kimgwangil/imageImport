from django.views import View
import redshift_connector
import pandas as pd
from db_settings import ENGINE_POSTGRES_REDSHIFT, HOST, PASSWORD, USER, DATABASE
from django.shortcuts import render

# class ImgView(View):
def product_img_lst(request):
  conn = redshift_connector.connect(
    host= HOST,
    database= DATABASE,
    user= USER,
    password= PASSWORD,
  )

  cursor = conn.cursor()

  sql = """
    
    select b.prdt_cd                      as prdt_cd
        , a.erp_goods_no                  as recmd_prdt
        , item_nm                         as item_nm
        , exp_seq                         as seq
        , decode(a.exp_type_cd,'10','추천','20','유사') as recmd
        , url                                     as img_url
    from if_ec.ip_prdt_recommend a
    join prcs.db_prdt b
      on b.part_cd = a.dsgn_grp_no 
    join prcs.dw_prdt_img c 
      on substring(c.prdt_cd, 5) = substring(a.erp_goods_no, 1, 9)
    and color_cd = substring(a.erp_goods_no, 11)
    where 1=1
      and b.brd_cd = 'X'
      and c.default_yn = true
      and c.img_from = 'ONLINE'
    order by b.prdt_cd desc,a.exp_type_cd, a.exp_seq
    ;

    """

  # result = cursor.fetchall()

  # df = pd.DataFrame(result, columns=['prdt_cd', 'img_url'])
  df = pd.read_sql(sql, conn)
  # print(df)
  img = df.to_dict('records')

  dict = {
        'prdt_cd'     : '',
        'item_nm'     : '',
        'recmd'       : [
                          {
                          'id' : '',
                          'seq': 0,
                          'recmd_prdt' : '',
                          'img_url' : ''
                          }
                        ]
        }

  data = []

  for i in range(len(img)):
      if img[i]["prdt_cd"] != dict["prdt_cd"]:
          dict = {
          'prdt_cd'     : '',
          'item_nm'     : '',
          'recmd'       : []
          }
          
          dict['prdt_cd']    = img[i]['prdt_cd']
          dict['item_nm']    = img[i]['item_nm']
          dict['recmd'].append({
                                'id'         : img[i]['recmd'],
                                'seq'        : img[i]['seq'],
                                'recmd_prdt' : img[i]['recmd_prdt'],
                                'img_url'    : img[i]['img_url']
                              })
          data.append(dict)
      else:
          dict["recmd"].append({
                                'id'         : img[i]['recmd'],
                                'seq'        : img[i]['seq'],
                                'recmd_prdt' : img[i]['recmd_prdt'],
                                'img_url'    : img[i]['img_url']
                              })

  return render(request, 'product/index.html', {'imgs': data})
  # return render(request, 'product/index.html', {'imgs': data})