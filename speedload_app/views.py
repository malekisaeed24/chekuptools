from bs4 import BeautifulSoup
from urllib.parse import urljoin
from django.http import JsonResponse
from django.shortcuts import render
from asgiref.sync import async_to_sync
from .models import Slider, Section, Sidebar
import requests
import whois
import asyncio
import aiohttp
import time

# --- Speed Test Functions ---

async def fetch_resource(session, url):
    try:
        start_time = time.time()
        async with session.get(url) as response:
            content = await response.read()
            end_time = time.time()
            return content, response.content_type, end_time - start_time
    except Exception as e:
        return None, None, 0

async def get_resource_size_and_time(url):
    async with aiohttp.ClientSession() as session:
        html_content, html_type, html_time = await fetch_resource(session, url)
        if not html_content:
            return {'error': 'خطا در پردازش URL'}

        html_size = len(html_content)
        soup = BeautifulSoup(html_content, 'html.parser')

        tasks = []
        for css in soup.find_all('link', rel='stylesheet'):
            css_url = urljoin(url, css.get('href'))
            tasks.append(fetch_resource(session, css_url))
        for js in soup.find_all('script', src=True):
            js_url = urljoin(url, js.get('src'))
            tasks.append(fetch_resource(session, js_url))
        for img in soup.find_all('img'):
            img_url = urljoin(url, img.get('src'))
            tasks.append(fetch_resource(session, img_url))

        resources = await asyncio.gather(*tasks)
        css_time, js_time, img_time = 0, 0, 0
        css_size, js_size, img_size = 0, 0, 0

        for resource, resource_type, resource_time in resources:
            if resource:
                if 'css' in resource_type:
                    css_time += resource_time
                    css_size += len(resource)
                elif 'javascript' in resource_type:
                    js_time += resource_time
                    js_size += len(resource)
                elif 'image' in resource_type:
                    img_time += resource_time
                    img_size += len(resource)

        total_time = html_time + css_time + js_time + img_time

        return {
            'html': {'time': html_time, 'size': html_size},
            'css': {'time': css_time, 'size': css_size},
            'js': {'time': js_time, 'size': js_size},
            'img': {'time': img_time, 'size': img_size},
            'total_time': total_time
        }

def speed_test(request):
    if request.method == 'POST':
        url = request.POST.get('url')

        if not url:
            return JsonResponse({'error': 'لطفا آدرس سایت را وارد کنید'})

        if not url.startswith('http'):
            url = 'http://' + url

        try:
            results = async_to_sync(get_resource_size_and_time)(url)
            return JsonResponse(results)
        except Exception as e:
            return JsonResponse({'error': 'خطا در پردازش URL', 'details': str(e)})

    return render(request, 'speedload_app/speed_test.html')


# --- SEO Analysis View ---

