from django.shortcuts import render, redirect
import json 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common import exceptions  
import re
from books.models import BooksDetail, BooksModel
from django.http import HttpResponse


# Create your views here.
def scrapper(request):
    browser = None

    try:
        browser = webdriver.Chrome()
    except Exception as error:
        print(error)



    # Here we scrap the links of every single book 
    category_links = open('start_links.txt','r',encoding='utf-8')
    out_file = open('book_links.json','w+' , encoding='utf-8')
    product_links = list()

    next_button_Xpath = '//*[@id="my-store-741189"]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div/div[3]/div[2]/a[2]/span[1]'

    for link in category_links :
        print('Working on :' ,link.split('/')[-1][:-4])
        try:
                    browser.get(link)
                    

        except Exception as err:
                    print(str(err))
                    break
        else:
                    print('Successfully Accessed:',link)
                    print('Please be patient it may take several minutes .....')


        while True :
            time.sleep(20)
            try :
                
                element = browser.find_element_by_xpath(next_button_Xpath)
            except NoSuchElementException:
                

                #div_tags = soup.find_all('div', attrs={"class":"grid-product__wrap-inner"})
                div_tags = browser.find_elements_by_xpath('//div[@class="grid-product__wrap-inner"]')
                for tag in div_tags :
                    #anchor = tag.findChild('a',attrs={'class':'grid-product__title'})
                    anchor = tag.find_element_by_tag_name("a")
                    product_links.append(anchor.get_attribute("href"))
                        
                break 
            
            element = WebDriverWait(browser, 120 ,ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,))\
                            .until(expected_conditions.presence_of_element_located((By.XPATH, next_button_Xpath)))
            try :
                if element.is_displayed() :
                    

                    div_tags = browser.find_elements_by_xpath('//div[@class="grid-product__wrap-inner"]')
                    
                    for tag in div_tags :
                        anchor = tag.find_element_by_tag_name("a")
                        product_links.append( anchor.get_attribute("href"))
                            
                    browser.execute_script("arguments[0].click();", element)
                    time.sleep(5)
                else :
                    time.sleep(5)

                    div_tags = browser.find_elements_by_xpath('//div[@class="grid-product__wrap-inner"]')
                    
                    for tag in div_tags :
                        anchor = tag.find_element_by_tag_name("a")
                        product_links.append( anchor.get_attribute("href"))
                        
                    break 

            except exceptions.StaleElementReferenceException:  
                pass
        
        print('writing links to file .... ')
        out_file.seek(0)
        out_file.truncate()
        json.dump({'links':list(set(product_links))},out_file)
        print('File successfully updated.....')
        


    out_file.close()
    print('All data saved successfully !!')

    # Here we scrap book details

    links = json.loads(open('book_links.json', 'r' , encoding='utf-8').read())["links"]
    out_file = open('book_Data.json','w+' , encoding='utf-8')
    book_data = dict()

    for link in links :
        
        try:
                    browser.get(link)
                    time.sleep(15)
                    # html_text = browser.page_source

        except Exception as err:
                    print(str(err))
                    break
        else:
                    print('Successfully Accessed:',link)
        time.sleep(10)


        # book_name = soup.find('h1', attrs={'class':'product-details__product-title'})
        try :    
            book_name = browser.find_element_by_xpath('//h1[@class="product-details__product-title"]')
            book_data[book_name.text] = dict()
        except NoSuchElementException :
            pass
        #book_price = soup.find('span',attrs={'class':'details-product-price__value notranslate'})
        try :
            book_price = browser.find_element_by_xpath('//span[@class="details-product-price__value notranslate"]')
            book_data[book_name.text]['Price'] = book_price.text
        except NoSuchElementException :
            pass
        # book_description = soup.find('div',attrs={'id':'productDescription'})
        try:
            book_description = browser.find_element_by_xpath('//div[@id="productDescription"]')
            description_cleaned   = book_description.find_element_by_tag_name("div").text.replace('Available for Rent or Used, Second Hand at Best Prices on  www.pustakkosh.com','')
            book_data[book_name.text]['Decription'] = description_cleaned  
        except NoSuchElementException :
            pass
        
        #img_div = soup.find('div',attrs={'class':'details-gallery__image-wrapper-inner'})
        try :
            img_div = browser.find_element_by_xpath('//div[@class="details-gallery__image-wrapper-inner"]')
            book_data[book_name.text]['Image_URL'] = img_div.find_element_by_tag_name('img').get_attribute("src")
        except NoSuchElementException :
            pass
        print('writing data to file .... ')
        out_file.seek(0)
        out_file.truncate()
        json.dump(book_data,out_file)
        print('File successfully updated.....')    
        
    out_file.seek(0)
    out_file.truncate()
    json.dump(book_data,out_file)
    
    import pdb;pdb.set_trace()
    # Create a Django model object for each object in the JSON 
    for data in book_data:
        
        try:
                        
            book = BooksDetail()
            try:
                book.name = data
            except:
                pass

            try:
                book.mrp = book_data[data]['Price']
            except:
                pass

            try:
                book.description = book_data[data]['Decription']

                if not data:
                    book.name = book_data[data]['Decription']

            except:
                book.description = ""

            try:
                book.image = book_data[data]['Image_URL']
            except:
                book.image = None

            book.save()
            print('successfully saved')
        except:
            pass
    

    out_file.close()
    print('All Data saved successfully ....!!')
    browser.close()

    return redirect('/')

