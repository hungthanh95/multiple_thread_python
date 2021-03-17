# main.py - Downloads XKCD comics using multiple threads.

import requests, os, bs4, threading

os.makedirs('xkcd', exist_ok=True)  # store comics in ./xkcd


def download_xkcd(start_comic, end_comic):
    for url_number in range(start_comic, end_comic):
        # Download the page.
        print('Downloading page http://xkcd.com/%s...' % url_number)
        res = requests.get('http://xkcd.com/%s' % url_number)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text)

        # Find the URL of the comic image.
        comic_elem = soup.select('#comic img')
        if not comic_elem:
            print('Could not find comic image.')
        else:
            comic_url = comic_elem[0].get('src')

        # Download the image.
        print('Downloading image %s...' % comic_url)
        res = requests.get('http:' + comic_url)
        res.raise_for_status()
        # Save the image to ./xkcd.
        with open(os.path.join('xkcd', os.path.basename(comic_url)), 'wb') as image_file:
            for chunk in res.iter_content(100000):
                image_file.write(chunk)


# Create and start the Thread objects.
download_threads = []  # a list of all the threads obj
for i in range(1, 1400, 100):    # loop 14 times, creates 14 threads
    download_thread = threading.Thread(target=download_xkcd, args=(i, i + 99))
    download_threads.append(download_thread)
    download_thread.start()

# Wait for all threads to end.
for download_thread in download_threads:
    download_thread.join()
print('Done.')