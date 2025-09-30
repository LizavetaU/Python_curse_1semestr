import requests
from bs4 import BeautifulSoup
import pandas as pd

def simple_bestchange():
    """Простая версия для получения курсов с BestChange"""
    
    print("🎯 Загружаем курсы с BestChange...")
    
    # Ссылки на страницы BestChange
    pages = {
        'Bitcoin → RUB': 'https://www.bestchange.ru/bitcoin-to-ruble.html',
        'Solana → RUB': 'https://www.bestchange.ru/solana-to-ruble.html',
        'USDT → RUB': 'https://www.bestchange.ru/tether-trc20-to-ruble.html'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    all_data = []
    
    for direction, url in pages.items():
        print(f"Загружаем {direction}...")
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {'id': 'content_table'})
            
            if table:
                rows = table.find_all('tr')[1:6]  # Берем только первые 5 обменников
                
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        exchange = cols[1].get_text(strip=True)
                        give = cols[2].get_text(strip=True)
                        receive = cols[3].get_text(strip=True)
                        
                        all_data.append({
                            'Направление': direction,
                            'Обменник': exchange,
                            'Отдаете': give,
                            'Получаете': receive
                        })
        except Exception as e:
            print(f"Ошибка для {direction}: {e}")
    
    # Создаем таблицу
    df = pd.DataFrame(all_data)
    
    # Выводим результаты
    print("\n" + "="*60)
    print("КУРСЫ ОБМЕННИКОВ:")
    print("="*60)
    
    for direction in pages.keys():
        print(f"\n{direction}:")
        print("-" * 60)
        direction_data = df[df['Направление'] == direction]
        
        for _, row in direction_data.iterrows():
            print(f"🔹 {row['Обменник']}:")
            print(f"   Отдаете: {row['Отдаете']}")
            print(f"   Получаете: {row['Получаете']}")
            print()
    
    return df

# Запускаем программу
df = simple_bestchange()
