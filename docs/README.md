# GCONNECT APP: Wi-Fi Voucher Automation Middleware
> [!NOTE] 
> _A Macro Generating Solution for MacroDroid. A tool to automate E-Wallet payments (GCash, Maya). A WiFi Voucher Print-out Customizer for Omada Controllers **(With Omada Cloud Controller Voucher API Integration)**_

The **GCONNECT APP** is a powerful middleware solution designed to streamline the voucher management process between Omada Cloud Controller exports and MacroDroid's pre-configured macros. This application acts as a bridge, automating the segregation of voucher data based on pricing and facilitating seamless transmission to MacroDroid.

**MacroDroid** then effortlessly utilizes **SMS and push notifications from e-wallet apps** to activate predefined actions, creating a flexible and responsive system for managing vouchers.
## Key Features

- **Automated Voucher Segregation:** GCONNECT intelligently categorizes, and segregates voucher data exported from Omada Cloud Controller, ensuring efficient organization based on pricing tiers.

- **MacroDroid Integration:** With seamless integration with MacroDroid, GCONNECT directly transmits pre-configured macros, optimizing the execution of tasks and workflows associated with voucher management.

- **Dynamic Macro Configuration:** The app dynamically generates and configures macros based on the pricing information derived from the exported voucher data, eliminating manual intervention, and reducing the risk of errors.

- **Customizable Printouts:** GCONNECT offers a user-friendly interface to customize Wi-Fi voucher printouts directly from the CSV file, providing flexibility and adaptability to unique printing requirements.

- **User-Friendly Interface:** The application features a very simple interface, ensuring ease of use for both novice and experienced users. It simplifies complex processes, making voucher management more accessible.

_Experience unparalleled automation and efficiency with the GCONNECT APP, your go-to solution for optimizing voucher workflows and enhancing productivity in the dynamic landscape of network management._


