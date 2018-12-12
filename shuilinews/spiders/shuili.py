import scrapy
import string
from urllib.parse import unquote,quote;
from ..items import ShuilinewsItem
class ShuiliSpider(scrapy.Spider):
    name='shuili'
    news_url1='https://www.gzssltzinc.com/yaowen.php?fl=%BC%AF%CD%C5%D2%AA%CE%C5' # 集团要闻
    news_url2='https://www.gzssltzinc.com/toutiaolist.php?fl=%CD%B7%CC%F5%BB%D8%B9%CB' # 头条回顾
    news_url3='https://www.gzssltzinc.com/new.php?fl=%C3%BD%CC%E5%BE%DB%BD%B9'   # 媒体聚焦
    news_url4='https://www.gzssltzinc.com/new.php?fl=%BB%F9%B2%E3%D0%C5%CF%A2'   # 基层信息
    news_url5='https://www.gzssltzinc.com/new.php?fl=%D0%D0%D2%B5%D7%CA%D1%B6'   # 行业资讯
    news_url6='https://www.gzssltzinc.com/new.php?fl=%CA%B1%D5%FE%D2%AA%CE%C5'   # 时政要闻
    news_url7='https://www.gzssltzinc.com/new.php?fl=%D6%B0%B9%A4%B7%E7%B2%C9'   # 职工风采
    news_url8='https://www.gzssltzinc.com/new.php?fl=%B4%F3%CA%C2%BC%C7'   # 大事记
    start_urls=[news_url2,news_url3]
    host_name = 'https://www.gzssltzinc.com/{}'

    def parse(self, response):
        print(response)
        zf = ShuilinewsItem()

        type= response.xpath("//h3[@class='fl']/text()").extract()   #extract(),序列化该节点为unicode字符串并返回list。
        title_list = response.xpath("//ul[@class='textcontent subpagelist']//li//a/text()").extract()
        url_list = response.xpath("//ul[@class='textcontent subpagelist']//li//a/@href").extract()
        news_date_list = response.xpath("//ul[@class='textcontent subpagelist']//li//div/text()").extract()
        print(title_list,url_list,news_date_list,'3333')
        for b, c, d in zip(title_list, url_list,news_date_list):
            zf['type'] = "".join(type)
            zf['title'] = b
            url1 = 'https://www.gzssltzinc.com/' + "".join(c)
            urlall = quote(url1, safe=string.printable, encoding='gbk')  # 中文转换为url
            zf['url'] = urlall
            zf['news_date'] = d
            yield zf


        # 查找下一页并执行上面
        next_pages = response.xpath(".//div[@class='page']//a[contains(text(),'下一页')]/@href").extract()

        if len(next_pages) > 0:
            next_page = self.host_name.format(next_pages[0])
            next_pages1 = quote(next_page, safe=string.printable, encoding='gbk')
            print(next_pages1, '$$$$$' * 10)
            yield scrapy.Request(next_pages1, callback=self.parse)  # 丢回调度器并指定回调函数parse不用括号
            # yield ：生成器，和return类似，但是不会停止函数执行。优点：节约内存
        else:
            pass