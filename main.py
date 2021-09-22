from OilReport import Investing, OilPrice, CMEGroup
from pandas import read_csv, DataFrame
import getpass
 

class Report:
    def __init__(self):
        print("Initializing...")
        try:
            with open('secret.txt', 'r') as f:
                #If file is used, make sure to hash password and email!!!!!!!!!
                self.email = f.readline()
                self.email = [EMAIL ADDRESS]
                self.password = f.readline()
                UserWarning("This is a risky method, consider inputs only or Hashing")
        except:
            print("Enter Email Details ")
            try:
                self.email = input("Email Address: ")
                self.password = getpass.getpass("Password: ")
            except Exception as error:
                print('ERROR', error)
            
            
            
        self.subject = "CERES DAILY OIL REPORT"
        self.recipients = list(read_csv("email_list.csv")["Email"])


    def html_email(self):
        investing = Investing()
        oilprice = OilPrice()
        cme = CMEGroup()

        cl = [investing, oilprice, cme]

        price_table = DataFrame()
        for c in cl:
            price_table = price_table.append(c.get_basic_info())

        oil = price_table.to_html(index=False, justify="center", border=0).replace("\n", "")

        #STYLE
        oil = oil.replace('<table border="0" class="dataframe">', '<table border="0" class="dataframe" align="center" style=" font-family: Georgia, Times New Roman, Times, serif; border-collapse: collapse; width: 80%;">')
        oil = oil.replace("<th>", '<th style="  background-color: black; color: white; text-transform: uppercase;border-bottom: 3px solid #b9bcd3; padding: 8px;">')
        oil = oil.replace("<td>", '<td style="   border-bottom: 3px solid #b9bcd3; padding: 8px;border-bottom: 3px solid #b9bcd3; padding: 8px;">')
        oil = oil.replace('<tr style="text-align: center;">', '<tr style="text-align: center; background-color: #ffffff; box-shadow: 0px 0px 10px 10px rgba(0,0,0,0.1);">')

        oil_tech_indicator = investing.get_indicator()
        oil_gen_info = cme.get_general_info()
        headlines = investing.get_articles()
        anals = investing.get_analysis()
        oil_headlines = [
        f"""<tr><td align="left"><a href="{out_article['link']}" class="img"><img class=" lazyloaded" style="height:92px; width:120px;   padding-bottom:18px" data-src="{out_article['img']}" alt="" onerror="javascript:this.src='https://i-invdn-com.investing.com/news/news-paper_108x81.png';" src="{out_article['img']}"></a>
        <div class="textDiv"><a href="{out_article['link']}" title={out_article['title']}" class="title">{out_article['title']}</a><span style="line-height:20px;" class="articleDetails"><span style="line-height:20px;"><br>Source: {out_article['source']}</span><span style="line-height:20px;" class="date"><br>Published: {out_article['time']}</span></span>
        <p style="line-height: 16px;">{out_article['by']}<br>{out_article['news_text']}</p>
        </div>
        </td>
        <div class="clear"></div>
        </td></tr>
        """ for out_article in headlines
        ]

        oil_anals= [
        f"""<tr><td align="left"><a href="{out_article['link']}" class="img"><img class=" lazyloaded" style="height:92px; width:120px;   padding-bottom:18px" data-src="{out_article['img']}" alt="" onerror="javascript:this.src='https://i-invdn-com.investing.com/news/news-paper_108x81.png';" src="{out_article['img']}"></a>
        <div class="textDiv"><a href="{out_article['link']}" title={out_article['title']}" class="title">{out_article['title']}</a><span style="line-height:20px;" class="articleDetails"><span style="line-height:20px;"><br>Source: {out_article['source']}</span><span style="line-height:20px;" class="date"><br>Published: {out_article['time']}</span></span>
        <p style="line-height: 16px;">{out_article['by']}<br>{out_article['news_text']}</p>
        </div>
        
        <div class="clear"></div>
        </td></tr>
        """ for out_article in anals
        ]

        string2 = f"""<h2 style="text-align: left; padding-left: 10px;">Posted Prices</h2> <p style="line-height: 20px; padding-bottom:20px; border-bottom:5px ridge rgba(23, 23, 95, 0.411);">{oil}</p><br>
        <h2 style="text-align: left; padding-left: 10px; padding-top:20px; border-top:5px ridge rgba(23, 23, 95, 0.411);">General Info</h2>
        <p style="line-height: 20px; text-align: left; padding-left: 10px; padding-bottom:20px; border-bottom:5px ridge rgba(23, 23, 95, 0.411);">{oil_gen_info}</p>
        <h2 style="text-align: left; padding-left: 10px;">Technical Indicator Summary</h2><p style="line-height: 20px;text-align: left; padding-left: 10px; padding-bottom:20px; border-bottom:5px ridge rgba(23, 23, 95, 0.411);">{oil_tech_indicator}</p>

          <table cellpadding="0" cellspacing="0" width="100%">
        <h2 style="text-align: left; padding-left: 10px;">Top Headlines</h2>          
        <h2 style="text-align: left; padding-left: 10px; padding-top:20px; border-top:2px ridge rgba(23, 23, 95, 0.411);"></h2><article align="center" style=" padding-left:8px; display: table-cell;vertical-align: top;text-align: left;direction: ltr;margin-top:2px;">{oil_headlines[0]}</article><p>&nbsp;</p>
        <h2 style="text-align: left; padding-left: 10px; padding-top:20px; border-top:2px ridge rgba(23, 23, 95, 0.411);"></h2><article align="center" style=" padding-left:8px; display: table-cell;vertical-align: top;text-align: left;direction: ltr;margin-top:2px;">{oil_headlines[1]}</article><p>&nbsp;</p>
        <h2 style="text-align: left; padding-left: 10px; padding-top:20px; border-top:2px ridge rgba(23, 23, 95, 0.411);"></h2><article align="center" style=" padding-left:8px; display: table-cell;vertical-align: top;text-align: left;direction: ltr;margin-top:2px;">{oil_headlines[2]}</article><p>&nbsp;</p>
              
          </table>      
        <p style="line-height: 20px;text-align: left; padding-left: 10px; padding-bottom:20px; border-bottom:5px ridge rgba(23, 23, 95, 0.411);"><br></p>
        <h2 style="text-align: left; padding-left: 10px;">Top Analysis & Opinion</h2><article align="center" style=" padding-left:8px; border-bottom: 2px solid #404040; padding-bottom:10px; display: table-cell;vertical-align: top;text-align: left;direction: ltr;margin-top:2px;">{oil_anals[0]}</article><p>&nbsp;</p><article align="center" style=" width:100%; padding-left:8px; border-bottom: 2px solid #404040; padding-bottom:10px; display: table-cell;vertical-align: top;text-align: left;direction: ltr;margin-top:2px;">{oil_anals[1]}</article><p>&nbsp;</p><article align="center" style=" padding-left:8px; border-bottom: 2px solid #404040; padding-bottom:10px; display: table-cell;vertical-align: top;text-align: left;direction: ltr;margin-top:2px;">{oil_anals[2]}</article>
        """
        with open("HTML/string1.html") as f1, open("HTML/string3.html") as f2:
            string1 = f1.read()
            string3 = f2.read()
            message = string1+string2+string3
            self.message = message.replace("\\","").replace("\n", "").replace("\t", "")
            print("Message Compiled!")
        
        return

    
report = Report()
report.html_email()
from EmailMain import Email 
email = Email()
email.sendmail(report.email, report.password, report.recipients, report.subject, report.message)