## Demo
-   [GConnect App Demo](https://www.youtube.com/watch?v=eXLdvv9VYJA)
-   [GConnect Installation & Configuration](https://www.youtube.com/watch?v=O_8u0-8A6Nk)


## Authors
- [@cleifwork](https://www.github.com/cleifwork)


## Environment Variables
> [!IMPORTANT] 
> To run this project, you will need to add the following environment variables to your _**" .. / GCONNECT / app "**_ folder.

`put_api_key_here.txt` (File should contain GDrive API KEY)

`service_account.json` (File should contain GDrive Service Account)

`put_md_url_here.txt` (File should contain MacroDroid WebHook URL)

`creds.json` (File should contain your Omada Cloud-Based Controller credentials)

## Installation & Configuration
**INVOLVED APPS:**
- Omada Cloud Controller (Web)
- GConnect App (Desktop)
- Google Drive (Web)
- MacroDroid (Mobile)
- GCash | Maya (Mobile)

### REQUIREMENTS:
**1. SHOULD HAVE A WINDOWS PC/LAPTOP** 
> [!NOTE] 
> _Tested in Windows 10 and Windows 11_
		
- Download the **[GCONNECT-V3](https://github.com/cleifwork/GCONNECT/tree/GCONNECT-V3)**
- Click Code > Download Zip
- Extract main folder to your Desktop
- Launch the app thru _'LaunchPad.bat'_.

> [!TIP]
> During installation or first run, you may encounter security prompts:
- If the _"Windows protected..."_ SmartScreen window appears, click _"More info"_ and select _"Run anyway"_.
- If the _"Windows Security Alert"_ window appears, click _"Allow access"_.

**2. OMADA CLOUD CONTROLLER ACCOUNT**
> [!NOTE] 
> Although not tested with SDN and OC200, it should still function properly as long as their exported CSV file adheres to the [Cloud-Based Controller format](https://www.facebook.com/photo?fbid=122120593298569233&set=gm.1987184375082838&idorvanity=1776872022780742).
- Login to your [Omada Cloud Controller](https://omada.tplinkcloud.com/)
- Launch your Controller (Global View)
- Go to Settings
- Select Platform Integration
- Click **+Add New App**
    - App Name: **GConnect App**
    - Mode: Client
    - Role: Admin
    - Site Privileges: Sites
    - Select your site name
    - Click **Create**
- Click show icon under ACTION column
    - Obtain **"Interface Access Address"** and **"Omada ID"**
    - Copy & paste these credentials to **"..GCONNECT / app / creds.json"**
    - INFO: _You can open **"creds.json"** file via notepad_
    - Click OK
    - Obtain **"Client ID"** and **"CLIENT SECRET"**
    - Copy & paste these credentials to **"..GCONNECT / app / creds.json"**
- Click **Global View** drop down then select your site name
- Click **Hotspot** module from the side panel
    - INFO: _This will open a new tab_
    - Click **Vouchers** dropdown
    - Click **Voucher Groups** 
    - NOTES: _If you have existing vouchers already proceed below (IF NONE create one first)_
        - Click the **"Print Unused Vouchers"** icon under ACTION column
        - Obtain **Site ID** from the URL of the voucher print preview
        - INFO: _Site ID is the string in between **"?site="** and **"&omadacId"**_
        - Copy & paste this to **"..GCONNECT / app / creds.json"**

**3. SHOULD HAVE A GOOGLE ACCOUNT**
> [!TIP]
> **How to create [Service Account & API Key](https://www.youtube.com/watch?v=1Afr24gCKOo)**
- Login to to your google account
- Enable [Google Drive API](https://console.cloud.google.com/)
- Create a **NEW PROJECT** 
> [!TIP]
> You may use your Voucher WiFi Portal Name as project name
- Goto APIs & Services
    - ENABLE APIS & SERVICES 
    - Select Google Drive
    - ENABLE

**> CREDENTIALS CONFIGURATION**
- **Service Account Creation:**
    - Goto _"Credentials"_ (with the key icon)
    - Click **"+CREATE CREDENTIALS"**
	- Select Service Account
	- Give it Account Name **(REQUIRED)**
	- Give it Account ID **(REQUIRED - _Auto Generated_)**
	- Give it Description _(OPTIONAL)_
	- CREATE AND CONTINUE
	- Give it an **"Owner"** role
	- DONE
    - Click the newly created Service Account
	- Goto **"KEYS"** tab
	- Click ADD KEY
	- Create new key
	- Key type: **JSON** 
	- CREATE _(file will be downloaded)_
	- Rename file to _"service_account"_ (.json)
	- Save to _" .. / GCONNECT / app "_

- **API Key Creation:**
    - Go back to +CREATE CREDENTIALS
    - Select API KEY
    - Copy API KEY first
    - Click _"Edit API key"_ in the pop-up window
    - Select _"Restrict API key"_ under API restrictions
    - Check Google Drive API > OK > SAVE
    - Paste API KEY to this file _**'put_api_key_here.txt'**_      
   
**> GCONNECT INITIALIZATION**  
- (GCONNECT APP) Click **"RUN INITIAL CONFIG"** button

> [!NOTE]
> Wait for the browser to open, showing the macro file and voucher folder
-   Download the macro file then transfer to your android phone
> [!NOTE]
> The following instructions apply **ONLY IF** you are using the same Google account on both your PC and Android device, and already installed MacroDroid & GDrive on your phone.
-   (ANDROID) Launch Google Drive App
-   (ANDROID) Goto _"Shared"_ tab
-   (ANDROID) Go inside **"GCONNECT"** folder
-   (ANDROID) Tap more option **(⋮)** beside the macro file
-   (ANDROID) Tap _"Open with"_ (should open with MacroDroid automatically)
-   Proceed to **STEP: 3.2.6**

**4. SHOULD HAVE AN ANDROID DEVICE** (Voucher Server Phone)
> [!IMPORTANT]
> SOME REQUIREMENTS: 
```
- Phone must not be rooted
- Phone must have an active sim card 
- Phone must have available service (signal)
- Phone must have SMS credits (load for texting)
- Phone must be connected to the internet always (Data or WiFi)
- Phone is recommended to have separate GCash account (OPTIONAL)
- Phone must be able to receive GCash | Maya push notification
- Phone must be running Android 9 and up (RECOMMENDED) 
```
> [!NOTE] 
> What is _**'Push Notification'**_ ?
[Click to show sample](https://www.facebook.com/photo/?fbid=7982287951782295&set=gm.1833817397086204&idorvanity=1776872022780742)

> [!TIP]
> RECOMMENDED MODELS - Based on [dontkillmyapp](https://dontkillmyapp.com/)
```
- HTC
- Nokia (Android One)
- AOSP (Android One, Pixel, Nexus)
- Sony
- Unihertz
- Realme
- Blackview
- Oppo / Vivo
- Lenovo
- Wiko
- Asus
- Meizu 
- Other brands
```
> LESS RECOMMENDED MODELS
```
- Samsung
- Oneplus
- Xiaomi
- Huawei
```

**Install MacroDroid (Google Play Store)**
> [!IMPORTANT]
> MACRODROID & ANDROID RECOMMENDED PERMISSIONS/SETTINGS:
> [ADB Hack](https://www.macrodroidforum.com/index.php?threads/adb-hack-granting-extra-capabilities-via-the-adb-tool.48/)
```
- Ignore Battery Optimizations (MD Settings)
- Keep Accessibility Services Running (MD Settings)
- Set MacroDroid as Admin (Android Settings)
- Enable MacroDroid in Accessibility (Android Settings)
- Allow "Background Autostart" (Android Settings)
- Enable Notification Access (App Info Settings)
- Lock MacroDroid in recent app tray (OPTIONAL)
- Intall MacroDroid Helper from Play Store (OPTIONAL)
- Grant MacroDroid WRITE_SECURE_SETTINGS using ADB Hack (OPTIONAL)
- Enable Extended Unlock or Smart Unlock (OPTIONAL)
- Screen Pin MacroDroid (OPTIONAL)
```

> [!IMPORTANT]
> E-WALLET APPS RECOMMENDED PERMISSIONS/SETTINGS: (Gcash, Maya)
```
- Enable Notification Access (App Info Settings)
- Disable "Pause app activity if unused" (Infinix Models)
- Notification: Reminder Intensity = Follow App (Infinix Models)
- Disable Do-Not-Disturb mode (or Allow app in DND mode)
- Enable "Background data" (App Info Settings)
- Enable "Unrestricted data usage" (App Info Settings)
- Notifications & Status Bar: Smart Reminder (Disabled)
- Notifications & Status Bar: Lock Screen > Display Rule = Show notification content
- Notifications & Status Bar: Lock Screen > Wake Screen > Allow apps to wake screen
- Notifications & Status Bar: Lock Screen > Show notifications
```

> [!TIP]
> **How to grant [WRITE_SECURE_SETTINGS](https://www.youtube.com/watch?v=_WLbhtpC5ls&ab_channel=JacobL)**

- Import downloaded macro to MacroDroid or Import via Google Drive 
- Launch MacroDroid
    - (Home Tab) Tap on **Export/Import**
    - Tap on Storage under Import
    - Browse macro in your local storage 
    - Open the imported macro
    - **STEP: 3.2.6**  Tap on the Webhook trigger
        - Tap Configure
        - Copy the URL > Press Back button
        - Send URL to PC 


> [!TIP]
> **Looks like this:** _["https://trigger.macrodroid.com/{DEVICE_ID}/sync_vouchers"](https://www.facebook.com/photo/?fbid=1057719152807995&set=gm.1949664338834842&idorvanity=1776872022780742)_

- (PC) Put the URL inside this text file _**'put_md_url_here.txt'**_
- (MD) Tap on the import button **(≡+)** then enable the macro  
- (GCONNECT APP) Click **EXTRUP & SYNC**


## Running Tests
- (MD) Click on **Local Variables > VCHCD** to verify if the voucher codes have been successfully added to their respective amounts.
- Send amount to the Server Phone's registered e-wallet (Gcash | Maya) number.
    - Sender should receive WiFi Voucher via SMS. 


## Optimizations
- Implemented cache-busting in PRINT VOUCHER function (no need to clear cache when loading new csv file)
- Optimized code in "PrintVoucher.html" (for modularization and readability) 
- Added app logger to quickly identify newly encountered issues
- Added voucher API integration (directly fetching "VoucherList.csv" from the controller)
- Added option to add pokemon icons in your vouchers


## Screenshots
![App Screenshot](https://drive.google.com/uc?export=view&id=1WJ4y4uSUbzCsRefyo24yspFGiteloGoM)


## Support
#### Join our [FB Group](https://www.facebook.com/groups/1776872022780742) Or subscribe to our [YouTube](https://www.youtube.com/channel/UC9O3ezuyjS7C6V7-ZAHCQrA) Channel


## Tech Stack
- **Client:** Python, HTML, Batch, JS
- **Server:** Node.JS, GDrive, MacroDroid


## Related
> [!TIP] 
> **Ideal Voucher Printing Preference**
- Layout              : **Landscape**
- Paper Size          : **Letter** _(short)_
- Margin              : **None**   
- Scale               : **Custom (93%)**
- Headers & Footers   : **Unchecked (disabled)**
- Background Graphics : **Checked** _(if you have logo)_
> [!NOTE]
> _This can print up to 32 vouchers in a single page_

