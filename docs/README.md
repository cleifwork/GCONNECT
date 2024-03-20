
# GCONNECT APP: Print Voucher Only Version

- **Customizable Printouts:** GCONNECT offers a user-friendly interface to customize Wi-Fi voucher printouts directly from the CSV file, providing flexibility and adaptability to unique printing requirements.

- **User-Friendly Interface:** The application features a very simple interface, ensuring ease of use for both novice and experienced users. It simplifies complex processes, making voucher management more accessible.

## Demo

-   [GConnect App Demo](https://www.youtube.com/watch?v=eXLdvv9VYJA)
-   [GConnect Installation & Configuration](https://www.youtube.com/watch?v=fOBG7ZszJXA)

## Authors

- [@cleifwork](https://www.github.com/cleifwork)

## Installation & Configuration

**INVOLVED APPS:**
- Omada Cloud Controller (Web)
- GConnect App PVO (Desktop)

### REQUIREMENTS:
**1. SHOULD HAVE A WINDOWS PC/LAPTOP** 
> [!NOTE] 
> Tested in Windows 10 and Windows 11

- [Install python](https://www.python.org/downloads/) (recommended version: _**python-3.11.4**_)
- [Install node.js](https://nodejs.org/en/download/) (recommended version: _**node-v18.16.1**_)

**DOWNLOAD THE APP**		
- Download the **[GCONNECT PVO](https://github.com/cleifwork/GCONNECT/tree/GCONNECT-PVO)**
- Click Code > Download Zip
- Extract main folder to your Desktop
- Rename main folder to **'GCONNECT'**
- Run _**'Install.bat'**_ inside the **'GCONNECT'** folder
- Run _**'InitialConfig.bat'**_ inside **'GCONNECT'** folder

> [!NOTE] 
> If _"Windows Security Alert"_ window pops
```
> Click _"Allow access"_
```
						
> [!NOTE] 
> Execute the following **ONLY IF** _"http-server"_ is not working or vouchers are not displaying properly
```
> (BROWSER) Empty cache & hard reload page
> IF NOT Restart browser 
> IF NOT Restart PC       
```
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
    - Save file to **'GCONNECT'** folder

## Running Tests
- (GCONNECT) Launch _"GConnect App"_ shortcut from the Desktop

> [!NOTE] 
> If _"Windows protected..."_ SmartScreen window pops
```
> Click _"More info"_  
> Run anyway
```

- (GCONNECT) Click the **"PRINT VOUCHERS"** button to check if it can now print vouchers automatically

## Optimizations
-   Created second button with dynamic background depending on voucher amount

## Screenshots

![App Screenshot](https://drive.google.com/thumbnail?id=1w-nk1QCgyCH2ZYK-dEdqrKQn7a80_Vmd)

[Zoom App Screenshot](https://drive.google.com/uc?id=1w-nk1QCgyCH2ZYK-dEdqrKQn7a80_Vmd)

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

