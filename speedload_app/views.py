import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from django.http import JsonResponse
from django.shortcuts import render

async def fetch_resource(session, url):
    try:
        start_time = time.time()  # ثبت زمان شروع
        async with session.get(url) as response:
            content = await response.read()
            end_time = time.time()  # ثبت زمان پایان
            return content, response.content_type, end_time - start_time  # محاسبه زمان بارگذاری
    except Exception as e:
        return None, None, 0  # در صورت بروز خطا

async def get_resource_size_and_time(url):
    async with aiohttp.ClientSession() as session:
        # زمان بارگذاری HTML
        html_start = time.time()
        html_content, html_type, html_time = await fetch_resource(session, url)
        if not html_content:
            return {'error': 'خطا در پردازش URL'}

        html_size = len(html_content)
        soup = BeautifulSoup(html_content, 'html.parser')

        # تبدیل لینک‌های نسبی به لینک‌های کامل
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

        # محاسبه زمان و اندازه کل CSS، JS و تصاویر
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

        # محاسبه زمان کلی
        total_time = html_time + css_time + js_time + img_time

        return {
            'html': {'time': html_time, 'size': html_size},
            'css': {'time': css_time, 'size': css_size},
            'js': {'time': js_time, 'size': js_size},
            'img': {'time': img_time, 'size': img_size},
            'total_time': total_time  # زمان کلی بارگذاری
        }

def speed_test(request):
    if request.method == 'POST':
        url = request.POST.get('url')

        if not url:
            return JsonResponse({'error': 'لطفا آدرس سایت را وارد کنید'})

        if not url.startswith('http'):
            url = 'http://' + url

        try:
            results = asyncio.run(get_resource_size_and_time(url))
            return JsonResponse(results)
        except Exception as e:
            return JsonResponse({'error': 'خطا در پردازش URL', 'details': str(e)})

    return render(request, 'speedload_app/speed_test.html')
