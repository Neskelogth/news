from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import time


class newsGetter:

    def __init__(self):
        self.driver = webdriver.Firefox()

    def remove_element_by_id(self, id):

        self.driver.execute_script("""
            let element = document.getElementById(arguments[0]);
            if (typeof element !== 'undefined'){
            
                element.parentNode.removeChild(element);
            }    
        """, id)

    def remove_element_by_class_name(self, class_name, idx=-1):
        self.driver.execute_script("""
                    let element;
                    let elements;
                    elements = document.getElementsByClassName(arguments[0]);
                    
                    if(arguments[1] != -1){
                        
                        element = elements[arguments[1]]
                        if (typeof element !== 'undefined'){
                            element.parentNode.removeChild(element);
                        }
                    }
                    
                    if (typeof elements !== 'undefined'){
                        
                        Array.prototype.slice.call(elements).forEach((item) => {
                            item.parentNode.removeChild(item);
                        })
                    }    
                """, class_name, idx)

    def remove_class(self, element_name, class_to_remove, idx=0):
        self.driver.execute_script("""
                            
                            let element = document.getElementsByTagName(arguments[0])[arguments[2]];
                            element.classList.remove(arguments[1])
                        """, element_name, class_to_remove, idx)

    def get_qdp_news(self, link, categories):

        base_link = link + '/category/'
        final_output = ''
        for cat in categories:
            new_link = base_link + cat
            final_output += '## ' + cat.replace('-', ' ').capitalize()
            final_output += ' \n\n'
            self.driver.get(new_link)
            self.remove_element_by_class_name('advads-background', 0)
            self.remove_element_by_id('cmplz-cookiebanner-container')

            elements = self.driver.find_elements(By.TAG_NAME, 'h2')

            for el in elements:
                link = el.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
                final_output += '[' + el.text + '](' + link + ')\n\n'

            final_output += '\n'

        return final_output

    # very ugly but for some reason i have to wait inside the loop because the site won't load correctly I suppose
    def get_gazzettino_news(self, link):

        final_ouput = ''
        self.driver.get(link)
        self.remove_element_by_class_name('iubenda-cs-close-btn', 0)
        articles = self.driver.find_elements(By.CLASS_NAME, 'item_content')

        for article in articles:
            elements = article.find_elements(By.TAG_NAME, 'h2')
            time.sleep(0.2)
            if len(elements) > 0:
                element = elements[0]
                news_link = element.find_elements(By.TAG_NAME, 'a')
                time.sleep(0.2)
                if len(news_link) > 0:
                    news_link = news_link[0]
                    href = news_link.get_attribute('href')
                    final_ouput += '[' + news_link.text + '](' + href + ')\n\n'

        return final_ouput

    def get_corriere_news(self, link):

        final_output = ''
        self.driver.get(link)
        self.remove_element_by_class_name('privacy-cp-wall', 0)
        self.remove_element_by_class_name('info')
        return final_output

    def get(self, sites, qdp_categories):
        out = ''
        for key in sites:
            value = sites[key]
            if key == 'qdp':
                print('Getting QDP')
                out += '# QDP News\n\n'
                out += self.get_qdp_news(value, qdp_categories)
                out += '-' * 70
                out += '\n'
            if key == 'gazzettino':
                print('Getting Gazzettino')
                out += '# Gazzettino\n\n'
                # out += self.get_gazzettino_news(value)
                out += '-' * 70
                out += '\n'
            if key == 'corriere della sera':
                print('Getting Corriere della sera')
                out += '# Corriere della sera\n\n'
                out += self.get_corriere_news(value)
                out += '-' * 70
                out += '\n'
        return out

    def __del__(self):
        self.driver.close()
