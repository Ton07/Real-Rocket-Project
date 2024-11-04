
from nicegui import ui
import sqlite3
#สีพื้นหลัง
ui.add_head_html('<style>body{background:linear-gradient(to right,#591c53,#ff1f76); height: 100vh; margin: 0;}</style>')
#เมนูในแถบ
#search_results_container = ui.container()

# สร้างรายการของเกมที่เพิ่มลงในตะกร้าสินค้า
cart_items = []
games = [
    {"name": "PUBG", "price": "FREE", "image": "path/to/pubg_image.jpg"},
    {"name": "APEX LEGENDS", "price": "FREE", "image": "path/to/apex_image.jpg"},
    {"name": "FORTNITE", "price": "FREE", "image": "path/to/fortnite_image.jpg"},
    {"name": "BW: WUKONG", "price": "฿1,799.00", "image": "path/to/wukong_image.jpg"},
    {"name": "RED DEAD 2", "price": "฿1,599.00", "image": "path/to/red_dead_image.jpg"},
    {"name": "COD: WARFARE 2", "price": "฿1,224.50", "image": "path/to/cod_image.jpg"},
]

shopping_cart = []
user_library = []


def move_to_library():
    global shopping_cart
    user_library.extend(shopping_cart)  # Add items from cart to library
    shopping_cart.clear()               # Clear the cart after purchase
    update_library()                    # Refresh the library display
    update_cart()                       # Refresh the cart display
    Shopping_Cart_content.classes(add='hidden')




def update_library():
    library_display.clear()
    for item in user_library:
        with library_display:
            ui.label(item["name"]).style("color: white; font-size: 20px;")
            ui.button("Download").on_click(lambda: download_game(item))

def update_cart_display():
    # Clear the current cart display
    cart_section.clear()
    
    # Display each item in the shopping cart
    for game in shopping_cart:
        ui.label(game).classes('shopping-cart-item')


def add_to_cart(game_name, price, image_url):
    shopping_cart.append({"name": game_name, "price": price, "image_url": image_url})
    update_cart()
    Shopping_Cart_content.classes(remove='hidden')
    
    
# Function to handle checkout and move games to library
def checkout():
    for item in shopping_cart:
        user_library.append(item)  # Move game to the library for the logged-in user
    shopping_cart.clear()  # Clear the cart after purchase
    update_library()  # Update the library display
    update_cart()  # Update cart display
    Shopping_Cart_content.classes(add='hidden')  # Hide cart after checkout


# Function to update cart display
def update_cart():
    cart_display.clear()
    for item in shopping_cart:
        with cart_display:
            with ui.row().classes("cart-item"):
                ui.image(item["image_url"]).classes("w-[50px] h-[50px]")
                ui.label(item["name"]).style("font-size: 16px; color: white;")
                ui.label(f'฿{item["price"]}').style("font-size: 16px; color: white;")
    # Add "Check Out" button
    ui.button('Check Out', on_click=checkout).style('margin-top: 10px;')

