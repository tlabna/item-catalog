# Project: Item Catalog

The purpose of this project was to develop a web application that provides a list of items within a variety of categories and integrate third party user registration and authentication. Authenticated users should have the ability to post, edit, and delete their own items.

This project utilizes Flask, SQLAlchemy, Jinja2, HTML, JQUERY, CSS, Javascript, and Oauth2
___

### Dependencies
- Virtual Box
- [Vagrant](https://www.vagrantup.com/downloads.html)
- Python 2.7
- Web browser
- Shell
- Google and Facebook account
- Flask
- SQLAlchemy

___

### How to run project

- Clone repository: `git clone https://github.com/tlabna/item-catalog.git`.
- In your shell change directory to project directory `cd item-catalog/vagrant/catalog/`
- Start vagrant by typing `vagrant up`. *This may take some time.*
- Start vagrant shell by typing `vagrant ssh`.
- Go to the shared folder `cd /vagrant/catalog`
- Setup database by typing `python database_setup.py`. *(This will create database **music.db**)*
- Next to populate database with dummy data, type `python dummy_data.py`.

Before starting the web application, to get authentication/authorization with Oauth2 working, you will need to setup your own Google and Facebook API console projects. **Client IDs for both are not supplied and you must generate your own**

##### Google

- Steps to create a [Google API console project](https://developers.google.com/identity/sign-in/web/devconsole-project)
- Download client secret JSON by clicking on **Download JSON** under credentials in your console.
- Add downloaded file to the `/catalog` directory and rename to `client_secrets.json`.
- In your Google API console, under **Credentials > Authorized JavaScript origins** add URL:
`http://localhost:5000`
- In your Google API console, under **Credentials > Authorized redirect URIs** add URLs:
`http://localhost:5000/`,
`http://localhost:5000/login`,
`http://localhost:5000/gconnect`,
`http://localhost:5000/gdisconnect`,
- In file **login.html**, replace `YOUR_CLIENT_ID` with your client ID.

##### Facebook
- Steps to create a [Facebook API console project](https://developers.facebook.com/docs/facebook-login/web)
- In your Facebook console, add **Site URL** `http://localhost:5000/`
- Create file `fb_client_secrets.json` under the `/catalog` directory and fill it in with
```
{
  "web": {
    "app_id": "YOUR_APP_ID",
    "app_secret": "YOUR_APP_SECRET"
  }
}
```
- In file **login.html**, replace `YOUR_APP_ID` with your app ID.

##### Running the web application

- Once all above steps have been completed, in your terminal type `python main.py` to run the application.
- Open your web browser at `http://localhost:5000/`


**You should now have a running Item Catalog application**

___

#### Accessing JSON Endpoints

To test JSON Endpoints for this project, you can navigate to the following URLs below:

**View JSON for all catagories**
```
http://localhost:5000/genre/JSON
```

**View JSON for all items under a catagory**
```
http://localhost:5000/genre/GENRE_ID/JSON
```

**View JSON for a single item**
```
http://localhost:5000/genre/GENRE_ID/song/SONG_ID/JSON
```
___

### How to stop running application (Stop the application, exit the SSH session and shutdown the VM)

````
[press Ctrl+C to stop the application]
$ exit
$ vagrant halt
```
