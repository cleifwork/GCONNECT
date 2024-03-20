
# GCONNECT APP: Print Voucher Only Version

- **Customizable Printouts:** GCONNECT offers a user-friendly interface to customize Wi-Fi voucher printouts directly from the CSV file, providing flexibility and adaptability to unique printing requirements.

- **User-Friendly Interface:** The application features a very simple interface, ensuring ease of use for both novice and experienced users. It simplifies complex processes, making voucher management more accessible.

_Experience unparalleled automation and efficiency with the GCONNECT APP, your go-to solution for optimizing voucher workflows and enhancing productivity in the dynamic landscape of network management._
## Demo

-   [GConnect App Demo](https://www.youtube.com/watch?v=eXLdvv9VYJA)
-   [GConnect Installation & Configuration](https://www.youtube.com/watch?v=fOBG7ZszJXA)


## Authors

- [@cleifwork](https://www.github.com/cleifwork)

## Installation & Configuration

**INVOLVED APPS:**
- Omada Cloud Controller (Web)
- GConnect App (Desktop)

### REQUIREMENTS:
**1. SHOULD HAVE A WINDOWS PC/LAPTOP** 
> [!NOTE] 
> Tested in Windows 10 and Windows 11

- [Install python](https://www.python.org/downloads/) (recommended version: _**python-3.11.4**_)
- [Install node.js](https://nodejs.org/en/download/) (recommended version: _**node-v18.16.1**_)

- (CMD) Execute after installation: 
        
```
  npm install --global http-server
```
- (CMD) Run the following to check if working properly
```
http-server
```

> [!NOTE] 
> If _"Windows Security Alert"_ window pops
- Click _"Allow access"_
						
> [!NOTE] 
> Execute the following **ONLY IF** _"http-server"_ is not working or vouchers are not displaying properly
- (BROWSER) Empty cache & hard reload page
- Restart browser 
- Restart PC       

**Install the following libraries via CMD**
```
pip install customtkinter
pip install packaging
pip install Pillow
pip install google-auth
pip install google-api-python-client
pip install pywin32
```
		
-   Download the **[GCONNECT APP](https://github.com/cleifwork/GCONNECT)**
-   Click Code > Download Zip
-   Extract main folder to your Desktop
-   Rename main folder to **'GCONNECT'**
-   Launch the app thru _'LaunchPad.bat'_ or the _"GConnect App"_ shortcut.

> [!NOTE] 
> If _"Windows protected..."_ SmartScreen window pops
-   Click _"More info"_ > Run anyway

**2. OMADA CLOUD CONTROLLER ACCOUNT**
> [!NOTE] 
> Although not tested with SDN and OC200, it should still function properly as long as their exported CSV file adheres to the CBC formatting.
- Login to your [Omada Cloud Controller](https://omada.tplinkcloud.com/)
-   Launch your Controller
-   Go to Settings (Global)
-   Select Export Data
-   Export List: Voucher Codes  
    - Format: CSV 
    - Portal: _"Your Voucher WiFi Name"_ 
    - Save file to _**'%USERPROFILE%\Desktop\GCONNECT\raw_csv'**_

## Running Tests
-   (GCONNECT) Click on **'Local Variables'** to verify if the voucher codes have been successfully added to their respective voucher variables.

## Optimizations

-   Refactored the code to eliminate redundancy.
-   Successfully reduced the macro size from 229KB to 44KB by restructuring multiple IF/ELSE statements and consolidating similar variables into a single dictionary/array.
-   Optimized file asset usage by automatically extracting the necessary data from the source file.
## Screenshots

![App Screenshot](https://drive.google.com/thumbnail?id=1e4YSlZMKv2KPSJopF8owPT_tNJgetqAF)

[Zoom App Screenshot](https://drive.google.com/uc?id=1e4YSlZMKv2KPSJopF8owPT_tNJgetqAF)

## Support

#### For support, join our FB Group
[GConnect App (Omada Voucher Solution)](https://www.facebook.com/groups/1776872022780742) 
  
#### Or subcribe to our YouTube Channel
[@JDIYMPH](https://www.youtube.com/channel/UC9O3ezuyjS7C6V7-ZAHCQrA)
## Tech Stack

**Client:** Python, HTML, Batch

**Server:** Node (http-server)

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

