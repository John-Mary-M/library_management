# --- Instructions Start Here ---

Setting Up and Accessing the Library Management App from GitHub

Hi there!  You've found the code for the Library Management App on GitHub! Here's how you can set it up on your own computer to use it.

## Before You Start:

Make sure you have Frappe and Bench already installed on your computer. If you don't, you'll need to install them first. You can find instructions on the Frappe Framework website (https://frappeframework.com/docs/v14/user/installation - Note: The installation process might vary slightly depending on the Frappe version. Refer to the official Frappe documentation for your version). You'll need to have "Bench" set up and working.

## Steps to Set Up the App:

Open your computer's "Terminal" or "Command Prompt".

Go to your Frappe "bench" folder.  Remember the folder where you installed Frappe Bench?  You need to be inside that folder in your Terminal.  Use the cd command to navigate there. For example, if your bench folder is called frappe_bench and it's in your home directory, you would type: `cd frappe_bench`

Clone (download) the Library Management App from GitHub.  Copy the following command and paste it into your Terminal and press Enter. Make sure to replace YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME with the actual GitHub address of the repository you want to download.  For example, if the GitHub repository address is https://github.com/MyName/library_management_app, the command would be:
```
bench get-app library_management_app --branch main https://github.com/MyName/library_management_app
```

Replace library_management_app with the name you want to give to the app folder on your computer. It's usually easiest to use the same name as the repository on GitHub.
Replace https://github.com/MyName/library_management_app with the actual URL of the GitHub repository where the app code is stored. You can find this URL on the GitHub repository page, it usually looks like "https://github.com/YourUsername/YourRepositoryName".
--branch main tells it to download the code from the "main" branch of the repository. If the repository uses a different main branch name (like master), you might need to adjust this.
Install the app in your Frappe site.  After the app is downloaded, you need to tell Frappe to install it in your site. Use this command in the Terminal, replacing your_site_name with the name of your Frappe site (e.g., library.localhost or site1.local):
`bench --site your_site_name install-app library_management_app`

Again, make sure library_management_app matches the folder name you used in the bench get-app command.

Update your Frappe site (migrate). This step is very important! It updates the database with any new things from the app (like new DocTypes or settings). Use this command, again replacing your_site_name: `bench --site your_site_name migrate`

Start the Frappe server.  To run the app, you need to start the Frappe server. Use this command: `bench start`

Keep this Terminal window open while you are using the app.

Access the Library Management App in your web browser. Open your web browser (like Chrome, Firefox, Safari) and go to your Frappe site's address. This is usually: `http://localhost:8000` or whatever URL you use to access your Frappe site.

Log in. You should see the login page.  Use your Frappe login details (usually "Administrator" and the password you set during Frappe setup).

Explore the Library Management App! Once you are logged in, you should see the Library Management App in your Frappe Desk (the main Frappe screen). You can usually find it in the "Awesome Bar" (search box at the top) by typing "Library Management" or by looking in the main menu.

Accessing the Custom Login Page (Important!)

If your custom login page replaces the default Frappe login page:  When you go to http://localhost:8000 (or your Frappe site address) in your browser, you should automatically see your custom login page instead of the standard Frappe login.

If your custom login page is at a different URL (not replacing the default): You will need to figure out the specific web address (URL) for your custom login page.  The person who created the app (that's me!) should provide this URL. It might be something like http://localhost:8000/your_custom_login_page_route (replace your_custom_login_page_route with the actual route).  Ask the app creator for the exact URL if you are not sure.

### Troubleshooting:
If you see any errors during these steps, carefully re-read each step and make sure you typed the commands correctly and replaced the placeholder names (like your_site_name, YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME, library_management_app) with your actual names.
If you still have problems, check the Frappe documentation or the Frappe forum for help, or ask the person who shared the app for assistance!

