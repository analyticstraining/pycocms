# pycoCMS a less than minimalist CMS for Python Google App Engine

This is a really simple CMS based on Python GAE. It all started after reading this article:
[Custom user authentication with webapp2](http://blog.abahgat.com/2013/01/07/user-authentication-with-webapp2-on-google-app-engine).

I needed those info to secure a web application I was playing with and I decided that the best way to tinker around was to create a super small system that would allow users to read content or create content.
Right now content can only be a text snippet and nothing more, but there is built-in support for handling users with different subscription levels, etc.

This is not Wordpress or even an attempt to create another Wordpress. It is more of a skeleton app that you can customize to create your own website with user authentication and authorization. 
User can also have a subscription and access to certain pages can be limited by subscription type.

The HTML pages use Bootstrap and jQuery but there is practically no client side code and the server takes care of everything. I do not claim this is the best approach, just what made it easy for me to bootstrap development.

Hopefully this project will grow with the help of other people contributions.


Things you will need to take care of:

* Implement a payment system for user switching level
* subscription expiration handling
* landing page
* skinning


etc.

# Future Stuff/ wishes
* It would be really useful to add Google/Facebook/etc. based login.
* A proper user maangement page done as SPA
* Better emails

and so forth.

# How to start
First of all you will need Node & NPM to handle the little dependencies (Boostrap, jQuery, Font Awesome).

npm install
will install the dependencies.

run also:
gulp build-debug

and all the assets will be copied in the right folder. Launch it with the Google App Engine launcher and you are "done".

For the verification email to work in dev server you need to pass configuration parameters to the dev appserver. There is a batch file that does that (start.bat) for Windows.
