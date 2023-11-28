WiFi Voucher App + GCash Config

INVOLVED APPS:
1. Omada Cloud Controller (Web)
2. Voucher WiFi App (Desktop)
3. Google Drive (Web)
4. MacroDroid (Mobile)
5. GCash (Mobile)


*** REQUIREMENTS ***
------------------------------------------------------------------

0. ** SHOULD HAVE A WINDOWS PC/LAPTOP
    * TESTED: Windows 10, Windows 11

   0.1  Install python : Download here => https://www.python.org/downloads/
   0.2  Install node.js : Download here => https://nodejs.org/en/download/
        0.2.1  (CMD) Execute after installation: npm install --global http-server
        0.2.2  (CMD) Type "http-server" to check if working properly
        0.2.3  Execute below ONLY IF "http-server" is not working
               0.2.3.1  (Browser) Empty cache & hard reload page (dev tools, ctrl + right click) 
   0.3  (CMD) pip install customtkinter
   0.4  (CMD) pip install Pillow
   0.5  (CMD) pip install google-auth
   0.6  (CMD) pip install google-api-python-client
   0.7  Download WiFi Voucher App
        0.7.1 Download here => https://github.com/cleifwork/GCONNECT
        0.7.2 Click Code > Download Zip
        0.7.3 Extract main folder to your Desktop
        0.7.4 Rename main folder to GCONNECT


1. ** OMADA CLOUD CONTROLLER ACCOUNT
    * NOTES: Not tested using SDN Controller and OC200. 
             IF the exported vouchers (CSV) has the same columns as the Cloud Controller it should still work.
   
   1.1  Login to your Omada Cloud Controller => https://omada.tplinkcloud.com/
   1.2  Launch your Controller
   1.3  Go to Settings (Global)
        1.3.1  Select Export Data
               1.3.1.1  Export List: Voucher Codes  
               1.3.1.2  Format: CSV 
               1.3.1.3  Portal: "Your WiFi Name" 
               1.3.1.4  Save file to this folder: %USERPROFILE%\Desktop\GCONNECT\raw_csv


2. ** SHOULD HAVE A GOOGLE ACCOUNT
   2.1  Enable Google Drive API here => https://developers.google.com/drive/api/guides/enable-sdk
   2.2  Take NOTE of your API KEY for later use
   2.3  Create Service Account 
   2.4  Save Service Account Key (.json) in the WiFi Voucher App main folder: %USERPROFILE%\Desktop\GCONNECT
   2.5  Create these folders in your GDrive: My Drive/VOUCHER_WIFI_NAME/vouchers (e.g. My Drive/GCONNECT/vouchers)
   2.6  Upload empty text files named like the ff. to GCONNECT/vouchers folder.
        2.6.1   5php_vouchers.txt
        2.6.2  10php_vouchers.txt
        2.6.3  15php_vouchers.txt
        2.6.4  20php_vouchers.txt
        2.6.5  30php_vouchers.txt
        2.6.6  50php_vouchers.txt
        2.6.7  99php_vouchers.txt
   
   2.7  Get "GCONNECT/vouchers" FOLDER_ID by sharing the folder to EVERYONE WITH LINK.
        * NOTES: It's the string in between "https://drive.google.com/drive/folders/" and "?usp=sharing"
        * Example: For "GCONNECT/vouchers" => https://drive.google.com/drive/folders/GET_FOLDER_ID_HERE?usp=sharing
        
        2.6.1  Paste FOLDER_ID inside this text file: %USERPROFILE%\Desktop\GCONNECT\put_folder_id_here.txt
   
   2.8  Get each text file's FILE_ID by sharing the file to EVERYONE WITH LINK.
        2.8.1  Get the LINK
        * NOTES: It's the string in between "https://drive.google.com/file/d/" and "/view?usp=sharing"
        * Example: For " 5php_vouchers.txt" => https://drive.google.com/file/d/GET_FILE_ID_HERE/view?usp=sharing

        2.8.2 Save these FILE_IDs for later use


3. ** SHOULD HAVE AN ANDROID PHONE
    * BRAND/MODELS:
      Highly Recommended: Nexus, HTC, Pixels, Android One, Nokia, Sony, Other Newer Vendors
      Recommended       : RealMe, Blackview, Oppo, Vivo, Lenovo, Meizu, Asus, Xiaomi
      Not So Recommended: Huawei, Samsung, OnePlus

   3.1  Install MacroDroid (Google Play Store)
   3.2  Download macro here => https://drive.google.com/drive/folders/1QfV7-ELD7QrVR5gsQI3qZu3njGw3SMYV
   3.3  Import downloaded macro to MacroDroid
        3.3.1  Go inside the imported macro
        3.3.2  Add TRIGGER (Webhook)
               3.3.2.1  Configure Webhook
                        3.3.2.1.1  Add Identifier: {sync_vouchers}
                        3.3.2.1.2  Copy the URL
                        3.3.2.1.3  (PC) Go to your WiFi Voucher App main folder: %USERPROFILE%\Desktop\GCONNECT
                        3.3.2.1.4  (PC) Put the URL inside this text file: %USERPROFILE%\Desktop\GCONNECT\put_md_url_here.txt
        3.3.3  Update existing ACTION (second IF CLAUSE)
               3.3.3.1  Configure and change Trigger Fired to the newly added Webhook
        3.3.4  Save changes then enable the macro    
        3.3.5  Configure each voucher's HTTP Request (under second IF CLAUSE)
               3.3.5.1  Paste each FILE_ID accordingly in the URL (Settings tab)
               3.3.5.2  Add your Google Drive API key (Query Params tab)   
------------------------------------------------------------------

*** IDEAL VOUCHER PRINTING PREFERENCE ***
1. Layout     = Landscape (prints more voucher than portrait)
2. Paper Size = Letter (short)
3. Margin     = None
4. Scale      = Custom (93%)
5. Headers and Footers = unchecked (disabled)
6. Background Graphics = checked (only if you have a logo)

  * THIS CAN PRINT UP TO 32 VOUCHERS IN 1 PAGE