def scrapper2(request):
    # We take control of browser here 
    browser = None

    try:
        browser = webdriver.Chrome()
    except Exception as error:
        print(error)    

    # Here we scrap product links from thier respective categories 

    category_links = open('kick_start_categories.txt','r',encoding='utf-8')
    out_file = open('indiabookstore_book_links.json','w+' , encoding='utf-8')
    product_links = list()

    next_btn_Xpath = '//li[@class="arrow"][contains(text(),"Next »")]'
    book_links_Xpath = '//div[@class="col-md-3 col-xs-6 text-center "]//child::a[@class="bookPageLink"]'

    for link in category_links :
        print('Working on :' ,link.split('/')[-1])
        try:
                    browser.get(link)
                    

        except Exception as err:
                    print(str(err))
                    break
        else:
                    print('Successfully Accessed:',link)
                    print('Please be patient it may take several minutes .....')
        while True :
            try :
                element = browser.find_element_by_xpath(next_btn_Xpath)
            except NoSuchElementException:
                time.sleep(1)
                
                anchor_tags = browser.find_elements_by_xpath(book_links_Xpath) 
                
                    
                for tag in anchor_tags :
                    product_links.append(tag.get_attribute("href"))
                        
                break 
            time.sleep(1)
            element = WebDriverWait(browser, 120 ,ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,))\
                            .until(expected_conditions.presence_of_element_located((By.XPATH, next_btn_Xpath)))
            try :
                if element.is_displayed() :
                    time.sleep(1)
                    anchor_tags = browser.find_elements_by_xpath(book_links_Xpath) 
                    
                    
                    for tag in anchor_tags :
                        product_links.append(tag.get_attribute("href"))
                    
                    browser.execute_script("arguments[0].click();", element)
                    time.sleep(1)
                else :
                    time.sleep(1)
                    anchor_tags = browser.find_elements_by_xpath(book_links_Xpath) 
                
                    
                    for tag in anchor_tags :
                        product_links.append(tag.get_attribute("href"))
                    
                    break 

            except exceptions.StaleElementReferenceException:  
                pass
        
        print('writing links to file .... ')
        out_file.seek(0)
        out_file.truncate()
        json.dump({'links':list(set(product_links))},out_file)
        print('File successfully updated.....')



    out_file.close()
    print('All data saved successfully !!')


    # Here we scrape book data 

    print('Getting book data now .....')
    links = json.loads(open('indiabookstore_book_links.json','r' , encoding='utf-8').read())['links']
    out_file =  open('indiabookstore_data.json','w+' , encoding='utf-8')

    book_data = dict()
    for link in links :

        try:
                    browser.get(link)
                    

        except Exception as err:
                    print(str(err))
                    break
        else:
                    print('Successfully Accessed:',link)
                    

        try : 
            book_name = re.sub('\s+', '' , browser.find_element_by_xpath('//h1[@class="bookMainTitle"]').text )
            book_data[book_name] = dict()
            book_data[book_name]['ISBN-13'] = link.split('/')[-1]
        except :
            pass 
        try :
            Author = browser.find_element_by_xpath('//div[@itemprop="author"]').text.split(':')[1]
            book_data[book_name]['Author'] = Author
        except :
            pass
        try:
            Publisher = browser.find_element_by_xpath('//div[@itemprop="author"]//following-sibling::div').text.split(':')[1]
            book_data[book_name]['Publisher'] = Publisher
        except :
            pass
        try :
            rating = re.findall("\d+\.\d+", browser.find_element_by_xpath('//div[@itemprop="ratingValue"]').text)[0]
            book_data[book_name]['Rating'] = rating
        except :
            pass 
        try :
            isbn_10 = browser.find_element_by_xpath('//div[@class="table-responsive"]//child::td[contains(text(),"ISBN-10")]//following-sibling::td[@itemprop="isbn"]').text
            book_data[book_name]['ISBN-10'] = isbn_10
        except :
            pass 
        try :
            number_of_pages = browser.find_element_by_xpath('//div[@class="table-responsive"]//child::td[contains(text(),"Number of pages")]//following-sibling::td[@itemprop="numberOfPages"]').text.split()[0]
            book_data[book_name]['Number of pages'] = number_of_pages
        except:
            pass 
        try :
            language = browser.find_element_by_xpath('//div[@class="table-responsive"]//child::td[contains(text(),"Language")]//following-sibling::td[@itemprop="inLanguage"]').text
            book_data[book_name]['Language'] = language
        except :
            pass 
        try :
            edition = browser.find_element_by_xpath('//div[@class="table-responsive"]//child::td[contains(text(),"Edition")]//following-sibling::td').text
            book_data[book_name]['Edition'] = edition
        except :
            pass
        try :
            dimensions = browser.find_element_by_xpath('//div[@class="table-responsive"]//child::td[contains(text(),"Dimension")]//following-sibling::td').text
            book_data[book_name]['Dimensions'] = re.sub('\s+', '' , dimensions )
        except :
            pass 
        try :
            description = browser.find_element_by_xpath('//span[@itemprop="description"]').text
            book_data[book_name]['Book Description'] = description
        except :
            pass 
        try :
            image_URL = browser.find_element_by_xpath('//img[@class="bookMainImage"]').get_attribute('src')
            book_data[book_name]['Image_URL'] = image_URL 
        except :
            pass 
        try :
            prices = list()
            price_tags = browser.find_elements_by_xpath('//div[@class="card"]//child::a')[:-1]
            for price_tag in price_tags :
                text_data = price_tag.get_attribute('textContent')
                if '@' in text_data : prices.append(text_data)
            book_data[book_name]['Prices'] = prices
        except :
            pass
        print('Writing to file')
        out_file.seek(0)
        out_file.truncate()
        json.dump(book_data,out_file)
        print('File successfully updated.....')

    out_file.seek(0)
    out_file.truncate()
    json.dump(book_data,out_file)

    import pdb;pdb.set_trace()
    # Create a Django model object for each object in the JSON 
    for data in book_data:
        
        try:
                        
            book = BooksModel()
            try:
                book.Name = data
            except:
                pass

            try:
                book.ISBN_13 = book_data[data]['ISBN-13']
            except:
                pass

            try:
                book.Author = book_data[data]['Author']

                # if not data:
                #     book.name = book_data[data]['Decription']

            except:
                book.description = ""

            try:
                book.Publisher = book_data[data]['Publisher']
            except:
                book.Publisher = None

            try:
                book.Rating = book_data[data]['Rating']
            except:
                pass

            try:
                book.ISBN_10 = book_data[data]['ISBN-10']
            except:
                pass

            try:
                book.Number_of_pages = book_data[data]['Number of pages']
            except:
                pass

            try:
                book.Language = book_data[data]['Language']
            except:
                pass

            try:
                book.Edition = book_data[data]['Edition']
            except:
                pass

            try:
                book.Dimensions = book_data[data]['Dimensions']
            except:
                pass

            try:
                book.Book_Description = book_data[data]['Book Description']
            except:
                pass

            try:
                book.Image_URL = book_data[data]['Image_URL']
            except:
                book.Image_URL = None

            try:
                book.Prices = book_data[data]['Prices']
            except:
                pass

            book.save()
            print('successfully saved')
        except:
            pass

    print('All data scrapped Successfullly !!!')
    out_file.close()
    browser.close()
    
    return redirect('/')
