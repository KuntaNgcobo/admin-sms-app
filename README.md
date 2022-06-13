# Admin SMS App
This is an application in which one can send an SMS to someone's phonenumber via the site's Send-SMS form.

# How to use
You can access to app from this url: https://sender-sms-app.herokuapp.com

Once you have logged in, you will be navigated to the sms_app page, where you can view the previously sent messages, access page to send form to the user or logout.

To send a SMS to number:
    - Click on the link link with text `Send a SMS`, to which you'll be navigated to the relevant page
    - Fill out the form with the relevant information (only one number works - the Twilio verified number at the moment) and press send

To reload status of the SMS that were from the list of message:
    - Click on the link with text `Reload SMS Status` or refresh the page, the page will have the messsages with updated SMS statuses

To logout:
    - Click on the link with text `Logout` and you'll redirected to the login page (if you naviagte to the login page yourself you'll logged out as well) 