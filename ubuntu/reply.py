import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup ChromeDriver dengan opsi
options = Options()
options.add_argument('--headless')  # Menjalankan Chrome di background
options.add_argument('--no-sandbox')  # Untuk menghindari masalah dengan sandboxing
options.add_argument('--disable-dev-shm-usage')  # Untuk menghindari masalah dengan memory sharing

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return len([line for line in file if line.strip() != ''])
    except Exception as e:
        print(f"🚨 Gagal membaca file: {e}")
        return 0

# Daftar emoji acak
emojis = [
    '🎉', '🚀', '💫', '🔥', '🤩', '🌟', '💥', '🥳', '🎈', '👑',
    '🚀', '🥂', '🎁', '👏', '🙌', '✨', '🕺', '💃', '🎊', '🍾',
    '🧡', '💜', '💙', '💚', '❤️', '🖤', '🤍', '🤎', '💛', '🤩'
]

# Fungsi delay sederhana
def delay(time_ms):
    time.sleep(time_ms / 1000.0)

# Fungsi untuk memilih emoji acak
def get_random_emoji():
    return random.choice(emojis)

def main():
    print('🚀 Memulai proses!')

    driver.set_window_size(375, 667)  # Ukuran viewport ponsel
    print('📏 Ukuran viewport diatur.')

    try:
        # Memuat cookies
        with open('./cookies1.json', 'r', encoding='utf-8') as file:
            cookies = json.load(file)
        driver.get('https://x.com/')  # Masukkan URL awal untuk memuat cookies
        for cookie in cookies:
            driver.add_cookie(cookie)
        print('🍪 Cookies telah dimuat.')

        driver.refresh()  # Refresh untuk menerapkan cookies
        delay(2000)  # Delay ekstra

        url = 'https://x.com/triindonesia/status/1817906586414878989'
        driver.get(url)
        print('🔄 Memuat halaman...')
        time.sleep(10)  # Delay standar

        url_id = url.split('/')[-1]  # Ambil ID dari URL
        log_file_path = f'{url_id}.txt'
        n = 300  # Jumlah iterasi

        for i in range(n):
            print('⏲️ Menunggu sebelum posting...')
            delay(2000)

            print('📝 Menyiapkan untuk menulis komentar...')
            # Hitung jumlah baris dalam file log
            line_count_before = count_lines_in_file(log_file_path)
            random_emoji = get_random_emoji()
            comment = (f'Beli Kuota Harga Hemat Gak Pake Kompromi \n'
                       '#IniWaktunyaKita\n'
                       '#UntungPakaiTri #GakPakeKompromi\n'
                       'Bismillah semoga Menang \n'
                       f'~{line_count_before}')

            # Tampilkan jumlah baris dalam komentar
            print(f'💬 Mengirim komentar: "{comment}"')

            delay(2000)
            text_area = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')
            text_area.click()
            text_area.send_keys(comment)
            delay(2000)
            tweet_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="tweetButtonInline"]')
            tweet_button.click()
            print('✅ Komentar berhasil dikirim!')

            # Menunggu pesan konfirmasi dan mengambil ID Tweet
            print('🔄 Menunggu pesan konfirmasi...')
            try:
                # Tunggu hingga elemen konfirmasi muncul
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="alert"] a'))
                )
                
                # Cari elemen link "Lihat"
                tweet_link_element = driver.find_element(By.CSS_SELECTOR, 'div[role="alert"] a')
                tweet_url = tweet_link_element.get_attribute('href')
                tweet_id = tweet_url.split('/')[-1]
                if tweet_id:
                    with open(log_file_path, 'a', encoding='utf-8') as file:
                        file.write(tweet_id + '\n')
                    print(f'📑 Target ID {tweet_id} disimpan di {log_file_path}')

                    # Hitung jumlah baris dalam file setelah posting
                    line_count_after = count_lines_in_file(log_file_path)
                    print(f"🆔 Tweet ID: {tweet_id}")
                    print(f'📄 Jumlah baris setelah posting: {line_count_after}')

            except Exception as e:
                print(f"🚨 Timeout atau kesalahan saat menunggu pesan konfirmasi: {e}")

            # Delay acak antar iterasi
            iteration_delay = random.randint(5000, 10000) / 1000.0  # 5 - 10 detik
            print(f'⏳ Menunggu {iteration_delay} detik sebelum iterasi berikutnya...')
            delay(iteration_delay)
 
    except Exception as e:
        print(f"🚨 Gagal memuat halaman: {e}")

    print('🎉 Selesai.')
    driver.quit()

    # Menampilkan informasi pembuat kode
    print('==============================')
    print('   Kode ini dibuat oleh ngatmuri   ')
    print('==============================')

if __name__ == "__main__":
    main()