def analyze_seo(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url.startswith('http'):
            url = 'http://' + url

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # استخراج عنوان سایت
            title_tag = soup.find('title')
            title_text = title_tag.text if title_tag else 'عنوانی یافت نشد'
            title_length = len(title_text)
            title_words = len(title_text.split())

            # توضیحات متا و طول آن
            meta_description = soup.find('meta', attrs={'name': 'description'})
            meta_description_content = meta_description['content'] if meta_description else "بدون توضیحات"
            meta_description_length = len(meta_description_content)

            # پیام بهینه‌سازی توضیحات متا
            optimal_meta_message = (
                "طول توضیحات متا باید بین 50 تا 160 کاراکتر باشد تا بهینه باشد."
                if not (50 <= meta_description_length <= 160)
                else "طول توضیحات متا مناسب است."
            )

            # تعداد کلمات کلیدی
            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            keywords = meta_keywords['content'].split(',') if meta_keywords else []
            keyword_count = len(keywords)

            # ثبات کلمه کلیدی
            body_text = soup.get_text()
            keyword_consistency = sum(body_text.count(keyword) for keyword in keywords)

            # نسبت کد به متن
            html_content = response.content
            text_length = len(body_text)
            html_length = len(html_content)
            text_html_ratio = (text_length / html_length) * 100 if html_length > 0 else 0

            # وضعیت GZIP
            gzip_enabled = 'Content-Encoding' in response.headers

            # بررسی ریدایرکت WWW
            redirected_url = response.url
            is_www_redirected = 'www.' in redirected_url

            # بررسی ریدایرکت آیپی
            ip_address = requests.get('https://api.ipify.org').text
            ip_redirected = ip_address in redirected_url

            # وضعیت لینک ها
            in_page_links = [link['href'] for link in soup.find_all('a', href=True)]
            in_page_links_count = len(in_page_links)

            # بررسی XML Sitemap
            sitemap_url = urljoin(url, '/sitemap.xml')
            sitemap_exists = requests.head(sitemap_url).status_code == 200

            # فایل robots.txt
            robots_txt_url = urljoin(url, '/robots.txt')
            robots_exists = requests.head(robots_txt_url).status_code == 200

            # بررسی آندراسکور در لینک
            underscores_in_urls = sum(1 for link in in_page_links if '_' in link)

            # وضعیت دامنه
            domain_info = whois.whois(url)
            domain_status = 'فعال' if domain_info else 'غیر فعال'

            # اطلاعات ثبت کننده
            registrar_info = domain_info.registrar if domain_info else 'اطلاعات ثبت کننده موجود نیست'

            # موبایل دوستانه
            viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
            mobile_friendly = viewport_meta is not None

            # حجم صفحه
            page_size = len(response.content)

            # بررسی فاو آیکن
            favicon_exists = soup.find('link', rel='icon') is not None

            # بررسی صفحه 404 سفارشی
            custom_404_exists = requests.head(urljoin(url, '/404'))  # فرض می‌کنیم که آدرس صفحه 404 این‌گونه است
            custom_404_status = custom_404_exists.status_code == 200

            # بررسی تعداد تصاویر و آدرس تصاویر بدون alt
            images = soup.find_all('img')
            total_images = len(images)
            images_without_alt = [img['src'] for img in images if not img.get('alt')]

            # صفحات ایندکس شده (مثال)
            indexed_pages = "در حال بررسی"  # این مورد نیاز به روش خاصی دارد که می‌توانید توسعه دهید.

            # کشور بازدیدکنندگان (مثال)
            visitors_localization = "در حال بررسی"  # این مورد نیز نیاز به روش خاصی دارد.

            return JsonResponse({
                'title_text': title_text,
                'title_length': title_length,
                'title_words': title_words,
                'meta_description_content': meta_description_content,
                'meta_description_length': meta_description_length,
                'optimal_meta_message': optimal_meta_message,
                'keyword_count': keyword_count,
                'keyword_consistency': keyword_consistency,
                'text_html_ratio': text_html_ratio,
                'gzip_enabled': gzip_enabled,
                'is_www_redirected': is_www_redirected,
                'ip_redirected': ip_redirected,
                'in_page_links_count': in_page_links_count,
                'sitemap_exists': sitemap_exists,
                'robots_exists': robots_exists,
                'underscores_in_urls': underscores_in_urls,
                'domain_status': domain_status,
                'registrar_info': registrar_info,
                'mobile_friendly': mobile_friendly,
                'page_size': page_size,
                'favicon_exists': favicon_exists,
                'custom_404_status': custom_404_status,
                'total_images': total_images,
                'images_without_alt_count': len(images_without_alt),  # تعداد تصاویر بدون alt
                'images_without_alt': images_without_alt,
                'indexed_pages': indexed_pages,
                'visitors_localization': visitors_localization,
            })

        except requests.RequestException:
            return JsonResponse({'error': 'خطا در دسترسی به آدرس وارد شده.'})

    return render(request, 'speedload_app/analyze_seo.html')

# --- Homepage View ---

def home(request):
    sliders = Slider.objects.all().order_by('order')  # دریافت اسلایدرها
    sections = Section.objects.all().order_by('order')  # دریافت سکشن‌ها
    sidebars = Sidebar.objects.all()  # دریافت سایدبارها
    context = {
        'sliders': sliders,
        'sections': sections,
        'sidebars': sidebars
    }
    return render(request, 'speedload_app/home.html', context)
