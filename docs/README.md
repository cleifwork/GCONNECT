
# GCONNECT APP: Wi-Fi Voucher Automation Middleware

The GCONNECT APP is a powerful middleware solution designed to streamline the voucher management process between Omada Cloud Controller exports and MacroDroid's pre-configured macros. This application acts as a bridge, automating the segregation of voucher data based on pricing and facilitating seamless transmission to MacroDroid.
Key Features:

Experience unparalleled automation and efficiency with the GCONNECT APP, your go-to solution for optimizing voucher workflows and enhancing productivity in the dynamic landscape of network management.

## Key Features

- Automated Voucher Segregation: GCONNECT intelligently categorizes, and segregates voucher data exported from Omada Cloud Controller, ensuring efficient organization based on pricing tiers.

- MacroDroid Integration: With seamless integration with MacroDroid, GCONNECT directly transmits pre-configured macros, optimizing the execution of tasks and workflows associated with voucher management.

- Dynamic Macro Configuration: The app dynamically generates and configures macros based on the pricing information derived from the exported voucher data, eliminating manual intervention, and reducing the risk of errors.

- Customizable Printouts: GCONNECT offers a user-friendly interface to customize Wi-Fi voucher printouts directly from the CSV file, providing flexibility and adaptability to unique printing requirements.

- User-Friendly Interface: The application features a very simple interface, ensuring ease of use for both novice and experienced users. It simplifies complex processes, making voucher management more accessible.


## Demo

Insert gif or link to demo


## Authors