def search_games(query):
    conn = sqlite3.connect('ln2.db')
    cursor = conn.cursor()

    # Search for games based on query
    cursor.execute("SELECT name, price FROM games WHERE name LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()
    conn.close()

    # Display search results
    with search_results_container:
        search_results_container.clear()  # Clear previous results
        ui.label("Search Results:")
        for name, price in results:
            ui.label(f"{name} - ${price}")
            
def show_store_content():
    store_content.classes(replace='block')  # แสดง carousel
    library_content.classes(replace='hidden')  # ซ่อนเนื้อหาอื่น
    Shopping_Cart_content.classes(replace='hidden')

def show_library_content():
    store_content.classes(replace='hidden')
    library_content.classes(replace='block')  # แสดง Library
    Shopping_Cart_content.classes(replace='hidden')

def show_shopping_cart_content():
    store_content.classes(replace='hidden')
    library_content.classes(replace='hidden')
    Shopping_Cart_content.classes(replace='block')  # แสดง Profile


    

# แถบบาร์
with ui.header().style('background: linear-gradient(to right, #591c53, #ff1f76); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2)').classes(replace='row items-center') as header:
    with ui.row().classes('w-full justify-between items-center'):
        with ui.tabs() as tabs:
            ui.image('https://img2.pic.in.th/pic/4418be603786d0ba8d.png').classes('w-[300px] h-[49px]')
            ui.input(placeholder='Search for games...').props('clearable').on('input', search_games).classes('mr-4') 
            ui.tab('Store').on('click', show_store_content)
            ui.tab('Library').on('click', show_library_content)
            ui.tab('Shopping Cart').on('click', show_shopping_cart_content)

      #หน้าdatabase
        with ui.row().style('display: flex; justify-content: flex-end;'):
           login_button = ui.button('Log in1', icon='account_circle').props('flat color=white').on('click', lambda: ui.run_javascript('window.location.href="/login"'))
        #หน้าlogin
        @ui.page('/login')
        def cod_warfare2_page():
         conn = sqlite3.connect('ln2.db')
         c = conn.cursor()
         c.execute('''
         CREATE TABLE IF NOT EXISTS login (
        username TEXT NOT NULL,
        password INTEGER NOT NULL
    );
''')
         # ฟังก์ชันสำหรับการเข้าสู่ระบบ
         def login(username, password):
           c.execute("SELECT * FROM login WHERE username=? AND password=?", (username, password))
           user = c.fetchone()
           if user:
             ui.notify(f'Welcome {username}!', color='green')
             login_button.set_text(username)
           else:
             ui.notify('Login failed. Please check your credentials.', color='red')
         conn.commit()
         # ฟังก์ชันสำหรับการลงทะเบียน
         def register(username, password):
          c.execute("INSERT INTO login (username, password) VALUES (?, ?)", (username, password))
          conn.commit()
          ui.notify('Registration successful!', color='green')

# สร้าง UI
         ui.add_head_html('<style>body{background:linear-gradient(to right,#591c53,#ff1f76); height: 100vh; margin: 0;}</style>')

         with ui.row().classes('justify-center').style('margin-top: 100px; margin-left: 350px; margin-right: 600px;'):
          with ui.card().tight().style('background: linear-gradient(to top, #591c53, #ff1f76); width: 800px; height: 500px;'):
           ui.image('https://img5.pic.in.th/file/secure-sv1/Group-16ecff8af2147ab43.png').style('width: 400px; height: auto; margin-top: 40px; margin-left: 200px;')
        
           username_input = ui.input(label='USERNAME', placeholder='Enter your username').props('flat color=white').style('color: white; width: 400px; height: auto; margin-top: 60px; margin-left: 200px;').props('input-style="color: white;"')
        
           password_input = ui.input(label='PASSWORD', placeholder='Enter your password', password=True).props('flat color=white').style('width: 400px; height: auto; margin-top: 40px; margin-left: 200px;')

           # ปุ่มสำหรับการเข้าสู่ระบบ
           ui.button('LOG IN2', on_click=lambda: login(username_input.value, password_input.value)).style('font-size: 10px; width: 400px; height: auto; margin-top: 50px; margin-left: 200px; ').props('color="green"').on('click',main_store)

           # ปุ่มสำหรับการลงทะเบียน
           ui.button('REGISTER', on_click=lambda: register(username_input.value, password_input.value)).style('font-size: 10px; width: 400px; height: auto; margin-top: 20px; margin-left: 200px; ').props('color="cyan"')





#สไลด์
with ui.row().classes('justify-center').style('margin-top: auto; margin-left: 40px; margin-right: 335px;'):
    store_content = ui.element('div').classes('block')
    with store_content:
        with ui.carousel(animated=True, arrows=True, navigation=True).props('height=250px'):
            with ui.carousel_slide().classes('p-0'):
                ui.image('https://i.postimg.cc/8Psmvt9Q/cyber.png').classes('w-[1400px]')
            with ui.carousel_slide().classes('p-0'):
                ui.image('https://i.postimg.cc/kGH8wPzr/cod.png').classes('w-[1400px]')
            with ui.carousel_slide().classes('p-0'):
                ui.image('https://i.postimg.cc/hPJVvhQK/gta.png').classes('w-[1400px]')

    
    # หมวดหมู่เกม
        with ui.row().classes('space-around'):
    # เลเบล FREE GAMES
             ui.label('FREE GAMES').style('font-size: 28px; font-weight: bold; color: white; margin-top: 60px; margin-right: auto;')
    # เลเบล SPECIAL PRICE GAMES
             ui.label('SPECIAL PRICE GAMES').style('font-size: 28px; font-weight: bold; color: white; margin-top: 60px; margin-left: 20px; margin-right: 335px;')


        def main_store():
             ui.run_javascript('window.location.href="/"')



        with ui.row().classes('justify-between'):  # กระจายการ์ดให้มีช่องว่างระหว่างกัน

    # การ์ดซ้าย: PUBG, Apex, Fortnite
            with ui.row().classes('justify-start'):
        # PUBG
            #หน้าตัวอย่างเกม
             @ui.page('/pubg')
             def cod_warfare2_page():
              ui.image('https://static.cdnlogo.com/logos/p/57/pubg.png').classes('w-[200px] h-[auto] mx-auto')
              ui.label('PUBG: BATTLEGROUND').style('font-size: 40px; font-weight: bold; color: white; margin-top: -10px; text-shadow: 5px 5px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
               #แท็บตัวอย่างเกม
              with ui.tabs().classes('w-full').style('color:white;') as tabs:
               one = ui.tab('Trailer 1')
               two = ui.tab('Trailer 2')
               three = ui.tab('Screenshot 1')
               four = ui.tab('Screenshot 2')
               five = ui.tab('Screenshot 3')
              with ui.tab_panels(tabs, value=one).classes('w-full').style('background: linear-gradient(to right,#3f1b10,#7c4125);'):
               with ui.tab_panel(one):
                   ui.video('https://cdn.discordapp.com/attachments/1082744348690624646/1289906725566283797/PUBG___Veil_of_Taego__Episode_3_-_PUBG__BATTLEGROUNDS_1080p_h264_youtube.mp4?ex=66fdd280&is=66fc8100&hm=808cd7f768ebdbb37798fd433d1f2fc6f8b41a4c468bbe3d2c26f84bc694dbfd&' , autoplay=True ).classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(two):
                   ui.video('https://cdn.discordapp.com/attachments/1082744348690624646/1289906806709030932/PUBG___Survivors_Left_Behind_-_Gameplay_Trailer_-_PUBG__BATTLEGROUNDS_1080p_h264_youtube.mp4?ex=66fdd294&is=66fc8114&hm=f003e5cd4a8adb127d408ede24d9b636b60f73da56a2c0f9983425c8a63c699d&' , autoplay=True ).classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(three):
                 ui.image('https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/578080/ss_66e156cf716e72096c15c132c3443e774cb2f9a5.1920x1080.jpg?t=1727384289').classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(four):
                 ui.image('https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/578080/ss_034714c0f118657ac694c5b9c43bb647ed9ec051.1920x1080.jpg?t=1727384289').classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(five):
                 ui.image('https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/578080/ss_109d7072cf85f5b3b1e3dacadf3009718db451c4.1920x1080.jpg?t=1727384289').classes('w-[1000px] h-[562px] mx-auto')
              #ปุ่มเพิ่มไปตระกร้า  
              ui.button('ADD TO SHOPPING CART', on_click=lambda: add_to_cart('GAME 1', 100.00, 'https://example.com/game_image.png')).style('font-size: 16px;').props('color="green"')
              # with ui.row().classes('justify-center'):
              #   ui.button('ADD TO SHOPPING CART', on_click=lambda: add_to_cart('PUBG')).style('font-size: 10px;').props('color="green"')
             # ui.button('ADD TO SHOPPING CART', classes='mx-auto', color='green').on('click', lambda: Shopping_Cart_content.classes(remove='hidden'))
              #  ui.button('ADD TO SHOPPING CART', on_click=lambda: add_to_cart('PUBG')).style('font-size: 10px;').props('color="green"')

              #เกียวกับเกม
              ui.label('ABOUT THIS GAME').style('font-size: 25px; font-weight: bold; color: white; margin-top: 50px; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
              with ui.card().tight().classes('w-[1000px] h-[130px] mx-auto').style('background: linear-gradient(to right,#3f1b10,#7c4125);'):
                with ui.card_section():
                  ui.label('เล่น PUBG: BATTLEGROUNDS ฟรี').style('font-size: 18px; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7); ')
                  ui.label('ลงจอดบนพื้นที่ยุทธศาสตร์ ปล้นอาวุธและเสบียง และเอาชีวิตรอดเพื่อเป็นทีมสุดท้ายที่ยืนอยู่ในสมรภูมิที่หลากหลายและหลากหลาย').style('font-size: 18px; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7); ')
                  ui.label('รวมทีมและเข้าร่วม Battlegrounds เพื่อสัมผัสประสบการณ์ Battle Royale ดั้งเดิมที่มีเพียง PUBG: BATTLEGROUNDS เท่านั้นที่สามารถให้ได้').style('font-size: 18px; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7); ')
              #เความต้องการของระบบ
              ui.label('SYSTEM REQUIREMENTS').style('font-size: 25px; font-weight: bold; color: white; margin-top: 50px; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
              with ui.row():
               with ui.card().tight().classes('w-[475px] h-[160px] justify-start').style('background: linear-gradient(to right,#3f1b10,#7c4125); margin-left:241px'):
                with ui.card_section():
                      ui.label('Minimum Specifications').style('font-size: 25px; font-weight: bold; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('OS: Windows 10 64 Bit').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('CPU: Intel Core i5-4430 or AMD FX-6300').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('RAM: 8 GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('Video Card:  NVIDIA GeForce GTX 960 2GB or AMD Radeon R7 370 2GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('Storage: 30 GB available space').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
               with ui.card().tight().classes('w-[512px] h-[160px] justify-start').style('background: linear-gradient(to right,#7c4125,#7c4125);'):
                with ui.card_section():
                       ui.label('Recommended Specifications').style('font-size: 25px; font-weight: bold; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('OS: Windows 10 64 Bit').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('CPU: Intel Core i5-6600K or AMD Ryzen 5 1600').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('RAM: 16 GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('Video Card: NVIDIA GeForce GTX 1060 3GB or AMD Radeon RX 580 4GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('Storage: 30 GB available space').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
              ui.add_head_html('<style>body{background:linear-gradient(to right,#3f1b10,#7c4125);}</style>')
              # แถบบาร์1
              with ui.header().style('background: linear-gradient(to right, #3f1b10, #7c4125); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2)').classes(replace='row items-center') as header:
               with ui.row().classes('w-full justify-between items-center'):
                with ui.tabs() as tabs:
                 ui.image('https://cdn.discordapp.com/attachments/1149668982127853572/1286314883801153722/ROCKET444.png?ex=66ed7596&is=66ec2416&hm=a54383ae76f0c99239ded909c2756da6d141f118a5a7c9317baa4e3e662e8981&').classes('w-[300px] h-[49px]')
                 ui.tab('Store').on('click',main_store)
                 ui.tab('Library').on('click', show_library_content)
                 ui.tab('Shopping Cart').on('click', show_shopping_cart_content)
                with ui.row().style('display: flex; justify-content: flex-end;'):
                 ui.button('Log in', icon='account_circle').props('flat color=white')

                 #การ์ดเกม
             with ui.card().tight().props('height=200px').classes('w-[200px] mt-4').style('background: linear-gradient(to right, #3f1b10, #7c4125); margin-top: auto; margin-left: 0px; margin-right: auto;'):
               ui.image('https://img5.pic.in.th/file/secure-sv1/pg20a16977b0d9265b.png').classes('w-full h-full object-cover')
               with ui.card_section():
                ui.label('PUBG').style('color: white; font-size: 20px;')
                ui.button('Free').style('font-size: 10px;').props('color="green"').on('click', lambda: ui.run_javascript('window.location.href="/pubg"'))

        # Apex Legend
            #หน้าตัวอย่างเกม
             @ui.page('/apex_legends')
             def cod_warfare2_page():
              #ชื่อเกม
              ui.image('https://img2.pic.in.th/pic/imageaa89fdc72eb050e6.png').classes('w-[300px] h-[auto] mx-auto').style('margin-top: 10px;')
              ui.label('APEX LEGENDS').style('font-size: 40px; font-weight: bold; color: white; margin-top: 1px; text-shadow: 5px 5px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
               #แท็บตัวอย่างเกม
              with ui.tabs().classes('w-full').style('color:white;') as tabs:
               one = ui.tab('Trailer 1')
               two = ui.tab('Trailer 2')
               three = ui.tab('Screenshot 1')
               four = ui.tab('Screenshot 2')
               five = ui.tab('Screenshot 3')
              with ui.tab_panels(tabs, value=one).classes('w-full').style('background: linear-gradient(to right,#7f1d05,#ab4127);'):
               with ui.tab_panel(one):
                   ui.video('https://cdn.discordapp.com/attachments/1082744348690624646/1289900702738681887/Apex_Legends__Space_Hunt_Event_Trailer_-_Apex_Legends_1080p60_h264_youtube.mp4?ex=66fe75a4&is=66fd2424&hm=647d27a164430cee6933ad516842fadcc00b3537e268c617d8b6587242e24376&' , autoplay=True ).classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(two):
                   ui.video('https://cdn.discordapp.com/attachments/1082744348690624646/1289901074521526273/Apex_Legends__Temporal_Chaos_Collection_Event_-_Apex_Legends_1080p60_h264_youtube.mp4?ex=66fe75fd&is=66fd247d&hm=c174b9752f3c4168de10382b66dcb7b7cb580f2c1a043eea34ab5adb69dd2cc1&' , autoplay=True ).classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(three):
                 ui.image('https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1172470/ss_5de2eea9cfb1d4a76ac540662e86a99c0c1f5627.1920x1080.jpg?t=1727104892').classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(four):
                 ui.image('https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1172470/ss_0e1e750780d80e00a91ac27135a9e2800ed91995.1920x1080.jpg?t=1727104892').classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(five):
                 ui.image('https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1172470/ss_6839de0a879d749eb93b10bda5f42ba3d6c7ff3a.1920x1080.jpg?t=1727104892').classes('w-[1000px] h-[562px] mx-auto')
              #ปุ่มเพิ่มไปตระกร้า  
              ui.button('ADD TO SHOPPING CART', on_click=lambda: add_to_cart('GAME 1', 100.00, 'https://example.com/game_image.png')).style('font-size: 16px;').props('color="green"')

              #เกียวกับเกม
              ui.label('ABOUT THIS GAME').style('font-size: 25px; font-weight: bold; color: white; margin-top: 50px; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
              with ui.card().tight().classes('w-[1000px] h-[130px] mx-auto').style('background: linear-gradient(to right,#7f1d05,#ab4127);'):
                with ui.card_section():
                  ui.label('พิชิตด้วยเอกลักษณ์ใน Apex Legends เกม Hero Shooter แบบเล่นฟรี ที่เหล่าตัวละครในตำนานซึ่งมีความสามารถทรงพลังจะร่วมมือกันต่อสู้เพื่อชื่อเสียงและทรัพย์สมบัติในเขตชายแดน').style('font-size: 18px; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7); ')
                  ui.label('ฝึกฝนการใช้ Legends หลากหลายที่เพิ่มขึ้นอย่างต่อเนื่อง, การเล่นเป็นทีมเชิงกลยุทธ์ที่ลึกซึ้ง, และนวัตกรรมใหม่ที่กล้าหาญซึ่งก้าวไปไกลกว่าประสบการณ์ Battle Royale — ทั้งหมดนี้ในโลกที่ขรุขระซึ่งทุกอย่างเกิดขึ้นได้ ยินดีต้อนรับสู่วิวัฒนาการถัดไปของเกม Hero Shooter.').style('font-size: 18px; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7); ')
              #เความต้องการของระบบ
              ui.label('SYSTEM REQUIREMENTS').style('font-size: 25px; font-weight: bold; color: white; margin-top: 50px; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
              with ui.row():
               with ui.card().tight().classes('w-[475px] h-[160px] justify-start').style('background: linear-gradient(to right,#7f1d05,#ab4127); margin-left:241px'):
                with ui.card_section():
                      ui.label('Minimum Specifications').style('font-size: 25px; font-weight: bold; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('OS: Windows 10 64 Bit').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('CPU: Intel Core i5-4430 or AMD FX-6300').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('RAM: 8 GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('Video Card:  NVIDIA GeForce GTX 960 2GB or AMD Radeon R7 370 2GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('Storage: 30 GB available space').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
               with ui.card().tight().classes('w-[512px] h-[160px] justify-start').style('background: linear-gradient(to right,#ab4127,#ab4127);'):
                with ui.card_section():
                       ui.label('Recommended Specifications').style('font-size: 25px; font-weight: bold; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('OS: Windows 10 64 Bit').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('CPU: Intel Core i5-6600K or AMD Ryzen 5 1600').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('RAM: 16 GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('Video Card: NVIDIA GeForce GTX 1060 3GB or AMD Radeon RX 580 4GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('Storage: 30 GB available space').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
              ui.add_head_html('<style>body{background:linear-gradient(to right,#7f1d05,#ab4127);}</style>')
              # แถบบาร์2
              with ui.header().style('background: linear-gradient(to right, #7f1d05, #ab4127); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2)').classes(replace='row items-center') as header:
               with ui.row().classes('w-full justify-between items-center'):
                with ui.tabs() as tabs:
                 ui.image('https://cdn.discordapp.com/attachments/1149668982127853572/1286314883801153722/ROCKET444.png?ex=66ed7596&is=66ec2416&hm=a54383ae76f0c99239ded909c2756da6d141f118a5a7c9317baa4e3e662e8981&').classes('w-[300px] h-[49px]')
                 ui.tab('Store').on('click',main_store)
                 ui.tab('Library').on('click', show_library_content)
                 ui.tab('Shopping Cart').on('click', show_shopping_cart_content)
                with ui.row().style('display: flex; justify-content: flex-end;'):
                 ui.button('Log in', icon='account_circle').props('flat color=white')

                 #การ์ดเกม
             with ui.card().tight().props('height=200px').classes('w-[200px] mt-4').style('background: linear-gradient(to right, #7f1d05, #ab4127);'):
               ui.image('https://img2.pic.in.th/pic/image09c20fc7f53b8c77.png').classes('w-full h-full object-cover')
               with ui.card_section():
                ui.label('APEX LEGENDS').style('color: white; font-size: 20px;')
                ui.button('Free').style('font-size: 10px;').props('color="green"').on('click', lambda: ui.run_javascript('window.location.href="/apex_legends"'))

        # Fortnite
            #หน้าตัวอย่างเกม
             @ui.page('/fortnite')
             def cod_warfare2_page():
               #ชื่อเกม
              ui.image('https://img5.pic.in.th/file/secure-sv1/imagedb63ef39374e5a69.png').classes('w-[300px] h-[auto] mx-auto').style('margin-top: 10px;')
              ui.label('FORTNITE').style('font-size: 40px; font-weight: bold; color: white; margin-top: 10px; text-shadow: 5px 5px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
               #แท็บตัวอย่างเกม
              with ui.tabs().classes('w-full').style('color:white;') as tabs:
               one = ui.tab('Trailer 1')
               two = ui.tab('Trailer 2')
               three = ui.tab('Screenshot 1')
               four = ui.tab('Screenshot 2')
               five = ui.tab('Screenshot 3')
              with ui.tab_panels(tabs, value=one).classes('w-full').style('background: linear-gradient(to right,#1561c0,#f24aab);'):
               with ui.tab_panel(one):
                   ui.video('https://cdn.discordapp.com/attachments/1082744348690624646/1289893149841293333/Fortnite_Battle_Royale_Chapter_5_Season_4_-_Absolute_Doom___Official_Season_Trailer_-_Fortnite_1080p60_h264_youtube.mp4?ex=66fe6e9b&is=66fd1d1b&hm=a19627b1076c7c2a9104c49d86d142c4e39b29c00cb9706455009a870dfdd54b&' , autoplay=True ).classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(two):
                   ui.video('https://cdn.discordapp.com/attachments/1082744348690624646/1289894816922075217/Day_of_Doom_-_New_Fortnite_x_Marvel_LTM_-_Fortnite_1080p_h264_youtube.mp4?ex=66fe7029&is=66fd1ea9&hm=790afac035cd415ab44eb1c7f4827e63b0cbb2cc53fd1cce6f3adcb4492ba330&' , autoplay=True ).classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(three):
                 ui.image('https://pbs.twimg.com/media/GX25FCmX0AA9OVM?format=jpg&name=4096x4096').classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(four):
                 ui.image('https://pbs.twimg.com/media/GUyVvNHXYAAthqO?format=jpg&name=large').classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(five):
                 ui.image('https://cdn2.unrealengine.com/download-key-art2-1920x1080-21e209f6bab4.jpg').classes('w-[1000px] h-[562px] mx-auto')
              #ปุ่มเพิ่มไปตระกร้า  
              ui.button('ADD TO SHOPPING CART').classes('mx-auto ').props('color="green"')
              #เกียวกับเกม
              ui.label('ABOUT THIS GAME').style('font-size: 25px; font-weight: bold; color: white; margin-top: 50px; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
              with ui.card().tight().classes('w-[1000px] h-[100px] mx-auto').style('background: linear-gradient(to right,#1561c0,#f24aab);'):
                with ui.card_section():
                  ui.label('สร้าง เล่น และต่อสู้กับเพื่อนฟรีใน Fortnite เป็นผู้เล่นคนสุดท้ายที่เหลือรอดใน Battle Royale และ Zero Build ชมคอนเสิร์ตหรือไลฟ์อีเวนต์ หรือพบกับนักสร้างเกมนับล้าน เช่น เกมแข่งรถ ปากัวร์ เอาชีวิตรอดจากซอมบี้ และอีกมากมาย เกาะ Fortnite จะมีการจัดเรตอายุสำหรับแต่ละเกาะ คุณจึงสามารถเลือกสรรเกาะที่เหมาะสำหรับคุณกับเพื่อนๆ ได้ พบทั้งหมดนี้ได้ใน Fortnite ... แวะมาเล่นเลย').style('font-size: 18px; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7); ')
              #เความต้องการของระบบ
              ui.label('SYSTEM REQUIREMENTS').style('font-size: 25px; font-weight: bold; color: white; margin-top: 50px; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
              with ui.row():
               with ui.card().tight().classes('w-[475px] h-[160px] justify-start').style('background: linear-gradient(to right,#1561c0,#f24aab); margin-left:241px'):
                with ui.card_section():
                      ui.label('Minimum Specifications').style('font-size: 25px; font-weight: bold; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('OS: Windows 10 64 Bit').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('CPU: Core i3-3225 3.3 GHz').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('RAM: 8 GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('Video Card: Intel HD 4000 or AMD Radeon Vega 8').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('Storage: 30 GB available space').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
               with ui.card().tight().classes('w-[512px] h-[160px] justify-start').style('background: linear-gradient(to right,#f24aab,#f24aab);'):
                with ui.card_section():
                       ui.label('Recommended Specifications').style('font-size: 25px; font-weight: bold; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('OS: Windows 10 64 Bit').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('CPU: Core i5-7300U 3.5 GHz or AMD Ryzen 3 3300U ').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('RAM: 12 GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('Video Card: Nvidia GTX 960 or AMD R9 280').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('Storage: 30 GB available space').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
              ui.add_head_html('<style>body{background:linear-gradient(to right,#1561c0,#f24aab);}</style>')
              # แถบบาร์3
              with ui.header().style('background: linear-gradient(to right, #1561c0, #f24aab); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2)').classes(replace='row items-center') as header:
               with ui.row().classes('w-full justify-between items-center'):
                with ui.tabs() as tabs:
                 ui.image('https://cdn.discordapp.com/attachments/1149668982127853572/1286314883801153722/ROCKET444.png?ex=66ed7596&is=66ec2416&hm=a54383ae76f0c99239ded909c2756da6d141f118a5a7c9317baa4e3e662e8981&').classes('w-[300px] h-[49px]')
                 ui.tab('Store').on('click',main_store)
                 ui.tab('Library').on('click', show_library_content)
                 ui.tab('Shopping Cart').on('click', show_shopping_cart_content)
                with ui.row().style('display: flex; justify-content: flex-end;'):
                 ui.button('Log in', icon='account_circle').props('flat color=white')

                 #การ์ดเกม
             with ui.card().tight().props('height=200px').classes('w-[200px] mt-4').style('background: linear-gradient(to right, #1561c0, #f24aab);'):
               ui.image('https://img5.pic.in.th/file/secure-sv1/fn.png').classes('w-full h-full object-cover')
               with ui.card_section():
                 ui.label('FORTNITE').style('color: white; font-size: 20px;')
                 ui.button('Free').style('font-size: 10px;').props('color="green"').on('click', lambda: ui.run_javascript('window.location.href="/fortnite"'))

    # การ์ดขวา: Black Myth Wukong, RDR2, COD Warfare 2
            with ui.row().classes('justify-end'):
        # BLACK MYTH WUKONG
        #หน้าตัวอย่างเกม
             @ui.page('/bw_wukong')
             def cod_warfare2_page():

              #ชื่อเกม
              ui.image('https://cdn2.steamgriddb.com/logo/d022f8f5b598a462808167f2e7a4af3b.png').classes('w-[300px] h-[auto] mx-auto').style('margin-top: 10px;')
              ui.label('BLACK MYTH: WUKONG').style('font-size: 40px; font-weight: bold; color: white; margin-top: 10px; text-shadow: 5px 5px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
               #แท็บตัวอย่างเกม
              with ui.tabs().classes('w-full').style('color:white;') as tabs:
               one = ui.tab('Trailer 1')
               two = ui.tab('Trailer 2')
               three = ui.tab('Screenshot 1')
               four = ui.tab('Screenshot 2')
               five = ui.tab('Screenshot 3')
              with ui.tab_panels(tabs, value=one).classes('w-full').style('background: linear-gradient(to right,#444b55,#8798ac);'):
               with ui.tab_panel(one):
                   ui.video('https://cdn.discordapp.com/attachments/1082744348690624646/1289884475056062494/Black_Myth__Wukong_-_Pre-Order_CG_Trailer___PS5_Games_-_PlayStation_1080p60_h264_youtube.mp4?ex=66fe6687&is=66fd1507&hm=b5e1fb01ae4ca99774eb3d767baae724a34ea2cc6aeb46c61810ae4f71e074d5&' , autoplay=True ).classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(two):
                   ui.video('https://cdn.discordapp.com/attachments/1082744348690624646/1289885906391793664/Black_Myth__Wukong_-_Launch_Trailer___PS5_Games_-_PlayStation_1080p60_h264_youtube.mp4?ex=66fe67dd&is=66fd165d&hm=871c3232c8fdd4ef50cd9022ff4a4ce8d1b56f0c59d6d55089fbb80cb6dd9ae2&' , autoplay=True ).classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(three):
                 ui.image('https://images2.alphacoders.com/135/thumb-1920-1353330.jpeg').classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(four):
                 ui.image('https://images8.alphacoders.com/112/1129254.jpg').classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(five):
                 ui.image('https://images3.alphacoders.com/137/1377037.jpg').classes('w-[1000px] h-[562px] mx-auto')
              #ปุ่มเพิ่มไปตระกร้า  
              ui.button('ADD TO SHOPPING CART').classes('mx-auto ').props('color="green"')
              #เกียวกับเกม
              ui.label('ABOUT THIS GAME').style('font-size: 25px; font-weight: bold; color: white; margin-top: 50px; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
              with ui.card().tight().classes('w-[1000px] h-[100px] mx-auto').style('background: linear-gradient(to right,#444b55,#8798ac);'):
                with ui.card_section():
                  ui.label('Black Myth: Wukong เป็นเกม RPG แอคชันที่มีรากฐานมาจากตำนานจีน เรื่องราวนี้อิงจาก Journey to the West หรือ ไซอิ๋ว ซึ่งเป็นหนึ่งในสี่นวนิยายคลาสสิกที่ยิ่งใหญ่ของวรรณกรรมจีน คุณจะได้ออกเดินทางในฐานะผู้ถูกกำหนด เพื่อเผชิญกับความท้าทายและสิ่งมหัศจรรย์ข้างหน้า เพื่อเปิดเผยความจริงที่ถูกบดบังอยู่ภายใต้ม่านของตำนานที่รุ่งโรจน์จากอดีต').style('font-size: 18px; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7); ')
              #เความต้องการของระบบ
              ui.label('SYSTEM REQUIREMENTS').style('font-size: 25px; font-weight: bold; color: white; margin-top: 50px; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
              with ui.row():
               with ui.card().tight().classes('w-[475px] h-[185px] justify-start').style('background: linear-gradient(to right,#444b55,#8798ac); margin-left:241px'):
                with ui.card_section():
                      ui.label('Minimum Specifications').style('font-size: 25px; font-weight: bold; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('OS: Windows 10 64 Bit').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('CPU: Intel Core i5-8400 / AMD 5 1600').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('RAM: 16 GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('Video Card: NVIDIA GeForce GTX 1060 (6GB) / AMD Radeon RX 580 (8GB)').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('Storage: 130 GB available space').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
               with ui.card().tight().classes('w-[512px] h-[185px] justify-start').style('background: linear-gradient(to right,#8798ac,#8798ac);'):
                with ui.card_section():
                       ui.label('Recommended Specifications').style('font-size: 25px; font-weight: bold; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('OS: Windows 10 64 Bit').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('CPU: Intel Core i7-9700 / AMD Ryzen 5 5500').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('RAM: 12 GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('Video Card: NVIDIA GeForce GTX 2060 / AMD Radeon RX 5700XT / INTEL Arc A750').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('Storage: 150 GB available space').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')


              ui.add_head_html('<style>body{background:linear-gradient(to right,#444b55,#8798ac);}</style>')
              # แถบบาร์4
              with ui.header().style('background: linear-gradient(to right, #444b55, #8798ac); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2)').classes(replace='row items-center') as header:
               with ui.row().classes('w-full justify-between items-center'):
                with ui.tabs() as tabs:
                 ui.image('https://cdn.discordapp.com/attachments/1149668982127853572/1286314883801153722/ROCKET444.png?ex=66ed7596&is=66ec2416&hm=a54383ae76f0c99239ded909c2756da6d141f118a5a7c9317baa4e3e662e8981&').classes('w-[300px] h-[49px]')
                 ui.tab('Store').on('click',main_store)
                 ui.tab('Library').on('click', show_library_content)
                 ui.tab('Shopping Cart').on('click', show_shopping_cart_content)
                with ui.row().style('display: flex; justify-content: flex-end;'):
                 ui.button('Log in', icon='account_circle').props('flat color=white')

                 #การ์ดเกม
             with ui.card().tight().props('height=200px').classes('w-[200px] mt-4').style('background: linear-gradient(to right, #444b55, #8798ac);'):
                ui.image('https://img2.pic.in.th/pic/wk.png').classes('w-full h-full object-cover')
                with ui.card_section():
                 ui.label('BW : WUKONG').style('color: white; font-size: 20px;')
                 ui.button('฿1,799.00').style('font-size: 10px;').props('color="green"').on('click', lambda: ui.run_javascript('window.location.href="/bw_wukong"'))

        # RDR2
            #หน้าตัวอย่างเกม
             @ui.page('/rdr2')
             def cod_warfare2_page():
              
              #ชื่อเกม
              ui.image('https://upload.wikimedia.org/wikipedia/commons/2/22/Red_Dead_Redemption_2_Logo.png').classes('w-[300px] h-[auto] mx-auto').style('margin-top: 10px;')
              ui.label('RED DEAD REDEMPTION 2').style('font-size: 40px; font-weight: bold; color: white; margin-top: 10px; text-shadow: 5px 5px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
               #แท็บตัวอย่างเกม
              with ui.tabs().classes('w-full').style('color:white;') as tabs:
               one = ui.tab('Trailer 1')
               two = ui.tab('Trailer 2')
               three = ui.tab('Screenshot 1')
               four = ui.tab('Screenshot 2')
               five = ui.tab('Screenshot 3')
              with ui.tab_panels(tabs, value=one).classes('w-full').style('background: linear-gradient(to right, #8c0809, #ca0514);'):
               with ui.tab_panel(one):
                   ui.video('https://cdn.discordapp.com/attachments/1082744348690624646/1289880517403213834/Red_Dead_Redemption_2_PC_-_Official_4K_Trailer_-_IGN_1080p60_h264_youtube.mp4?ex=66fe62d8&is=66fd1158&hm=f28cc0b8c0defd58921a207988b827adcf868d65f71f9e36f61dcde39a98faf1&' , autoplay=True ).classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(two):
                   ui.video('https://cdn.discordapp.com/attachments/1082744348690624646/1289881294506950727/Red_Dead_Redemption_2_PC_Trailer_-_Rockstar_Games_1080p60_h264_youtube.mp4?ex=66fe6391&is=66fd1211&hm=7cc62a7b589aea07c6c95f987eeacd3a3b53d113f65e2f5be7707844720eb806&' , autoplay=True ).classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(three):
                 ui.image('https://images6.alphacoders.com/128/1282801.jpg').classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(four):
                 ui.image('https://images7.alphacoders.com/134/thumb-1920-1344757.png').classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(five):
                 ui.image('https://images4.alphacoders.com/948/thumb-1920-948666.jpg').classes('w-[1000px] h-[562px] mx-auto')
              #ปุ่มเพิ่มไปตระกร้า  
              ui.button('ADD TO SHOPPING CART').classes('mx-auto ').props('color="green"')
              #เกียวกับเกม
              ui.label('ABOUT THIS GAME').style('font-size: 25px; font-weight: bold; color: white; margin-top: 50px; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
              with ui.card().tight().classes('w-[1000px] h-[430px] mx-auto').style('background: linear-gradient(to right, #8c0809, #ca0514);'):
                with ui.card_section():
                  ui.label('อเมริกา ปี 1899').style('font-size: 18px; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7); ')
                  ui.label('อาร์เธอร์ มอร์แกน และแก๊งแวนเดอร์ลินด์คือกลุ่มโจรที่กำลังหนี โดยมีเจ้าหน้าที่ของรัฐบาลกลางและนักล่าค่าหัวที่เก่งที่สุดในประเทศติดตามพวกเขาอยู่ แก๊งนี้จำเป็นต้องปล้น, ขโมย และต่อสู้เพื่อเอาชีวิตรอดในใจกลางที่ขรุขระของอเมริกา ขณะที่ความขัดแย้งภายในเริ่มลึกซึ้งและคุกคามที่จะฉีกแก๊งนี้ออกเป็นชิ้น ๆ อาร์เธอร์ต้องเลือกว่าจะยึดมั่นในอุดมคติของตนเองหรือซื่อสัตย์ต่อแก๊งที่เลี้ยงดูเขา').style('font-size: 18px; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7); ')
                  ui.label('ตอนนี้มีเนื้อหาใหม่ในโหมดเนื้อเรื่องและโหมดถ่ายภาพที่มีฟีเจอร์ครบครัน Red Dead Redemption 2 ยังให้การเข้าถึงโลกออนไลน์ที่แชร์ร่วมกันของ Red Dead Online ฟรี ซึ่งผู้เล่นสามารถสวมบทบาทต่าง ๆ เพื่อสร้างเส้นทางที่ไม่เหมือนใครในเขตชายแดน โดยติดตามอาชญากรที่ต้องการในฐานะนักล่าค่าหัว, สร้างธุรกิจในฐานะพ่อค้า, ค้นพบสมบัติแปลกใหม่ในฐานะนักสะสม หรือดำเนินการโรงกลั่นสุราใต้ดินในฐานะผู้ผลิตสุราผิดกฎหมาย และอื่น ๆ').style('font-size: 18px; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7); ')
                  ui.label('Red Dead Redemption 2 สำหรับ PC ยังมีการปรับปรุงกราฟิกและเทคนิคใหม่ ๆ เพื่อเพิ่มความสมจริง โดยใช้พลังของ PC ให้เต็มที่เพื่อทำให้ทุกมุมของโลกอันกว้างใหญ่ที่เต็มไปด้วยรายละเอียดมีชีวิตชีวา รวมถึงระยะการมองเห็นที่เพิ่มขึ้น, คุณภาพการส่องสว่างทั่วโลกและการสร้างเงาที่ดีขึ้นเพื่อปรับปรุงการให้แสงในเวลากลางวันและกลางคืน, การสะท้อนที่ดีขึ้น และเงาที่มีความละเอียดลึกและสูงขึ้นในระยะทางทุกระยะ, เท็กซ์เจอร์ของต้นไม้ที่มีการสร้างแบบพิเศษ และการปรับปรุงเท็กซ์เจอร์ของหญ้าและขนสัตว์เพื่อเพิ่มความสมจริงให้กับพืชและสัตว์ทุกชนิด').style('font-size: 18px; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7); ')
                  ui.label('Red Dead Redemption 2 สำหรับ PC ยังรองรับ HDR, ความสามารถในการทำงานกับการตั้งค่าจอแสดงผลระดับสูงที่มีความละเอียด 4K ขึ้นไป, การตั้งค่าหลายจอ, การตั้งค่าจอแสดงผลกว้าง, อัตราเฟรมที่เร็วขึ้น และอื่น ๆ').style('font-size: 18px; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7); ')
              #เความต้องการของระบบ
              ui.label('SYSTEM REQUIREMENTS').style('font-size: 25px; font-weight: bold; color: white; margin-top: 50px; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
              with ui.row():
               with ui.card().tight().classes('w-[475px] h-[160px] justify-start').style('background: linear-gradient(to right, #8c0809, #ca0514); margin-left:241px'):
                with ui.card_section():
                      ui.label('Minimum Specifications').style('font-size: 25px; font-weight: bold; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('OS: Windows 10 64 Bit').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('CPU: Intel® Core™ i5-2500K / AMD FX-6300').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('RAM: 8 GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('Video Card: Nvidia GeForce GTX 770 2GB / AMD Radeon R9 280 3GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('Storage: 150 GB available space').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
               with ui.card().tight().classes('w-[512px] h-[160px] justify-start').style('background: linear-gradient(to right, #ca0514, #ca0514);'):
                with ui.card_section():
                       ui.label('Recommended Specifications').style('font-size: 25px; font-weight: bold; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('OS: Windows 10 64 Bit').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('CPU: Intel® Core™ i7-4770K / AMD Ryzen 5 1500X').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('RAM: 12 GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('Video Card: Nvidia GeForce GTX 1060 6GB / AMD Radeon RX 480 4GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('Storage: 150 GB available space').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')

              ui.add_head_html('<style>body{background:linear-gradient(to right,#8c0809,#ca0514);}</style>')
              # แถบบาร์5
              with ui.header().style('background: linear-gradient(to right, #8c0809, #ca0514); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2)').classes(replace='row items-center') as header:
               with ui.row().classes('w-full justify-between items-center'):
                with ui.tabs() as tabs:
                 ui.image('https://cdn.discordapp.com/attachments/1149668982127853572/1286314883801153722/ROCKET444.png?ex=66ed7596&is=66ec2416&hm=a54383ae76f0c99239ded909c2756da6d141f118a5a7c9317baa4e3e662e8981&').classes('w-[300px] h-[49px]')
                 ui.tab('Store').on('click',main_store)
                 ui.tab('Library').on('click', show_library_content)
                 ui.tab('Shopping Cart').on('click', show_shopping_cart_content)
                with ui.row().style('display: flex; justify-content: flex-end;'):
                 ui.button('Log in', icon='account_circle').props('flat color=white')

                 #การ์ดเกม
             with ui.card().tight().props('height=200px').classes('w-[200px] mt-4').style('background: linear-gradient(to right, #8c0809, #ca0514);'):
                 ui.image('https://img5.pic.in.th/file/secure-sv1/ouu.png').classes('w-full h-full object-cover')
                 with ui.card_section():
                  ui.label('RED DEAD 2').style('color: white; font-size: 20px;')
                  ui.button('฿1,599.00').style('font-size: 10px;').props('color="green"').on('click', lambda: ui.run_javascript('window.location.href="/rdr2"'))

        # COD : WARFARE 2
              #หน้าตัวอย่างเกมม
             @ui.page('/cod_warfare2')
             def cod_warfare2_page():
              ui.add_head_html('<style>body{background:linear-gradient(to right,#254120,#529446);}</style>')
              #ชื่อเกม/โลโก้เกมมมม
              ui.image('https://image.ceneostatic.pl/data/article_picture/d5/cc/a8fa-2c24-40cf-94af-22fbd62eeceb_large.png').classes('w-[300px] h-[auto] mx-auto').style('margin-top: 10px;')
              ui.label('CALL OF DUTY : MODERN WARFARE II').style('font-size: 40px; font-weight: bold; color: white; margin-top: 10px; text-shadow: 5px 5px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
               #แท็บตัวอย่างเกมมม
              with ui.tabs().classes('w-full').style('color:white;') as tabs:
               one = ui.tab('Trailer 1')
               two = ui.tab('Trailer 2')
               three = ui.tab('Screenshot 1')
               four = ui.tab('Screenshot 2')
               five = ui.tab('Screenshot 3')
              with ui.tab_panels(tabs, value=one).classes('w-full').style('background: linear-gradient(to right, #254120, #529446);'):
               with ui.tab_panel(one):
                   ui.video('https://cdn.discordapp.com/attachments/1082744348690624646/1289833239380230286/SnapSave.io-Call_of_Duty__Modern_Warfare_II_-_Official__Ultimate_Team__Teaser_Trailer.mp4?ex=66fe36d0&is=66fce550&hm=13f416040db32888700e7824812192d2c54438980f442a4cc5cbf9ea6504021f&' , autoplay=True ).classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(two):
                   ui.video('https://cdn.discordapp.com/attachments/1082744348690624646/1289837064178634805/SnapSave.io-Call_of_Duty__Modern_Warfare_II_Worldwide_Reveal_Trailer.mp4?ex=66fe3a60&is=66fce8e0&hm=402d18282019d618289b10f9597617a19f424ae0c21bcd50d0304eedabb5e9a4&' , autoplay=True ).classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(three):
                 ui.image('https://img5.pic.in.th/file/secure-sv1/4591a209f774c6c8b.png').classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(four):
                 ui.image('https://img5.pic.in.th/file/secure-sv1/39360da7e12b49b8f.png').classes('w-[1000px] h-[562px] mx-auto')
               with ui.tab_panel(five):
                 ui.image('https://img2.pic.in.th/pic/2dd943529a276f6db.png').classes('w-[1000px] h-[562px] mx-auto')
              #ปุ่มเพิ่มไปตระกร้า  
              ui.button('ADD TO SHOPPING CART').classes('mx-auto ').props('color="green"')
              #เกียวกับเกม
              ui.label('ABOUT THIS GAME').style('font-size: 25px; font-weight: bold; color: white; margin-top: 50px; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
              with ui.card().tight().classes('w-[1000px] h-[160px] mx-auto').style('background: linear-gradient(to right, #254120, #529446);'):
                with ui.card_section():
                     ui.label('ยินดีต้อนรับสู่ยุคใหม่ของ Call of Duty Call of Duty®: Modern Warfare® II พาผู้เล่นไปเผชิญกับความขัดแย้งทั่วโลกในแบบที่ไม่เคยมีมาก่อน ที่มาพร้อมโอเปอเรเตอร์แห่งกองกำลังเฉพาะกิจ 141 ที่ใครๆ ก็รู้จัก ผู้เล่นจะได้ลงไปลุยคู่กับสหายร่วมรบในประสบการณ์ที่สมจริง ตั้งแต่ปฏิบัติการแทรกซึมขนาดเล็กที่มีความเสี่ยงสูงไปจนถึงภารกิจลับสุดยอด'
                       'Infinity Ward จะให้แฟนๆ ได้สัมผัสกับเกมเพลย์ระดับแนวหน้า ที่มีการควบคุมปืนแบบใหม่ ระบบ AI อันล้ำหน้า ระบบแต่งปืนใหม่ รวมถึงเกมเพลย์และกราฟิกอื่นๆ ที่รังสรรค์มาใหม่ซึ่งจะยกระดับแฟรนไชส์ขึ้นไปอีก').style('font-size: 18px; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7); ')
              #เความต้องการของระบบ
              ui.label('SYSTEM REQUIREMENTS').style('font-size: 25px; font-weight: bold; color: white; margin-top: 50px; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);').classes('mx-auto')
              with ui.row():
               with ui.card().tight().classes('w-[450px] h-[160px] justify-start').style('background: linear-gradient(to right, #254120, #529446); margin-left:241px'):
                with ui.card_section():
                      ui.label('Minimum Specifications').style('font-size: 25px; font-weight: bold; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('OS: Windows 10 64 Bit').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('CPU: Intel Core i3-6100 / Core i5-2500K or AMD Ryzen 3 1200').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('RAM: 8 GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('Video Card: NVIDIA GeForce GTX 960 or AMD Radeon RX 470').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                      ui.label('Storage: 125 GB available space').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
               with ui.card().tight().classes('w-[532px] h-[160px] justify-start').style('background: linear-gradient(to right, #529446, #529446);'):
                with ui.card_section():
                       ui.label('Recommended Specifications').style('font-size: 25px; font-weight: bold; color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('OS: Windows 10 64 Bit').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('CPU: Intel Core i5-6600K / Core i7-4770 or AMD Ryzen 5 1400').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('RAM: 12 GB').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('Video Card: NVIDIA GeForce GTX 1060, AMD Radeon RX 580 or Intel Arc A770').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
                       ui.label('Storage: 125 GB available space').style('color: white; text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.7);')
              # แถบบาร์6
              with ui.header().style('background: linear-gradient(to right, #254120, #529446); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2)').classes(replace='row items-center') as header:
               with ui.row().classes('w-full justify-between items-center'):
                with ui.tabs() as tabs:
                 ui.image('https://cdn.discordapp.com/attachments/1149668982127853572/1286314883801153722/ROCKET444.png?ex=66ed7596&is=66ec2416&hm=a54383ae76f0c99239ded909c2756da6d141f118a5a7c9317baa4e3e662e8981&').classes('w-[300px] h-[49px]')
                 ui.tab('Store').on('click',main_store)
                 ui.tab('Library').on('click', show_library_content)
                 ui.tab('Shopping Cart').on('click', show_shopping_cart_content)
                with ui.row().style('display: flex; justify-content: flex-end;'):
                 ui.button('Log in', icon='account_ circle').props('flat color=white')

            #การ์ดเกมในหน้าร้านค้า
             with ui.card().tight().props('height=200px').classes('w-[200px] mt-4').style('background: linear-gradient(to right, #254120, #529446);'):
                  ui.image('https://img2.pic.in.th/pic/40cd.png').classes('w-full h-full object-cover')
                  with ui.card_section():
                   ui.label('COD : WARFARE 2').style('color: white; font-size: 20px;')
                   ui.button('฿1,224.50').style('font-size: 10px;').props('color="green"').on('click', lambda: ui.run_javascript('window.location.href="/cod_warfare2"'))






            


# UI ของ Library
Library_content = ui.element('div').style("background-color: #4B0082; padding: 20px; border-radius: 10px;").classes('hidden')
with Library_content:
    ui.label('LIBRARY').style("font-size: 24px; color: white; margin-bottom: 10px;")
    library_display = ui.element('div')
    update_library()
    
    
# UI ของตะกร้าสินค้า
Shopping_Cart_content = ui.element('div').style("background-color: #8A0D38; padding: 20px; border-radius: 10px;").classes('hidden')
with Shopping_Cart_content:
    ui.label('MY BASKET').style("font-size: 24px; color: white; margin-bottom: 10px;")
    cart_display = ui.element('div')
    ui.button('Go to Library', on_click=move_to_library).style('margin-top: 10px;')  # ปุ่มสำหรับย้ายไปที่ Library
    ui.button('CLOSE', on_click=lambda: Shopping_Cart_content.classes(add='hidden')).style('margin-top: 10px;')


ui.run()