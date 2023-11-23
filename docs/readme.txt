CUSTOM WIFI VOUCHER + APP + GCASH SETUP

INVOLVED APPS:
1. Omada Cloud Controller (Web)
2. Voucher WiFi App (Desktop)
3. Google Drive (Web)
4. MacroDroid (Mobile)
5. GCash (Mobile)


*** REQUIREMENTS ***
------------------------------------------------------------------

0. SHOULD HAVE A GOOGLE ACCOUNT
   0.1  Google Drive API needs to be ENABLED.
   0.2  Create Service Account 
   0.3  Save Service Account API KEY (service_account.json) in your VOUCHER WIFI APP root folder (../Desktop/GCONNECT).
   0.4  Create these folders in My Drive: > VOUCHER_WIFI_NAME/vouchers (e.g. My Drive/GCONNECT/vouchers).
   0.5  Upload empty text files named like the ff. to GCONNECT/vouchers.
        0.5.1  5php_vouchers.txt
        0.5.2  10php_vouchers.txt
        0.5.3  15php_vouchers.txt
        0.5.4  20php_vouchers.txt
        0.5.5  30php_vouchers.txt
        0.5.6  50php_vouchers.txt
        0.5.7  99php_vouchers.txt
   
   0.6  Get "GCONNECT/vouchers" folder ID.
        **NOTES: It's the string in between "https://drive.google.com/drive/folders/" and "?usp=sharing"

        0.6.1  (GCONNECT/vouchers) => https://drive.google.com/drive/folders/FOLDER_ID_HERE?usp=sharing
   
   0.7  Get each text file's ID, (should look like the ff. URL sample, will vary per google account)
        **NOTES: It's the string in between "https://drive.google.com/file/d/" and "/view?usp=sharing"

        0.7.1  ( 5php_vouchers.txt) => https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
        0.7.2  (10php_vouchers.txt) => https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
        0.7.3  (15php_vouchers.txt) => https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
        0.7.4  (20php_vouchers.txt) => https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
        0.7.5  (30php_vouchers.txt) => https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
        0.7.6  (50php_vouchers.txt) => https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
        0.7.7  (99php_vouchers.txt) => https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing


1. SHOULD HAVE AN ANDROID PHONE
   1.1  Install MacroDroid (voucher code generator)


2. SHOULD HAVE A WINDOWS PC/LAPTOP
   2.1  Install python : Download here => https://www.python.org/downloads/
   2.2  Install node.js : Download here => https://nodejs.org/en/download/
        2.2.1  (CMD) Execute after installation: npm install --global http-server
        2.2.2  (CMD) Empty cache & hard reload page only if "http-server" is not working properly (dev tools, ctrl + right click)
   2.3  (CMD) pip install customtkinter
   2.4  (CMD) pip install Pillow
   2.5  (CMD) pip install google-auth
   2.6  (CMD) pip install google-api-python-client
   2.7  Download GConnect WiFi Voucher App & extract folder to Desktop
        2.7.1 Download here => https://github.com/cleifwork/GCONNECT
        2.7.2 Rename root folder to GCONNECT
------------------------------------------------------------------

*** VERY IMPORTANT ***
Downloaded CSV file from Omada website 
should be place in the ff. path: "%USERPROFILE%\Desktop\WIFI_NAME_HERE\raw_csv"
Example: "%USERPROFILE%\Desktop\GCONNECT\raw_csv"
------------------------------------------------------------------

*** IDEAL VOUCHER PRINTING PREFERENCE ***
1. Layout     = Landscape (prints more voucher than portrait)
2. Paper Size = Letter (short)
3. Margin     = None
4. Scale      = Custom (93%)
5. Headers and Footers = unchecked (disabled)
6. Background Graphics = checked (only if you have a logo)

** INFO:THIS CAN PRINT UP TO 32 VOUCHERS IN 1 PAGE