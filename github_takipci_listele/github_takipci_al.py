# Bir github hesabına otomatik giriş yapıp o hesabın takipçi listesini alan program.
# kullanıcı adı ve şifreyi github_user_info.py dosyasından alıyoruz.
# Girmek istediğiniz hesabın kullanıcı adı ve şifresini oradan değiştirip deneyebilirsiniz.
# chromedriver.exe dosyasını python sitesinde selenium drivers olarak aratarak
# indirip programı çalıştırınız.

from selenium import webdriver
from github_user_info import username,password
from selenium.webdriver.common.keys import Keys
import time
class Github():
    def __init__(self,username,password):
        self.browser=webdriver.Chrome()
        self.username=username
        self.password=password
        self.followers=[]
    
    
    def dosyayaAl(self):
         file=open("followers.txt",'a',encoding="utf-8")
         for i in self.followers:
             file.write(i)
          
  
    
    def signIn(self):
        self.browser.get("https://github.com/login")
        time.sleep(2)
        self.browser.find_element_by_name("login").send_keys(self.username) # kullanıcı adı textbox ına kullanıcıadını girdik.
        self.browser.find_element_by_name("password").send_keys(self.password) # şifre textbox ına şifryi girdik
        self.browser.find_element_by_name("commit").click() # giriş yap butonuna bas dedik.
    
    
    def loadFollower(self):
         items=self.browser.find_elements_by_css_selector(".d-table.table-fixed")
         for i in items:
          self.followers.append(i.find_element_by_css_selector(".f4.Link--primary").text)

   
    def getFollower(self):
        self.browser.get(f"https://github.com/{self.username}?tab=followers")
        time.sleep(2)
        
        if len(self.followers)<=50: # 1 sayfaya sadece 50 takipçi geliyor, 50 takipçinin altında olan hesaplar için next ve prev linkleri olamayacağı için bu şekilde baştan bi kontrol sağladım.
            self.loadFollower()
        else:
             while True:
              links=self.browser.find_element_by_class_name("BtnGroup").find_element_by_tag_name("a")   
              if len(links)==1: # eğer linklerde sadece 1 adet varsa ya son sayfadayız prev linki var ya da ilk sayfadayız sadece next linki var.
               if links[0].text=="Next": # burada linkin textini kontrol ederek işlemler yapıyoruz.
                links[0].click()
                time.sleep(1)
                self.loadFollower()
               else:
                break # tek link prev ise demek ki son sayfadayız ve artık followersları alacağımız sayfa yok demek bu yüzden döngüden çıkıyoruz.        
              else: # şimdi de 2 adet linkin olduğu durumu kontrol edeceğiz.
                 for link in links:
                  if link.text=="Next":
                     link.click()
                     time.sleep(1)
                     self.loadFollower()
                 else:
                     continue # 2 adet linki kontrol ettiğimiz döngüde prev gelmişse devam et diyerek döngüye tekrar giriyoruz ve next i buluyoruz.
   
    
       
    



# Github sınıfından nesne oluşturup signIn methodunu kullanarak hesaba giriş yapıcaz.
github=Github(username,password)
github.signIn()
github.getFollower()
github.dosyayaAl()



