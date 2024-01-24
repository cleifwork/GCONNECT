Voucher WiFi App + GCash Config

INVOLVED APPS:
1. Omada Cloud Controller (Web)
2. GConnect App (Desktop)
3. Google Drive (Web)
4. MacroDroid (Mobile)
5. GCash (Mobile)


*** REQUIREMENTS ***
------------------------------------------------------------------

0. ** SHOULD HAVE A WINDOWS PC/LAPTOP
    * TESTED: Windows 10, Windows 11

   0.1  Install python : Download here => https://www.python.org/downloads/
        ** Recommended version: python-3.11.4

   0.2  Install node.js : Download here => https://nodejs.org/en/download/
        ** Recommended version: node-v18.16.1

        0.2.1  (CMD) Execute after installation: npm install --global http-server
        0.2.2  (CMD) Type "http-server" to check if working properly
		       0.2.2.1  If "Windows Security Alert" window pops
			            0.2.2.1.1  Click "Allow access"
						
        0.2.3  Execute below ONLY IF "http-server" is not working
               0.2.3.1  (BROWSER) Empty cache & hard reload page (dev tools, ctrl + right click) 
			   
   0.3  Install the following libraries in via CMD
	    0.3.1  pip install customtkinter
	    0.3.2  pip install packaging
	    0.3.3  pip install Pillow
	    0.3.4  pip install google-auth
	    0.3.5  pip install google-api-python-client
	    0.3.6  pip install pywin32
		
   0.4  Download GCONNECT APP
        0.4.1 Download here => https://github.com/cleifwork/GCONNECT
        0.4.2 Click Code > Download Zip
        0.4.3 Extract main folder to your Desktop
        0.4.4 Rename main folder to "GCONNECT"
		
   0.5 Launch the app thru "LaunchPad.bat" or the "GConnect App" shortcut.
	    0.5.1  If "Windows protected..." SmartScreen window pops
				0.5.1.1  Click "More info" > Run anyway


1. ** OMADA CLOUD CONTROLLER ACCOUNT
    * NOTES: Not tested using SDN Controller and OC200. 
             IF the exported vouchers (CSV) has the same columns as the Cloud Controller it should still work.
   
   1.1  Login to your Omada Cloud Controller => https://omada.tplinkcloud.com/
   1.2  Launch your Controller
   1.3  Go to Settings (Global)
        1.3.1  Select Export Data
               1.3.1.1  Export List: Voucher Codes  
               1.3.1.2  Format: CSV 
               1.3.1.3  Portal: "Your Voucher WiFi Name" 
               1.3.1.4  Save file to this folder: %USERPROFILE%\Desktop\GCONNECT\raw_csv


2. ** SHOULD HAVE A GOOGLE ACCOUNT
   2.1  Login to to your google account
   2.2  Enable Google Drive API here => https://console.cloud.google.com/
   2.3  Create a NEW PROJECT (use your voucher wifi portal name)
   2.4  Goto APIs & Services
        2.4.1  +ENABLE APIS & SERVICES 
        2.4.2  Select Google Drive
        2.4.3  ENABLE

   2.5  Credentials Configuration
        2.5.1  Service Account Creation:
               2.5.1.1  Goto "Credentials" (with the key icon)
               2.5.1.2  Click "+CREATE CREDENTIALS"
	       2.5.1.3  Select Service Account
	       2.5.1.4  Give it Account Name (OPTIONAL)
	       2.5.1.5  Give it Account ID (REQUIRED)
	       2.5.1.6  Give it Description (OPTIONAL)
	       2.5.1.7  CREATE AND CONTINUE
	       2.5.1.8  Give it an "Owner" role
	       2.5.1.9  DONE
	       2.5.1.10 Click the newly created Service Account
	       2.5.1.11 Goto "KEYS" tab
	       2.5.1.12 Click ADD KEY
	       2.5.1.13 Create new key
	       2.5.1.14 Key type: JSON 
	       2.5.1.15 CREATE (file will be downloaded)
	       2.5.1.16 Rename file to "service_account" (.json)
	       2.5.1.17 Save to => "%USERPROFILE%\Desktop\GCONNECT".

	2.5.2  API Key Creation:
               2.5.2.1  Go back to +CREATE CREDENTIALS
               2.5.2.2  Select API KEY
               2.5.2.3  Copy API KEY first
               2.5.2.4  Click "Edit API key" in the pop-up window
               2.5.2.5  Select "Restrict API key" under API restrictions
               2.5.2.6  Check Google Drive API > OK > SAVE
               2.5.2.7  Paste API KEY to this file => "%USERPROFILE%\Desktop\GCONNECT\put_api_key_here.txt".      
   
   2.6  (GCONNECT APP) Click "RUN INITIAL CONFIG" button
      * NOTES: Wait for the browser to open, showing the macro file and voucher folder

   2.7  Download the macro file then transfer to your android phone
      * NOTES: Below are applicable only if you're using the same Google Acount in your PC & Android
        2.7.1  (ANDROID) Launch Google Drive App
        2.7.2  (ANDROID) Goto "Shared" tab
        2.7.3  (ANDROID) Go inside "GCONNECT" folder
        2.7.4  (ANDROID) Tap more option (⋮) beside the macro file
        2.7.5  (ANDROID) Tap "Open with" (should open with MacroDroid automatically)
        2.7.6  Proceed to STEP: 3.2.6


3. ** SHOULD HAVE AN ANDROID DEVICE (Voucher Server Phone)
    * SOME REQUIREMENTS: 
      => Phone must not be rooted
      => Phone must have a active sim card 
      => Phone must have available service (signal)
      => Phone must have SMS credits (load for texting)
      => Phone must be connected to WiFi always
      => Phone must have separate GCash account installed
      => Phone must be able to receive GCash realtime notification

   3.1  Install MacroDroid (Google Play Store)
        3.1.1  Recommended permission for MacroDroid
               3.1.1.1  Give app admin rights
               3.1.1.2  Disable battery optimization
               3.1.1.3  Allow background autostart
               3.1.1.4  Give app notification access
               3.1.1.5  Lock app in recent app tray
   3.2  Import downloaded macro to MacroDroid or Import via Google Drive 
        3.2.1  Launch MacroDroid
        3.2.2  (HOME) Tap on Export/Import
        3.2.3  Tap on Storage under Import
        3.2.4  Browse macro in your local storage 
        3.2.5  Open the imported macro
        3.2.6  Tap on the Webhook trigger
               3.2.6.1  Tap Configure
               3.2.6.2  Copy the URL > Press Back button
               3.2.6.3  Send URL to PC (looks like this => https://trigger.macrodroid.com/DEVICE_ID/sync_voucher)
               3.2.6.4  (PC) Put the URL inside this text file => "%USERPROFILE%\Desktop\GCONNECT\put_md_url_here.txt"
        3.2.7  Tap on the import button (≡+) then enable the macro  
        3.2.8  (GCONNECT APP) Click EXTRUP + SYNC


4. ** PERFORM TESTING
   4.1  Send a GCash amount (5.00) to the Server Phone's GCash number.
        4.1.1  Sender should receive WiFi Voucher via SMS 
------------------------------------------------------------------

*** IDEAL VOUCHER PRINTING PREFERENCE ***
1. Layout     = Landscape (prints more voucher than portrait)
2. Paper Size = Letter (short)
3. Margin     = None
4. Scale      = Custom (93%)
5. Headers and Footers = unchecked (disabled)
6. Background Graphics = checked (only if you have a logo)

  * THIS CAN PRINT UP TO 32 VOUCHERS IN 1 PAGE