- [@cleifwork](https://www.github.com/cleifwork)
## Environment Variables

To run this project, you will need to add the following environment variables to your 'put_api_key_here.txt' file and GCONNECT folder.

`API_KEY`

`service_account.json`


## Installation & Configuration


### INVOLVED APPS:
- Omada Cloud Controller (Web)
- GConnect App (Desktop)
- Google Drive (Web)
- MacroDroid (Mobile)
- GCash (Mobile)


### REQUIREMENTS:
#### 1. SHOULD HAVE A WINDOWS PC/LAPTOP (tested on: Win10, Win11)

- [Install python](https://www.python.org/downloads/) (recommended version: python-3.11.4)
- [Install node.js](https://nodejs.org/en/download/) (recommended version: node-v18.16.1)

- (CMD) Execute after installation: 
        
```bash
  npm install --global http-server
```
- (CMD) Run the following to check if working properly
```bash
http-server
```

#### NOTES: If "Windows Security Alert" window pops
-   Click "Allow access"
						
#### NOTES: Execute the following commands ONLY IF "http-server" is not working or vouchers are not displaying
-   (BROWSER) Empty cache & hard reload page
-   Restart browser 
-   Restart PC       

#### Install the following libraries via CMD
```bash
pip install customtkinter
pip install packaging
pip install Pillow
pip install google-auth
pip install google-api-python-client
pip install pywin32
````
		
-   Download [GCONNECT APP](https://github.com/cleifwork/GCONNECT)
-   Click Code > Download Zip
-   Extract main folder to your Desktop
-   Rename main folder to "GCONNECT"
-   Launch the app thru "LaunchPad.bat" or the "GConnect App" shortcut.

#### NOTES: If "Windows protected..." SmartScreen window pops
-   Click "More info" > Run anyway


#### 2. OMADA CLOUD CONTROLLER ACCOUNT
##### NOTES: Not tested using SDN and OC200, BUT should still work provided thatmexported CSV file has the same columns as CBC.
- Login to your [Omada Cloud Controller](https://omada.tplinkcloud.com/)
-   Launch your Controller
-   Go to Settings (Global)
-   Select Export Data
-   Export List: Voucher Codes  
    - Format: CSV 
    - Portal: "Your Voucher WiFi Name" 
    - Save file to: %USERPROFILE%\Desktop\GCONNECT\raw_csv


#### 3. SHOULD HAVE A GOOGLE ACCOUNT
-   Login to to your google account
-   Enable [Google Drive API](https://console.cloud.google.com/)
-   Create a NEW PROJECT (use your voucher wifi portal name)
-   Goto APIs & Services
    -   ENABLE APIS & SERVICES 
    -   Select Google Drive
    -   ENABLE

##### CREDENTIALS CONFIGURATION
-   Service Account Creation:
    -   Goto "Credentials" (with the key icon)
    -   Click "+CREATE CREDENTIALS"
	-   Select Service Account
	-   Give it Account Name (OPTIONAL)
	-   Give it Account ID (REQUIRED)
	-   Give it Description (OPTIONAL)
	-   CREATE AND CONTINUE
	-   Give it an "Owner" role
	-   DONE
    -   Click the newly created Service Account
	-   Goto "KEYS" tab
	-   Click ADD KEY
	-   Create new key
	-   Key type: JSON 
	-   CREATE (file will be downloaded)
	-   Rename file to "service_account" (.json)
	-   Save to => "%USERPROFILE%\Desktop\GCONNECT".

-   API Key Creation:
    -   Go back to +CREATE CREDENTIALS
    -   Select API KEY
    -   Copy API KEY first
    -   Click "Edit API key" in the pop-up window
    -   Select "Restrict API key" under API restrictions
    -   Check Google Drive API > OK > SAVE
    -   Paste API KEY to this file => "%USERPROFILE%\Desktop\GCONNECT\put_api_key_here.txt"      
   
 ##### GCONNECT INITIALIZATION  
-   (GCONNECT APP) Click "RUN INITIAL CONFIG" button

##### NOTES: Wait for the browser to open, showing the macro file and voucher folder
-   Download the macro file then transfer to your android phone
##### NOTES: Below are applicable only if you're using the same Google Acount in your PC & Android
-   (ANDROID) Launch Google Drive App
-   (ANDROID) Goto "Shared" tab
-   (ANDROID) Go inside "GCONNECT" folder
-   (ANDROID) Tap more option (⋮) beside the macro file
-   (ANDROID) Tap "Open with" (should open with MacroDroid automatically)
-   Proceed to STEP: 3.2.6


#### 4. SHOULD HAVE AN ANDROID DEVICE (Voucher Server Phone)
    * SOME REQUIREMENTS: 
      => Phone must not be rooted
      => Phone must have an active sim card 
      => Phone must have available service (signal)
      => Phone must have SMS credits (load for texting)
      => Phone must be connected to WiFi always
      => Phone must have separate GCash account installed
      => Phone must be able to receive GCash realtime notification

##### Install MacroDroid (Google Play Store)
    * Recommended permissions for MacroDroid:
      => Give app admin rights
      => Disable battery optimization
      => Allow background autostart
      => Give app notification access
      => Lock app in recent app tray
      => Intall MacroDroid Helper (Play Store)
      => Grant [WRITE_SECURE_SETTINGS](https://www.youtube.com/watch?v=_WLbhtpC5ls&ab_channel=JacobL)
-   Import downloaded macro to MacroDroid or Import via Google Drive 
-   Launch MacroDroid
    -   (Home Tab) Tap on Export/Import
    -   Tap on Storage under Import
    -   Browse macro in your local storage 
    -   Open the imported macro
    -   STEP: 3.2.6  Tap on the Webhook trigger
        -   Tap Configure
        -   Copy the URL > Press Back button
        -   Send URL to PC 
```bash        
looks like this => https://trigger.macrodroid.com/DEVICE_ID/sync_voucher
````

-   (PC) Put the URL inside this text file => "%USERPROFILE%\Desktop\GCONNECT\put_md_url_here.txt"
-   (MD) Tap on the import button (≡+) then enable the macro  
-   (GCONNECT APP) Click EXTRUP & SYNC
## Running Tests

-   Send a GCash amount PHP 5.00 to the Server Phone's GCash number.
    -   Sender should receive WiFi Voucher via SMS. 



## Optimizations

-   Refactored code removing redundancy
-   Reduced macro size from 229kb to 44kb, by restructuring multiple IF/ELSE statement and putting similar variables to one dictionary/array 
-   Reducing file asset needed by automatically extracting the required data from the source file


## Screenshots

![App Screenshot](https://drive.google.com/file/d/1e4YSlZMKv2KPSJopF8owPT_tNJgetqAF/view?usp=sharing)


## Support

#### For support, join our FB Group
[GConnect App (Omada Voucher Solution)](https://www.facebook.com/groups/1776872022780742) 
  
#### Or subcribe to our YouTube Channel
[@JDIYMPH](https://www.youtube.com/channel/UC9O3ezuyjS7C6V7-ZAHCQrA)
## Tech Stack

**Client:** Python, HTML, Batch

**Server:** Node, GDrive, MacroDroid


## Related

### Ideal Voucher Printing Preference
    Layout              : Landscape
    Paper Size          : Letter (short)
    Margin              : None   
    Scale               : Custom (93%)
    Headers & Footers   : Unchecked (disabled)
    Background Graphics : Checked (if you have logo)
#### NOTES: This can print up to 32 vouchers in 1 page.

