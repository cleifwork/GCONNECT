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
            But if the exported vouchers (.csv) has the same format as the Cloud Controller it should still work.
   
   1.1  Login to your Omada Cloud Controller => https://omada.tplinkcloud.com/
   1.2  Launch your Controller
   1.3  Go to Settings (Global)
        1.3.1  Select Export Data
               1.3.1.1  Export List: Voucher Codes  
               1.3.1.2  Format: CSV 
               1.3.1.3  Portal: "Your WiFi Name" 
               1.3.1.4  Save file to this folder: %USERPROFILE%\Desktop\GCONNECT\raw_csv


2. ** SHOULD HAVE A GOOGLE ACCOUNT
   2.1  Google Drive API needs to be ENABLED.
   2.2  Create Service Account 
   2.3  Save Service Account API KEY (.json) in the WiFi Voucher App main folder: %USERPROFILE%\Desktop\GCONNECT
   2.4  Create these folders in My Drive: > VOUCHER_WIFI_NAME/vouchers (e.g. My Drive/GCONNECT/vouchers).
   2.5  Upload empty text files named like the ff. to GCONNECT/vouchers folder.
        2.5.1   5php_vouchers.txt
        2.5.2  10php_vouchers.txt
        2.5.3  15php_vouchers.txt
        2.5.4  20php_vouchers.txt
        2.5.5  30php_vouchers.txt
        2.5.6  50php_vouchers.txt
        2.5.7  99php_vouchers.txt
   
   2.6  Get "GCONNECT/vouchers" Folder ID.
        * NOTES: It's the string in between "https://drive.google.com/drive/folders/" and "?usp=sharing"
        * Example:
        2.6.1  For "GCONNECT/vouchers" => https://drive.google.com/drive/folders/FOLDER_ID_HERE?usp=sharing
        2.6.2  (PC) Paste Folder ID inside this text file: %USERPROFILE%\Desktop\GCONNECT\put_folder_id_here.txt
   
   2.7  Get each text file's ID, (should look like the ff. URL sample, will vary per google account)
        * NOTES: It's the string in between "https://drive.google.com/file/d/" and "/view?usp=sharing"
        * Example:
        2.7.1  For " 5php_vouchers.txt" => https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
        2.7.2  For "10php_vouchers.txt" => https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
        2.7.3  For "15php_vouchers.txt" => https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
        2.7.4  For "20php_vouchers.txt" => https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
        2.7.5  For "30php_vouchers.txt" => https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
        2.7.6  For "50php_vouchers.txt" => https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
        2.7.7  For "99php_vouchers.txt" => https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing


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
------------------------------------------------------------------

*** IDEAL VOUCHER PRINTING PREFERENCE ***
1. Layout     = Landscape (prints more voucher than portrait)
2. Paper Size = Letter (short)
3. Margin     = None
4. Scale      = Custom (93%)
5. Headers and Footers = unchecked (disabled)
6. Background Graphics = checked (only if you have a logo)

  * THIS CAN PRINT UP TO 32 VOUCHERS IN 1 PAGE
